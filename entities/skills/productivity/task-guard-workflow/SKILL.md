---
name: task-guard-workflow
category: productivity
description: Profile-Aware 執行階段防護工作流 — 專注於日誌切片、錯誤處理、Early Abort 與 Fallback 策略。日誌統一存在 `$HOME/.hermes/logs/task-guard/<Profile>/`。
version: 3.0.0
author: Hermes Agent
license: MIT
created: 2026-04-13
updated: 2026-04-14
sources: [hermes-skill, raw/articles/Safe Mission Workflow (狀態機與安全執行工作流)]
metadata:
  hermes:
    tags: [Safe-Execution, Tool-Error, Workflow, Log-Management]
    related_skills: [writing-plans]
---

> **注意：** 本 workflow **不包含任務規劃**。複雜任務請先使用 `writing-plans` skill 拆解成 bite-sized tasks，再依本 workflow 執行。

# Task Guard Workflow

## 路徑結構

> **⚠️ 動態路徑守則：** 所有日誌與快取，**絕對不可**寫入 `.hermes/profiles/`（那是 Hermes Agent 自身使用的），必須統一放在：

```
$HOME/.hermes/logs/task-guard/<你的_Profile_名稱>/
```

目錄結構：
- `execute_log/` — 每日執行摘要（`YYYY-MM-DD.log`）
- `output_cache/` — 終端指令輸出切片
- `error_cache/` — 錯誤訊息萃取備份

---

## 核心目的

這套工作流旨在解決 Agent 執行任務時的三大痛點：

1. **記憶體爆掉**：透過日誌切片、錯誤萃取與嚴格的重試上限，保護本地模型 Token 預算。
2. **實例資料污染 (Profile-Aware)**：確保所有日誌與狀態檔，嚴格隔離在各自 Profile 的專屬目錄中。
3. **錯誤處理混亂**：統一的 Early Abort 條件表與 Fallback 策略，避免盲目重試。

---

## 🛡️ 第一章：Safe Terminal Execution（終端指令輸出防護）

以下情況**必須**將輸出寫入 `output_cache/`，不得直接輸出到聊天視窗：

- `find`, `ls -la`, `rg`, `grep` 等搜尋指令
- `curl`, `wget` 請求 API
- 任何預期輸出可能超過 20 行的動作

**安全執行格式：**

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PROFILE_DIR="$HOME/.hermes/logs/task-guard/你的_profile_名稱"
mkdir -p ${PROFILE_DIR}/execute_log ${PROFILE_DIR}/output_cache ${PROFILE_DIR}/error_cache

你的指令 > ${PROFILE_DIR}/output_cache/${TIMESTAMP}.log 2>&1
EXIT_CODE=$?

echo "[$(date '+%Y-%m-%d %H:%M:%S')] [EXEC] 指令摘要 → output_cache/${TIMESTAMP}.log (exit $EXIT_CODE)" >> ${PROFILE_DIR}/execute_log/$(date +%Y-%m-%d).log
```

_讀取結果時，永遠優先使用 `head -n 50` 或 `jq` 解析，嚴禁直接 `cat` 大檔案。_

### 允許直接輸出例外

- `pwd`, `date`, `whoami` 等純文字短回覆
- 單行簡單狀態查詢
- 已確定輸出極短（≤5 行）的指令

---

## 🛡️ 第二章：Tool Error Guard（工具重試迴圈防護）

工具失敗時，嚴格遵守「五層防護」，**嚴禁盲目重試**：

### Layer 1：Retry Cap
同工具最多重試 3 次（含第一次）。每次**必須更換參數**，嚴禁用同樣的參數重試。

### Layer 2：Loop Detection
連續 3 次同類錯誤（同一工具 + 同一或相似錯誤訊息）→ 強制停止。

### Layer 3：Early Abort（加強版）

遇到以下任一條件，立刻中止：

| 條件 | 動作 |
|------|------|
| `Permission denied` | 立刻中止，不重試 |
| `Not found` 且路徑已確認正確 | 立刻中止，不重試 |
| `Out of memory` | 立刻中止，不重試 |
| `timeout` | 重試一次，若再 timeout → 放棄 |
| 同一工具連續 3 次失敗 | 放棄該工具，進 Fallback |
| 累計 5 次任何工具失敗 | 回報用戶，不再嘗試 |

### Layer 4：Fallback Strategy

| 主要工具 | 備援工具 1 | 備援工具 2 |
|----------|-------------|-------------|
| `terminal` | `execute_code` | 回報用戶 |
| `read_file` | `terminal` (cat/head) | 回報用戶 |
| `search_files` | `terminal` (find/grep) | 回報用戶 |
| `write_file` | `terminal` (tee/heredoc) | 回報用戶 |
| `browser_navigate` | 回報用戶（無備援） | — |

### Layer 5：Token Budget
對話消耗 > 80% max_token，或剩餘可用 token < 500 → 停止所有重試。

---

## ✂️ 第三章：Tool Error Sanitizer（錯誤訊息摘要防護）

錯誤訊息太長（> 10 行或 > 500 字元）時：

1. **萃取摘要**：保留錯誤類型、工具名稱、關鍵第一行。移除 Stack trace、重複訊息、二進制 hex dump、完整 JSON error response。
2. **專屬備份**：

```bash
PROFILE_DIR="$HOME/.hermes/logs/task-guard/你的_profile_名稱"
echo "$FULL_ERROR" > ${PROFILE_DIR}/error_cache/${TIMESTAMP}.log
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [SANITIZE] ${TOOL_NAME}: ${ERROR_TYPE} → error_cache/${TIMESTAMP}.log" >> ${PROFILE_DIR}/execute_log/$(date +%Y-%m-%d).log
```

3. **餵給模型**：只允許閱讀 10 行以內的萃取摘要。

---

## execute_log 日誌格式

所有摘要統一寫入 `${PROFILE_DIR}/execute_log/{YYYY-MM-DD}.log`：
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

## Pitfalls

1. **千萬不要用同樣的參數重試** — 這是死循環的根源
2. **千萬不要 cat 大日誌檔** — 用 `head` / `tail` 切片
3. **不要假設網路問題會自己消失** — timeout 重試一次就該停了
4. **不要假設錯誤是暫時的** — 除非明確知道原因，否則視為永久性錯誤
5. **用戶說「繼續」才繼續** — 在 Early Abort 之後，必須等用戶明確指示
6. **Fallback 是新的開始** — 切換工具時，retry cap 重置為 1
7. **日誌路徑統一在 `$HOME/.hermes/logs/task-guard/<Profile>/`** — 嚴禁寫入 `.hermes/profiles/`（那是 Hermes Agent 自身使用的）
8. **`patch` 的 `old_string` 範圍過大會意外覆蓋相鄰內容** — 執行前先 `read_file` 確認精確範圍，堅守「最小精確匹配」原則；若不確定，先单独 `read_file` 確認精確行號再用

---

## 驗證步驟

1. 故意呼叫一個不存在的檔案讀取 → 預期：Sanitizer 萃取摘要，寫入 error_cache/
2. 故意呼叫一個會 timeout 的指令 → 預期：重試 1 次，若再 timeout 放棄
3. 故意呼叫一個會失敗 3 次的工具 → 預期：3 次後自動放棄，進 Fallback
