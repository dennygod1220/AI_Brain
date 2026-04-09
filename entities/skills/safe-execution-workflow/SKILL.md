---
name: safe-execution-workflow
category: productivity
description: 安全執行工作流 — 終端指令輸出防護、工具錯誤重試防護、錯誤訊息摘要防護，三層合一
tags: [safe-execution, tool-error, output-log, error-sanitizer, workflow]
created: 2026-04-09
---

# Safe Execution Workflow（安全執行工作流）

## 目的

防止模型在執行任務時因三種原因爆掉 Context Window：

1. **終端機指令輸出太大** → 寫日誌，切片讀取
2. **工具錯誤重試迴圈** → 設定上限，果斷中止
3. **錯誤訊息本身太長** → 萃取摘要，避免模型被錯誤訊息撐爆

---

## 日誌目錄結構

```
.hermes/logs/
├── execute_log/
│   └── {YYYY-MM-DD}.log          ← 每日執行日誌（單行摘要）
├── output_cache/
│   └── {YYYYMMDD_HHMMSS}.log     ← 完整輸出（結果太大時）
└── error_cache/
    └── {YYYYMMDD_HHMMSS}.log     ← 完整錯誤訊息（太長時）
```

> 每次新 session 第一次執行終端指令前，確保這些目錄存在：
> `mkdir -p .hermes/logs/execute_log .hermes/logs/output_cache .hermes/logs/error_cache`

---

## 第一章：Safe Terminal Execution（終端指令輸出防護）

### 觸發時機

以下情況**必須**將輸出寫入 `output_cache/`，不得直接輸出：

- `find`, `ls -la`, `tree`, `rg`, `grep` 等搜尋指令
- `pip install`, `npm install`, `apt install` 等套件安裝
- 執行 Python/Shell 腳本（非 hello-world 等極短輸出）
- `curl`, `wget` 請求 API 或下載檔案
- `git status`, `git diff`, `git log` 等版本控制指令
- `ps aux`, `htop`, `df -h` 等系統監控指令
- 任何輸出可能超過 20 行的指令

### 執行格式

```bash
# Step 1: 確保目錄
mkdir -p .hermes/logs/execute_log .hermes/logs/output_cache .hermes/logs/error_cache

# Step 2: 執行並寫日誌（產生日誌檔名）
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Step 3: 執行指令，寫入 output_cache
你的指令 > .hermes/logs/output_cache/${TIMESTAMP}.log 2>&1
EXIT_CODE=$?

# Step 4: 寫摘要到 execute_log
if [ $EXIT_CODE -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [EXEC] 你的指令 → output_cache/${TIMESTAMP}.log" >> .hermes/logs/execute_log/$(date +%Y-%m-%d).log
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] 你的指令 → output_cache/${TIMESTAMP}.log (exit $EXIT_CODE)" >> .hermes/logs/execute_log/$(date +%Y-%m-%d).log
fi
```

### 讀取結果

| 情境 | 指令 |
|------|------|
| 想看執行結果（前段） | `head -n 30 .hermes/logs/output_cache/{時間戳}.log` |
| 想看執行結果（前 100 行） | `head -n 100 .hermes/logs/output_cache/{時間戳}.log` |
| 想看完整日誌 | `cat .hermes/logs/output_cache/{時間戳}.log` |
| 搜尋特定關鍵字 | `grep "關鍵字" .hermes/logs/output_cache/{時間戳}.log` |

### 允許直接輸出例外

- 純文字短回覆確認（如 `pwd`, `date`, `whoami`）
- 單行簡單狀態查詢
- 已確定輸出極短（≤5 行）的指令

---

## 第二章：Tool Error Guard（工具重試迴圈防護）

### 觸發時機

當工具（tool）呼叫失敗或出錯時。

### 核心原則

> **任何工具失敗時，永遠問自己：「我應該重試、放棄、還是換方法？」**

### 五層防護

#### Layer 1：Retry Cap（單工具重試上限）

```
同一個工具，最多重試 3 次（含第一次呼叫）
```

- 每次重試前，**必須更換參數或修正錯誤**，而非用同樣的參數再次呼叫
- 若同一工具連續失敗 3 次，**果斷放棄該工具**，不再重試

#### Layer 2：Loop Detection（迴圈偵測）

```
連續 3 次同類錯誤 → 強制停止重試
累計 5 次任何工具失敗 → 回報用戶，不再嘗試
```

**同類錯誤的定義：**
- 同一工具 + 同一錯誤訊息
- 同一工具 + 相似錯誤訊息（僅參數不同）

#### Layer 3：Early Abort（提前中止條件）

**遇到以下任一條件，立刻中止並回報：**

| 條件 | 動作 |
|------|------|
| 同一工具連續 3 次失敗 | 放棄該工具，進入 Fallback |
| 累計 5 次任何工具失敗 | 回報用戶：「已嘗試多種方法但未能成功」 |
| 錯誤訊息包含 `Permission denied` | 立刻中止，不重試 |
| 錯誤訊息包含 `Not found` 且路徑已確認正確 | 立刻中止，不重試 |
| 錯誤訊息包含 `timeout` | 重試一次，若再 timeout → 放棄 |
| 錯誤訊息包含 `Out of memory` | 立刻中止，不重試 |

#### Layer 4：Fallback Strategy（替代策略）

當主要工具失敗時，按以下順序嘗試備援：

