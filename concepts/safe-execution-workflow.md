---
name: Safe Execution Workflow
description: 安全執行工作流 — Profile-Aware 狀態機 + 終端輸出防護 + 工具錯誤防護 + Artifact 產出，三層合一
version: 1.1.0
created: 2026-04-09
updated: 2026-04-13
type: concept
tags: [productivity, safe-execution, tool-error, output-log, error-sanitizer, workflow, state-machine, profile-aware, artifact]
sources: [hermes-skill, raw/articles/Safe Mission Workflow (狀態機與安全執行工作流)]
---

# Safe Execution Workflow（安全執行工作流）

## 背景

小模型（如 Gemma）在執行任務時容易因為三種原因爆掉 Context Window：

| 問題 | 原因 |
|------|------|
| 終端機指令輸出太大 | `ls -la`、`find` 等指令結果太多行 |
| 工具錯誤重試迴圈 | 工具失敗但不斷重試，直到 output/think max_token 爆掉 |
| 錯誤訊息本身太長 | 工具返回的錯誤含完整 stack trace，數百行直接餵給模型 |

本 workflow 將三種防護機制合併為一，模型只需載入一個 skill 就能得到完整防護。

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

---

## 第一章：Safe Terminal Execution（終端指令輸出防護）

**解決：** 終端機指令輸出太大，撐爆 Context Window。

**觸發時機：** 執行可能超過 20 行的指令時（`find`、`ls -la`、`pip install` 等）。

**方法：** 結果寫入 `output_cache/`，摘要寫入 `execute_log/`，用 `head` / `tail` / `grep` 切片讀取。

---

## 第二章：Tool Error Guard（工具重試迴圈防護）

**解決：** 小模型不知道何時該停，陷入重試死循環。

**觸發時機：** 工具呼叫失敗或出錯時。

**五層防護：**

| Layer | 機制 | 閾值 |
|-------|------|------|
| 1 | Retry Cap | 同一工具最多 3 次 |
| 2 | Loop Detection | 同一工具連續 3 次 / 累計 5 次 |
| 3 | Early Abort | Permission denied / Not found / OOM → 立刻停 |
| 4 | Fallback | 主要工具失敗 → 嘗試備援工具 |
| 5 | Token Budget | >80% max_token → 停止重試 |

**核心原則：**
> **任何工具失敗時，永遠問自己：「我應該重試、放棄、還是換方法？」**

---

## 第三章：Tool Error Sanitizer（錯誤訊息摘要防護）

**解決：** 錯誤訊息本身太長（stack trace 數百行），直接餵給模型會讓模型自己爆掉。

**觸發時機：** 錯誤訊息 > 10 行 或 > 500 字元。

**萃取規則：**

```
保留：
- 錯誤類型（FileNotFoundError, PermissionError, Timeout）
- 工具名稱或檔案路徑
- 關鍵訊息（前 3 行）
- 行號（如果有）

移除：
- 完整 stack trace
- 重複訊息
- Hex dump / JSON response
- 記憶體位址
```

---

## execute_log 日誌格式

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

## Profile-Aware 狀態機（Profile-Aware Planner）

每次收到新任務，**必須**先建立專屬架構與狀態模板（Profile-Aware）：

```
PROFILE_NAME="你的_profile_名稱"
PROFILE_DIR="$HOME/.hermes/profiles/${PROFILE_NAME}"

# 建立專屬目錄
mkdir -p ${PROFILE_DIR}/logs/execute_log ${PROFILE_DIR}/logs/output_cache \
         ${PROFILE_DIR}/logs/error_cache ${PROFILE_DIR}/state ${PROFILE_DIR}/artifacts

# 若狀態檔不存在，自動建立模板
if [ ! -f "${PROFILE_DIR}/state/current_mission.md" ]; then
cat << 'EOF' > ${PROFILE_DIR}/state/current_mission.md
# 任務目標：[請在此填寫]

## 待辦清單 (Checklist)
- [ ] 步驟 1：(詳細說明)
- [ ] 步驟 2：(詳細說明)

## 執行日誌 (Execution Log)
- (留白，用於記錄每次行動的關鍵結果)
EOF
fi
```

**Read-Execute-Update Loop：**
1. 行動前讀取 `current_mission.md`，意識到自己在哪一步
2. 完成後**強制實體打勾**（使用 `mcp_write_file` 將 `- [ ]` 改為 `- [x]`）
3. 若出錯中斷，將錯誤寫入該檔案，下次對話時先讀取接續執行

---

## Artifact 產出（任務收尾）

當所有步驟打勾完成後，**必須**將最終結果寫入實體報告：

```
${PROFILE_DIR}/artifacts/任務名稱_$(date +%Y%m%d).md
```

---

## 陷阱與注意事項

1. **千萬不要用同樣的參數重試** — 這是死循環的根源
2. **千萬不要 cat 大日誌檔** — 用 `head` / `tail` 切片
3. **不要假設網路問題會自己消失** — timeout 重試一次就該停了
4. **不要假設錯誤是暫時的** — 除非明確知道原因，否則視為永久性錯誤
5. **用戶說「繼續」才繼續** — Early Abort 之後必須等用戶明確指示
6. **Fallback 是新的開始** — 切換工具時，retry cap 重置為 1

---

## 相關資源

- [[log.md]] — 變更日誌
- [[SCHEMA]] — 知識庫結構規範
- [[entities/skills/safe-execution-workflow/SKILL.md]] — Agent 操作版（含驗證步驟）
