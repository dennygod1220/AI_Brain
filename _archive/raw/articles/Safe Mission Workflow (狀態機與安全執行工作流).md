## name: safe-mission category: productivity description: Profile-Aware 工業級任務執行工作流 — 結合實體狀態機、最終產出物(Artifact)與三層安全防護。⚠️ 基礎版（已被 entities/skills/productivity/task-guard-workflow/SKILL.md v2.0.0 加強版取代） tags: [safe-execution, tool-error, state-management, workflow, planner, profile-aware] created: 2026-04-13 updated: 2026-04-13 related_skills: [task-guard-workflow]

# Safe Mission Workflow (狀態機與安全執行工作流)

## 🎯 核心目的

這套工作流旨在解決 Agent 執行複雜任務時的四大痛點：

1. **上下文失憶**：強制使用實體檔案追蹤進度，看著清單打勾，不忘記任務目標。
    
2. **記憶體爆掉**：透過日誌切片、錯誤萃取與嚴格的重試上限，保護本地模型 Token 預算。
    
3. **實例資料污染 (Profile-Aware)**：確保所有日誌與狀態檔，嚴格隔離在各自 Profile 的專屬目錄中。
    
4. **產出物遺失 (Artifact)**：強制將最終結果寫入實體報告，避免重要情報在對話紀錄中被洗掉。
    

## 📂 第一章：基礎建設與狀態管理 (Profile-Aware Planner)

> **⚠️ 動態路徑守則：** 你現在身處於獨立的 Profile 環境中。所有的日誌與狀態，**絕對不可**寫入全域目錄，必須使用 `$HOME/.hermes/profiles/<你的Profile名稱>/` 作為根目錄。

### 1.1 目錄與狀態模板初始化 (Idempotent Setup)

每次收到新任務，在採取任何實際行動前，**必須**先執行以下腳本，建立專屬架構與狀態模板：

```
# 1. 自動獲取你的 Profile 名稱
PROFILE_NAME="你的_profile_名稱"
PROFILE_DIR="$HOME/.hermes/profiles/${PROFILE_NAME}"

# 2. 建立專屬的日誌與狀態機目錄
mkdir -p ${PROFILE_DIR}/logs/execute_log ${PROFILE_DIR}/logs/output_cache ${PROFILE_DIR}/logs/error_cache ${PROFILE_DIR}/state ${PROFILE_DIR}/artifacts

# 3. 若狀態檔不存在，自動建立模板
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

1. **行動前讀取**：呼叫工具前，先讀取 `current_mission.md`，意識到自己在哪一步。
    
2. **完成後強制實體打勾**：成功完成後，**不允許只在對話中口頭說已更新**。你**必須**使用 `mcp_terminal` (透過 `sed`) 或 `mcp_write_file` 真實修改 `current_mission.md` 檔案，將 `- [ ]` 改為 `- [x]`。
    
3. **異常中斷重啟**：若出錯觸發中止，將錯誤寫入該檔案。下次對話時，先讀取此檔案接續執行。
    

## 🛡️ 第二章：Safe Terminal Execution (終端指令輸出防護)

以下情況**必須**將輸出寫入 `output_cache/`，不得直接輸出到聊天視窗：

- `find`, `ls -la`, `rg`, `grep` 等搜尋
    
- `curl`, `wget` 請求 API 或使用 `camofox` 抓取快照 / JSON (如 `@reddit_search`)
    
- 任何預期輸出可能超過 20 行的動作
    

**安全執行格式：**

```
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PROFILE_DIR="$HOME/.hermes/profiles/你的_profile_名稱"

# 執行指令並將輸出導向專屬快取
你的指令 > ${PROFILE_DIR}/logs/output_cache/${TIMESTAMP}.log 2>&1
EXIT_CODE=$?

# 寫摘要到專屬 execute_log
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [EXEC/ERROR] 指令摘要 → logs/output_cache/${TIMESTAMP}.log (exit $EXIT_CODE)" >> ${PROFILE_DIR}/logs/execute_log/$(date +%Y-%m-%d).log
```

_讀取結果時，永遠優先使用 `head -n 50` 或 `jq` 解析，嚴禁直接 `cat` 大檔案。_

## 🚫 第三章：Tool Error Guard (工具重試迴圈防護)

工具失敗時，嚴格遵守「五層防護」，**嚴禁盲目重試**：

1. **Retry Cap（上限）**：同工具最多重試 3 次。每次**必須更換參數**。
    
2. **Loop Detection（防死循環）**：連續 3 次同類錯誤 → 強制停止。
    
3. **Early Abort（提前中止）**：
    
    - 包含 `Permission denied`、`Out of memory`：立刻中止。
        
    - 包含 `timeout`：重試一次，若再 timeout 即放棄。
        
4. **Fallback Strategy（備援）**：失敗 3 次後，切換其他工具 (如 Python 腳本)。
    
5. **Token Budget（預算緊縮）**：連續失敗 5 次，停止嘗試，實體更新 `current_mission.md` 並回報。
    

## ✂️ 第四章：Tool Error Sanitizer (錯誤訊息摘要防護)

錯誤訊息太長（> 10 行或 > 500 字元）時：

1. **萃取摘要**：保留錯誤類型、工具名稱、關鍵第一行。移除 Stack trace。
    
2. **專屬備份**：
    

```
PROFILE_DIR="$HOME/.hermes/profiles/你的_profile_名稱"
# 完整錯誤寫入專屬 error_cache
echo "$FULL_ERROR" > ${PROFILE_DIR}/logs/error_cache/${TIMESTAMP}.log

# 摘要寫入專屬 execute_log
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [SANITIZE] ${TOOL_NAME}: ${ERROR_TYPE} → logs/error_cache/${TIMESTAMP}.log" >> ${PROFILE_DIR}/logs/execute_log/$(date +%Y-%m-%d).log
```

3. **餵給大腦**：只允許閱讀 10 行以內的「萃取摘要」。
    

## 📦 第五章：任務收尾與產出物 (Final Artifact)

當 `current_mission.md` 中所有的步驟都打勾完成後，你不能只口頭回報。

你**必須**將最終的研究結果、整理的表格或開發的程式碼，寫入專屬的產出目錄：

`${PROFILE_DIR}/artifacts/任務名稱_$(date +%Y%m%d).md`

## 📢 第六章：標準回報格式 (向用戶匯報)

任務完成或觸發中止時，請依照以下格式回報：

```
### 任務狀態匯報
- **當前進度**：[簡述 current_mission.md 中打勾的狀態]
- **遭遇狀況**：[成功完成 / 或在哪個步驟卡住]
- **最終產出物**：[若已完成，附上 artifacts/ 檔案路徑]

**(若發生錯誤則附上以下資訊)**
- **失敗工具**：<工具名稱>
- **錯誤摘要**：<萃取後的摘要，≤10 行>
- **日誌位置**：<${PROFILE_DIR}/logs/error_cache/{時間戳}.log>
- **已嘗試次數**：<次數>

**建議與下一步**：<請用戶指示是否更換策略>
```