| 主要工具 | 備援工具 1 | 備援工具 2 |
|----------|-------------|-------------|
| `mcp_terminal` | `mcp_execute_code` | 回報用戶 |
| `mcp_read_file` | `mcp_terminal` (cat/head) | 回報用戶 |
| `mcp_search_files` | `mcp_terminal` (find/grep) | 回報用戶 |
| `mcp_write_file` | `mcp_terminal` (tee/heredoc) | 回報用戶 |
| `mcp_browser_navigate` | 回報用戶（無備援） | — |

#### Layer 5：Token Budget（Token 預算）

```
當接近 max_token 上限時，停止重試，果斷回報
```

- 對話已消耗 > 80% max_token → 停止所有重試
- 剩餘可用 token < 500 → 停止所有重試

**Token 緊縮時的輸出原則：**

```
❌ 不要：詳細分析錯誤原因（浪費 token）
✅ 要：   「工具執行失敗，原因：[錯誤]。請指示下一步。」
```

---

## 第三章：Tool Error Sanitizer（錯誤訊息摘要防護）

### 觸發時機

工具返回的錯誤訊息本身太長時。

> **長度的定義：**
> - 錯誤訊息總行數 > 10 行
> - 或錯誤訊息總長度 > 500 字元

### 執行流程

```
Step 1: 工具返回錯誤（假設太長）
    ↓
Step 2: 萃取錯誤摘要（見下方規則）
    ↓
Step 3: 完整錯誤寫入 error_cache/
    ↓
Step 4: 摘要寫入 execute_log/
    ↓
Step 5: 將摘要餵給模型（不超過 10 行）
```

### 萃取規則

```
❌ 從摘要中移除：
   - 完整 stack trace（可能數百行）
   - 重複的錯誤訊息
   - 二進制 hex dump
   - 完整 JSON error response
   - 詳細的記憶體位址、指標資訊

✅ 保留在摘要中：
   - 錯誤類型（如：FileNotFoundError, PermissionError, Timeout）
   - 發生在哪個工具或檔案
   - 關鍵錯誤訊息（第一行或前 3 行）
   - 發生的行號（如果有）
```

### 摘要格式範例

```
錯誤類型：FileNotFoundError
工具：mcp_read_file
路徑：/path/to/missing_file.txt
原因：No such file or directory
（完整錯誤已保存至 error_cache/20260409_103018.log）
```

### 寫入日誌

```bash
# 完整錯誤寫入 error_cache
echo "$FULL_ERROR" > .hermes/logs/error_cache/${TIMESTAMP}.log

# 摘要寫入 execute_log
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [SANITIZE] ${TOOL_NAME}: ${ERROR_TYPE} (${ERROR_LINES} lines) → error_cache/${TIMESTAMP}.log" >> .hermes/logs/execute_log/$(date +%Y-%m-%d).log
```

---

## 第四章：execute_log 日誌格式規範

所有摘要統一寫入 `execute_log/{YYYY-MM-DD}.log`：

```
[2026-04-09 10:30:15] [EXEC]    pip install requests → output_cache/20260409_103015.log
[2026-04-09 10:30:18] [ERROR]   mcp_read_file: FileNot found
[2026-04-09 10:30:18] [SANITIZE] error (38 lines) → error_cache/20260409_103018.log
[2026-04-09 10:30:19] [RETRY]   attempt 2/3: mcp_terminal
[2026-04-09 10:30:20] [ABORT]   loop detected: same tool 3x
[2026-04-09 10:30:21] [FALLBACK] switch to mcp_execute_code
```

| 標籤 | 意義 |
|------|------|
| `[EXEC]` | 指令執行成功 |
| `[ERROR]` | 指令執行失敗 |
| `[SANITIZE]` | 錯誤訊息已萃取摘要 |
| `[RETRY]` | 正在重試工具 |
| `[ABORT]` | 達到中止條件 |
| `[FALLBACK]` | 切換到備援工具 |
| `[SUCCESS]` | 任務完成 |

---

## 陷阱與注意事項

1. **千萬不要用同樣的參數重試** — 這是死循環的根源
2. **千萬不要 cat 大日誌檔** — 用 `head` / `tail` 切片
3. **不要假設網路問題會自己消失** — timeout 重試一次就該停了
4. **不要假設錯誤是暫時的** — 除非明確知道原因，否則視為永久性錯誤
5. **用戶說「繼續」才繼續** — 在 Early Abort 之後，必須等用戶明確指示
6. **Fallback 是新的開始** — 切換工具時，retry cap 重置為 1

---

## 標準回報格式（回報用戶時）

```
[工具執行失敗]
工具：<工具名稱>
錯誤類型：<錯誤類型>
摘要：<萃取後的摘要，≤10 行>
完整錯誤：<error_cache/{時間戳}.log>
已嘗試：<次數>
建議：<下一步可以做什麼，或直接請用戶指示>
```

---

## 驗證步驟

完成此 Skill 後，進行以下測試：

```
1. 故意呼叫一個不存在的檔案讀取
   → 預期：Sanitizer 萃取摘要，寫入 error_cache/

2. 故意呼叫一個會 timeout 的指令
   → 預期：重試 1 次，若再 timeout 放棄，寫入 execute_log/

3. 故意呼叫一個會失敗 3 次的工具
   → 預期：3 次後自動放棄，進入 Fallback
```

---

## 相關頁面

- [[concepts/safe-execution-workflow]] — 人類概念版（給 AI Brain 閱讀）
