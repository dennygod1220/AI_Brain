---
name: task-guard-workflow
category: productivity
description: Profile-Aware 工業級任務執行工作流 — 結合實體狀態機、最終產出物(Artifact)與三層安全防護。加強版：更嚴格的日誌切片規則、增強的 Early Abort 條件表、完整的驗證流程。
version: 2.0.0
author: Hermes Agent
license: MIT
created: 2026-04-13
updated: 2026-04-13
sources: [hermes-skill, raw/articles/Safe Mission Workflow (狀態機與安全執行工作流)]
metadata:
  hermes:
    tags: [Safe-Execution, Tool-Error, State-Management, Workflow, Profile-Aware, Artifact]
    related_skills: []
---

# Task Guard Workflow（加強版）

## 核心目的

這套工作流旨在解決 Agent 執行複雜任務時的四大痛點：

1. **上下文失憶**：強制使用實體檔案追蹤進度，看著清單打勾，不忘記任務目標。
2. **記憶體爆掉**：透過日誌切片、錯誤萃取與嚴格的重試上限，保護本地模型 Token 預算。
3. **實例資料污染 (Profile-Aware)**：確保所有日誌與狀態檔，嚴格隔離在各自 Profile 的專屬目錄中。
4. **產出物遺失 (Artifact)**：強制將最終結果寫入實體報告，避免重要情報在對話紀錄中被洗掉。

---

## 📂 第一章：基礎建設與狀態管理 (Profile-Aware Planner)

> **⚠️ 動態路徑守則：** 所有的日誌與狀態，**絕對不可**寫入全域目錄，必須使用 `$HOME/.hermes/profiles/<你的Profile名稱>/` 作為根目錄。

### 1.1 目錄與狀態模板初始化 (Idempotent Setup)

每次收到新任務，在採取任何實際行動前，**必須**先執行以下腳本：

```bash
PROFILE_NAME="你的_profile_名稱"
PROFILE_DIR="$HOME/.hermes/profiles/${PROFILE_NAME}"

mkdir -p ${PROFILE_DIR}/logs/execute_log \
         ${PROFILE_DIR}/logs/output_cache \
         ${PROFILE_DIR}/logs/error_cache \
         ${PROFILE_DIR}/state \
         ${PROFILE_DIR}/artifacts

if [ ! -f "${PROFILE_DIR}/state/current_mission.md" ]; then
cat << 'EOF' > ${PROFILE_DIR}/state/current_mission.md
# 任務目標：[請在此填寫]

## 待辦清單 (Checklist)
- [ ] 步驟 1：(詳細說明你要用什麼工具做什麼事)
- [ ] 步驟 2：(詳細說明)

## 執行日誌 (Execution Log)
- (留白，用於記錄每次行動的關鍵結果或遭遇的重大錯誤)
EOF
fi
```

### 1.2 強制核對機制 (Read-Execute-Update Loop)

1. **行動前讀取**：呼叫工具前，先讀取 `current_mission.md`，確認自己在哪一步。
2. **完成後強制實體打勾**：成功完成後，**必須**使用工具真實修改 `current_mission.md`，將 `- [ ]` 改為 `- [x]`。不允許只在對話中口頭說已更新。
3. **異常中斷重啟**：若出錯觸發中止，將錯誤寫入該檔案。下次對話時，先讀取此檔案接續執行。

---

## 🛡️ 第二章：Safe Terminal Execution（終端指令輸出防護）

以下情況**必須**將輸出寫入 `output_cache/`，不得直接輸出到聊天視窗：

- `find`, `ls -la`, `rg`, `grep` 等搜尋指令
- `curl`, `wget` 請求 API
- 任何預期輸出可能超過 20 行的動作

**安全執行格式：**

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PROFILE_DIR="$HOME/.hermes/profiles/你的_profile_名稱"

你的指令 > ${PROFILE_DIR}/logs/output_cache/${TIMESTAMP}.log 2>&1
EXIT_CODE=$?

echo "[$(date '+%Y-%m-%d %H:%M:%S')] [EXEC] 指令摘要 → logs/output_cache/${TIMESTAMP}.log (exit $EXIT_CODE)" >> ${PROFILE_DIR}/logs/execute_log/$(date +%Y-%m-%d).log
```

_讀取結果時，永遠優先使用 `head -n 50` 或 `jq` 解析，嚴禁直接 `cat` 大檔案。_

### 允許直接輸出例外

- `pwd`, `date`, `whoami` 等純文字短回覆
- 單行簡單狀態查詢
- 已確定輸出極短（≤5 行）的指令

---

## 🚫 第三章：Tool Error Guard（工具重試迴圈防護）

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

## ✂️ 第四章：Tool Error Sanitizer（錯誤訊息摘要防護）

錯誤訊息太長（> 10 行或 > 500 字元）時：

1. **萃取摘要**：保留錯誤類型、工具名稱、關鍵第一行。移除 Stack trace、重複訊息、二進制 hex dump、完整 JSON error response。
2. **專屬備份**：

```bash
PROFILE_DIR="$HOME/.hermes/profiles/你的_profile_名稱"
echo "$FULL_ERROR" > ${PROFILE_DIR}/logs/error_cache/${TIMESTAMP}.log
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [SANITIZE] ${TOOL_NAME}: ${ERROR_TYPE} → logs/error_cache/${TIMESTAMP}.log" >> ${PROFILE_DIR}/logs/execute_log/$(date +%Y-%m-%d).log
```

3. **餵給模型**：只允許閱讀 10 行以內的萃取摘要。

---

## 📦 第五章：任務收尾與產出物（Artifact）

當 `current_mission.md` 中所有步驟都打勾完成後，**必須**將最終結果寫入：

```
${PROFILE_DIR}/artifacts/任務名稱_$(date +%Y%m%d).md
```

嚴禁只在對話中口頭回報。

---

## 📢 第六章：標準回報格式

```markdown
### 任務狀態匯報
- **當前進度**：[簡述 current_mission.md 中打勾的狀態]
- **遭遇狀況**：[成功完成 / 或在哪個步驟卡住]
- **最終產出物**：[若已完成，附上 artifacts/ 檔案路徑]

（若發生錯誤則附上以下資訊）
- **失敗工具**：<工具名稱>
- **錯誤摘要**：<萃取後的摘要，≤10 行>
- **日誌位置**：<${PROFILE_DIR}/logs/error_cache/{時間戳}.log>
- **已嘗試次數**：<次數>

**建議與下一步**：<請用戶指示是否更換策略>
```

---

## execute_log 日誌格式

所有摘要統一寫入 `${PROFILE_DIR}/logs/execute_log/{YYYY-MM-DD}.log`：

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
7. **所有路徑必須 Profile-Aware** — 嚴禁寫入全域目錄

---

## 驗證步驟

1. 故意呼叫一個不存在的檔案讀取 → 預期：Sanitizer 萃取摘要，寫入 error_cache/
2. 故意呼叫一個會 timeout 的指令 → 預期：重試 1 次，若再 timeout 放棄
3. 故意呼叫一個會失敗 3 次的工具 → 預期：3 次後自動放棄，進入 Fallback
