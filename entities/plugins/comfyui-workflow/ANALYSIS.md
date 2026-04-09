---
name: Hermes Agent ComfyUI Workflow Plugin 分析
description: 深度分析 hermes-agent-comfyui-workflow 外掛的架構、流程與潛在問題
version: 1.1.0
created: 2026-04-09
updated: 2026-04-09
type: resource
tags: [tool, plugin, comfyui, image-generation, flux2, hermes]
sources: [~/.hermes/plugins/hermes-agent-comfyui-workflow/__init__.py]
---

# Hermes Agent ComfyUI Workflow Plugin — 深度分析

## 一、Plugin 發現與註冊機制

### 1. Plugin 結構

```
hermes-agent-comfyui-workflow/
├── __init__.py                    ← 核心程式碼（314 行）
├── plugin.yaml                     ← Plugin 元資料
├── README.md                       ← 使用說明
└── templates/
    ├── Comfyui_Hermes_單圖編輯工作流API_Template.json   ← I2I workflow（14 nodes）
    └── Flux2_klein_t2i_API_Template.json               ← T2I workflow（10 nodes）
```

### 2. Hermes Plugin 註冊方式

Plugin 透過 `register(ctx)` 函式註冊至 Hermes Agent：

```python
def register(ctx):
    ctx.register_tool(
        "comfyui_workflow",         # tool name（對外暴露的名稱）
        "comfyui-workflow",         # toolset name
        COMFYUI_WORKFLOW_SCHEMA,    # JSON schema（用於參數驗證）
        handle_comfyui_workflow,    # 處理函式
    )
```

此為 Hermes Agent 的標準 plugin 介面：plugin 提供一個 `register()` 函式，Hermes 在啟動時呼叫它，傳入 `ctx`（Hermes 上下文），plugin 呼叫 `ctx.register_tool()` 註冊自己的 tool。

---

## 二、Tool Schema 分析

### Tool 參數

| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `prompt` | string | ✅ | 圖片生成 / 編輯指令 |
| `workflow_type` | string | ✅ | `image_edit` 或 `text_to_image` |
| `image_url` | string | ❌ | 圖片路徑或 URL（`image_edit` 時必填） |
| `width` | integer | ❌ | 寬度，預設 1024 |
| `height` | integer | ❌ | 高度，預設 1024 |

### 環境變數（plugin.yaml 聲明）

```yaml
requires_env:
  - COMFY_API_URL        # ComfyUI 伺服器 URL
  - COMFY_TEMPLATE_DIR  # workflow JSON 模板目錄
  - COMFY_OUTPUT_DIR    # 圖片輸出目錄
```

額外支援（`__init__.py`）：
```python
COMFY_WORKFLOW_DEBUG=true   # 啟用除錯日誌
COMFY_WORKFLOW_LOG_DIR     # 除錯日誌寫入目錄
```

---

## 三、核心執行流程

```
handle_comfyui_workflow(params)
    ↓
_run_workflow(prompt, workflow_type, image_url, width, height)
    ├── _get_template_path(workflow_type)    # 讀取 workflow JSON 模板
    ├── _load_template(template_path)         # JSON parse
    ├── 根據 workflow_type 修改模板參數
    │   ├── image_edit: 修改 node 64/7/28
    │   └── text_to_image: 修改 node 67/77
    ├── POST /prompt → ComfyUI API           # 提交 workflow
    ├── 取得 prompt_id
    ├── _poll_for_result()                   # 輪詢等待完成
    │   ├── GET /history/{prompt_id}        # 每 2 秒查詢
    │   ├── 解析 outputs，取第一張圖片
    │   └── GET /view → 下載圖片到 output_dir
    └── 回傳結果 JSON
```

### Polling 機制

- **輪詢間隔**：固定 2 秒
- **超時**：600 秒（10 分鐘）
- **完成判斷**：找到任意 node 的 `outputs.images[0]` 即視為完成
- **圖片下載**：直接呼叫 ComfyUI `/view` endpoint

---

## 四、兩個 Workflow 節點圖分析

### 4.1 Text-to-Image（Flux2 T2I）

