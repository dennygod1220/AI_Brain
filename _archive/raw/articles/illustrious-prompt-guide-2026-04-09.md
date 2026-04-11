# Illustrious XL Prompt 撰寫與優化完全指南

> 資料來源：[illustrious-xl.ai](https://www.illustrious-xl.ai) 官方網站、Blog、Updates
> 更新時間：2026-04-09
> 模型版本涵蓋：v1.0 ~ v3.6

---

## 1. 模型版本與選擇

### 官方模型系列命名對照

| 舊名稱 | 新名稱（易懂） | 特性 | 推薦用途 |
|--------|--------------|------|---------|
| **v1.0** | Legacy | 原始基礎模型 | 極簡提示詞用戶 |
| **v1.1** | Legacy | 角色理解小幅提升 | 人物創作 |
| **v2.0 Base** | Base | 穩定通用，1536 原生解析度 | 訓練 LoRA 的首選 |
| **v2.0 Aesthetic** | Refined | 色彩/構圖軟升級 | 美學導向創作 |
| **v3.0 EPS** | Creative | epsilon 訓練，風格化輸出 | 插畫風格生成 |
| **v3.0 VPred** | Expressive | velocity 預測，複合理解強 | 複雜提示詞 |
| **v3.5 VPred** | Expressive+ | 修正 VPred 色彩崩潰問題 | 高精度提示詞遵循 |
| **v3.6** | Creative+ | 增強創意輸出，一致性提升 | 商業插畫 |

### 選擇原則

```
✅ 複雜提示詞 + 自然語言 → Expressive / Expressive+
✅ 極簡提示詞 + 美學品質 → Creative / Creative+
✅ 訓練 LoRA / 微調 → 務必使用 Base 模型（Aesthetic 模型極難訓練）
✅ 通用場景 → Base 或 Refined 即可
```

---

## 2. 核心 Prompt 策略

### 2.1 短提示詞增強（Tag Booster + Mood Enhancer）

Illustrious 官方提供了 **Text-Enhancer** 系統，包含兩個元件：

#### Tag Booster（TIPO 框架）
- 將稀疏的標籤轉換為豐富的提示詞
- 支援雙向轉換：標籤 ↔ 自然語言
- **原理**：對齊模型訓練數據的分佈
- **範例**：
  - 輸入：`autumn forest`
  - 輸出：`autumn forest, golden sunlight, falling leaves, high detail, masterpiece, warm color palette`

#### Mood Enhancer
- 用於自然語言豐富化
- 最小輸入 → 詳細情感描述
- 成本低、延遲小（KV caching 優化）

### 2.2 提示詞結構（官方建議）

基於官方範例，Illustrious 的最佳提示詞結構：

```
[主體描述] + [風格/藝術家] + [光照/氛圍] + [品質標籤] + [技術參數]
```

#### 官方範例 1：人物角色（高解析度）
```
The image features two characters, each with distinct black and white outfits,
standing back-to-back. The character on the left wears a white coat with black
accents, black pants, and boots, and is chained at the wrists and ankles.
The character on the right is dressed in a black coat with white accents,
black pants, and boots, also chained at the wrists and ankles. Both characters
have spiked black hair and wield large key-shaped weapons.
```

#### 官方範例 2：場景生成
```
A breathtaking scene unfolds with two girls standing together, a striking
contrast in both appearance and demeanor. The girl on the left has flowing,
deep red hair, cascading in soft waves down her shoulders, with strands
illuminated by the ambient light. Her eyes are a mesmerizing shade of sea-black...
```

#### 官方範例 3：指定光照與氛圍
```
twilight sky over a vast ocean, where the last remnants of the sun cast a
golden glow across the waves, mixing with the incoming darkness. The wind
rustles through their hair as they stand close
```

### 2.3 推薦品質標籤

```
✅ masterpiece              # 品質提升
✅ best quality             # 最高品質
✅ high detail              # 高細節
✅ absurdres                 # 高解析度
✅ depth of field           # 景深效果
✅ absurdres, wallpaper     # 壁紙品質
✅ wlop, quasarcake         # 藝術家風格參考
✅ dynamic lighting          # 動態光照
✅ extremely aesthetic       # 極致美學
```

### 2.4 負面提示詞（Negative Prompt）

官方範例使用的負面提示詞：
```
worst quality, low quality, lowres, low details, bad quality,
poorly drawn, bad anatomy, multiple views, bad hands, blurry,
artist signature
```

---

## 3. 技術參數建議

### 3.1 解析度優化

| 版本 | 原生解析度 | 推薦尺寸 |
|------|-----------|---------|
| v1.x | ~1024 | 896x1152, 1024x1024 |
| **v2.x** | **1536 原生** | **1248x1824, 1152x1536** |
| v3.x | 256~2048 | 任意尺寸，最高支援 2048 |

> **v2.0 的核心改進**：1536 原生解析度訓練，解決 512x512 偽影與 1024x1536 不穩定問題。

### 3.2 Sampler 與 CFG 設置

| 參數 | 官方建議值 |
|------|-----------|
| Sampler | **Euler a**（官方主要展示用） |
| Schedule type | Automatic |
| **CFG Scale** | **7.5**（官方主要展示值） |
| Steps | 28（官方展示值） |

> ⚠️ **v-pred 模型的顏色問題**：
> - v3.0-vpred：默認過飽和（58% 像素 #FFFFFF 白色崩潰）
> - v3.5-vpred：修正為中間色調，色彩控制移至特定 tokens

### 3.3 進階技巧：FFT 分析提示

官方使用 Fast Fourier Transform 分析模型對提示詞的遵循程度，適用於測試複雜提示詞：
- 低頻信號 = 整体构图
- 高頻信號 = 細節與紋理

---

## 4. 自然語言理解能力

### 4.1 v3.x 的重大突破

**v3.5-vpred** 展示了前所未有的自然語言理解能力：

```
✅ "left is black, right is red"  → 成功執行左右色彩分離
✅ "left side is red hair, right side is blue hair"  → 成功
✅ 424 tokens 複雜提示詞 → 成功遵循
```

### 4.2 複雜提示詞測試案例

**424 tokens 超長提示詞成功率**：
- v3.0 epsilon：~92%（23/25）
- v3.0 vpred：過飽和但部分遵循
- v3.5 vpred：中間色調 + 良好遵循

---

## 5. LoRA 訓練兼容性

| 模型類型 | LoRA 訓練 | 說明 |
|---------|----------|------|
| **Base 模型** | ✅ 完全支援 | **官方推薦用於訓練** |
| Aesthetic 模型 | ⚠️ 極難訓練 | 官方：「Good luck with them」 |
| v3.x VPred | ⚠️ PEFT 不穩定 | 正在解決中 |

### LoRA 應用範例（官方展示）
```
2girls, standing, side-by-side, crazy mita, yuitsuka inori,
<lora:new_chars:1>, smiling, masterpiece, pixel art
```

---

## 6. 官方 Prompt 模板總結

### 模板 A：人物插畫
```
[詳細外貌描述：髮色、眼色、表情、穿著],
[姿勢/動作],
[背景描述],
[光照描述],
[品質標籤],
[藝術家風格（可選）]
```

### 模板 B：場景/氛圍
```
[場景類型],
[主要元素],
[光線/天氣/時間],
[色彩氛圍],
[視角],
[品質標籤],
[技術參數]
```

### 模板 C：角色對比
```
[角色 A 詳細描述],
[角色 B 詳細描述],
[對比/互動],
[背景],
[整體氛圍],
[品質標籤]
```

---

## 7. 與 FLUX 的比較

| 維度 | Illustrious XL | FLUX Schnell |
|------|---------------|-------------|
| 提示詞遵循 | ✅ 良好 + 插畫美學 | ✅ 良好 |
| 插畫品質 | ✅ 強項 | ⚠️ 較弱 |
| 風格多樣性 | ✅ 強項 | ⚠️ 一般 |
| 自然語言理解 | v3.x 顯著提升 | ✅ 原生支援 |
| 1536+ 解析度 | ✅ v2 原生 | 需後處理 |

> 官方結論：「better prompt adherence (alignment) with illustration-related functionalities. Not just aesthetic, Not just stupid compute.」

---

## 8. 實用工具與資源

| 資源 | 連結 |
|------|------|
| 官方生成平台 | https://www.illustrious-xl.ai/image-generate |
| 模型下載 | HuggingFace: OnomaAIResearch/Illustrious-XL-v2.0 |
| 官方 Blog | https://www.illustrious-xl.ai/blog |
| Tech Blog | https://www.illustrious-xl.ai/blog（Tech Blog 分類） |
| Discord 社群 | 官方導航列有連結 |

---

## 9. 快速參考卡片

```
┌─────────────────────────────────────────────────────────┐
│                  ILLUSTRIOUS PROMPT 速查                 │
├─────────────────────────────────────────────────────────┤
│  基本結構：主體 → 風格 → 光照 → 品質 → 參數              │
│  解析度：v2+ → 優先 1248x1824 或 1536x1536              │
│  Sampler：Euler a（官方預設）                           │
│  CFG：7.5（官方預設）                                   │
│  Steps：28（官方展示）                                   │
│  負面提示詞：worst quality, low quality, bad anatomy    │
│  訓練用：務必選 Base 模型                               │
│  複雜提示詞：選 Expressive / Expressive+                │
│  美學品質：選 Creative / Creative+                       │
│  必加標籤：masterpiece, best quality, high detail       │
└─────────────────────────────────────────────────────────┘
```

---

## 10. 延伸閱讀

- [Illustrious 官方 Blog](https://www.illustrious-xl.ai/blog)
- [Model Series 更新說明](https://www.illustrious-xl.ai/updates/20)
- [Text-Enhancer 技術詳解](https://www.illustrious-xl.ai/blog/15)
- [v3.0-v3.5 技術分析](https://www.illustrious-xl.ai/blog/8)
- [v2.0 訓練基礎模型介紹](https://www.illustrious-xl.ai/blog/7)
- HuggingFace: https://huggingface.co/OnomaAIResearch/Illustrious-XL-v2.0