```
[66] INTConstant(1024) ─┐
                       ├─→ [77] EmptyFlux2LatentImage(w,h,batch=1)
[77] EmptyFlux2LatentImage ─────────────────┐
                                          │
[70] CLIPLoader ─→ [67] CLIPTextEncode(prompt) ─→ [73] KSampler
                                          │                  ↑
[71] UNETLoader ──────────────────────────┴───→ [76] ConditioningZeroOut(negative)
                                          │                  ↑
                                          └──────────────────┘
[68] VAELoader ─→ [69] VAEDecode ─→ [75] ImageCompressor(WEPB,q80) → output
```

**特點：**
- 純文生圖，無條件圖（negative conditioning 全零）
- denoise=1.0（全去噪）
- 圖片尺寸由 node 77 動態設定（width, height）
- 固定 seed：447638775894178

### 4.2 Image-Edit（Flux2 I2I）

```
[64] LoadImageFromBase64(image) ─→ [63:51] ImageResizeKJv2(w,h) ─┐
                                                               ├─→ [63:50] VAEEncode
[52] VAELoader ───────────────────────────────────────────────────┘
                                                               │
[61] CLIPLoader ─→ [7] CLIPTextEncode(prompt) ─────────────────┐  │
                                                           ↓  │
[63:49] GetImageSize ─→ [63:57] EmptyFlux2LatentImage ─→ [63:55] ReferenceLatent(cond+latent)
                                                           │  │
                                                           ↓  │
                                                        [58] KSampler(denoise=0.85)
                                                           │
                                                           ↓
[63:56] ConditioningZeroOut ─→ [63:60] ReferenceLatent ─→ [54] VAEDecode ─→ [53] ImageCompressor → output
```

**特點：**
- 使用 `ReferenceLatent` 節點（類似 IP-Adapter / Deep Negative）保留主體
- denoise=0.85（輕度去噪，保留原始結構）
- 尺寸由 `28` INTConstant 控制（目前為 `%height%`，width 被忽略）
- **潛在問題**：`63:57` EmptyFlux2LatentImage 的 width/height 接到 `63:49` GetImageSize，但後者是讀取上傳圖片尺寸作為 latent 大小，邏輯有矛盾（見第五章）

---

## 五、發現的問題與設計缺陷

### 🔴 問題 1：image_edit 的 width/height 參數無效

**位置：** `__init__.py` 第 207 行
```python
workflow["28"]["inputs"]["value"] = height
```

**分析：**
- Node 28 (`INTConstant`) 僅傳給 `63:51` ImageResizeKJv2 的 `width` 和 `height`
- 但 `63:57` EmptyFlux2LatentImage 的尺寸是接到 `63:49` GetImageSize（讀取**上傳圖片**的原始尺寸）
- 也就是說：`height` 參數**只改變了 ImageResizeKJv2 的中間處理尺寸**，但最終 latent 大小仍由上傳圖片決定
- `width` 參數根本**沒有被寫入 workflow**，整行 `workflow["..."]["inputs"]["width"]` 缺席

**建議：** 若要支援自訂尺寸，應在 `image_edit` 流程中讓 `63:57` 的 width/height 也接受 `width`/`height` 參數。

### 🔴 問題 2：ImageCompressor 輸出到 ComfyUI 輸出目錄，而非自訂目錄

**位置：** workflow template 第 40 行
```json
"output_prefix": "compressed_",
"output_path": ""
```

**分析：**
- `output_path` 為空字串時，ComfyUI 會使用自己的預設輸出目錄
- 圖片下載端點 `/view` 預設從 ComfyUI 的 `output/` 目錄讀取
- 但 plugin 在 `_poll_for_result()` 時只取第一張圖片，假設是最終輸出
- 若 ComfyUI 有其他之前的圖片殘留，可能取到錯誤的圖片

**建議：** 讓 `output_path` 明確指向 `COMFY_OUTPUT_DIR`，並確保只取最新一張圖。

### 🟡 問題 3：image_edit workflow 的負向提示詞被設為空

**位置：** workflow template 第 63:56 行
```json
"class_type": "ConditioningZeroOut"
```

**分析：**
- `ConditioningZeroOut` 將條件化向量全部歸零，等同於「無負向提示詞」
- 正確的 negative prompt 應透過 `conditioning` 節點傳入，而非全部歸零
- 這導致生成結果完全依賴正向 prompt，無法抑制不需要的元素

**建議：** 若要支援負向提示詞，需新增一個 `CLIPTextEncode` 節點處理負向 prompt，並接到 `KSampler` 的 negative 端。

### 🟡 問題 4：無論 text_to_image 或 image_edit，都只能回傳一張圖

**位置：** `_poll_for_result()` 第 130 行
```python
if "images" in node_output and node_output["images"]:
    result_data = node_output
    break
```

**分析：**
- 取到第一個有 images 的 node 就 break，忽略後續輸出
- 若 workflow 輸出多張圖（batch > 1），只能拿到第一張
- `image_edit` 的 batch_size = 1，影響較小
- 但 `text_to_image` 的 `EmptyFlux2LatentImage` 也只有 batch=1

### 🟡 問題 5：輪詢時無 exponential backoff

**位置：** `_poll_for_result()` 第 154 行
```python
time.sleep(2)  # 固定 2 秒
```

**分析：**
- ComfyUI 生成一張圖可能需要 10 秒到 5 分鐘
- 固定 2 秒輪詢在高負載時可能造成 ComfyUI API 負擔
- 可考慮 2/4/8/16 秒的 exponential backoff

### 🟢 問題 6：除錯模式預設關閉

**位置：** `__init__.py` 第 26 行
```python
debug_mode = os.getenv("COMFY_WORKFLOW_DEBUG", "false").lower() == "true"
```

**分析：**
- 預設為 WARNING 等級，普通錯誤不會輸出日誌
- 若 ComfyUI 連線失敗，agent 只能從 tool 回傳的 JSON 判斷原因
- 建議在文件說明如何啟用 debug 模式

---

## 六、兩個 Template 之間的差異對照

| 維度 | T2I（node 77） | I2I（node 63:57） |
|------|---------------|-------------------|
| Latent 來源 | EmptyFlux2LatentImage（純噪聲） | 讀取上傳圖片 + VAEEncode |
| 去噪程度 | denoise=1.0（全去噪） | denoise=0.85（保留主體） |
| 參考機制 | 無 | ReferenceLatent（保留主體） |
| Prompt 節點 | 67（正向） + 76（全零負向） | 7（正向） + 63:56（全零負向） |
| ImageResize | 無 | ImageResizeKJv2（符合 height 參數） |
| 圖片尺寸 | 由 77 節點設定（width/height） | 由 63:49 GetImageSize 決定 |
| 固定 seed | 447638775894178 | 988841947314523 |

---

## 七、依賴關係圖（Model / VAE / CLIP）

```
共享資源（兩個 workflow 相同）：
├── CLIP:     qwen_3_8b_fp8mixed.safetensors  (type: flux2)
├── VAE:      flux2-vae.safetensors
└── Model:    flux2/snofsSexNudesAndOtherFunStuff_distilledV12Fp8.safetensors (fp8_e4m3fn)
```

**硬編碼的問題：** 模型路徑寫死在 workflow JSON 中，無法透過環境變數動態切換。若要更換模型，需直接修改 template JSON。

---

## 八、總結與改進建議

### 現有優點

1. **架構清晰**：Plugin 註冊模式標準，程式碼組織良好
2. **多格式支援**：同時支援本地檔案（`file://`）和 HTTP URL
3. **Polling 機制合理**：600 秒超時 + 每 2 秒輪詢，兼顧即時性和穩定性
4. **錯誤處理**：try/catch 包裹主要邏輯，回傳結構化 JSON

### 優先改進項目

1. **修復 width 參數缺失** — image_edit 應同時設定 width 和 height
2. **新增 negative prompt 支援** — 讓 KSampler 的 negative 端真正接收負向條件
3. **動態模型載入** — 將模型路徑從 JSON 抽出為環境變數
4. **除錯模式改為預設開啟或提高日誌等級** — 方便排查問題
5. **支援多圖輸出** — 目前只能取第一張圖

---

## 相關頁面

- [[concepts/safe-execution-workflow]] — Agent 安全執行工作流（本 plugin 分析屬於工具測試範疇）
- [[entities/skills/safe-execution-workflow/SKILL.md]] — Agent 操作版
