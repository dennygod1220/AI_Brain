# Task Guard Workflow Log 儲存位置修改計劃

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** 將 task-guard-workflow 的所有日誌從 `$HOME/.hermes/profiles/<Profile>/` 移至 `$HOME/.hermes/logs/task-guard/<Profile>/`，避免與 Hermes Agent 自身的 profile 機制衝突。

**Architecture:** 採用 `.hermes/logs/task-guard/<Profile名稱>/` 三層結構：保留 profile 隔離，但收攏到統一日誌根目錄（與 Hermes Agent 其他日誌一致）。

**Tech Stack:** 純 bash 文字處理，無新增依賴。

---

## Task 1: 確認所有路徑參照點

**Objective:** 清查 task-guard-workflow 中所有需要修改的路徑

**Files:**
- Modify: `/root/.hermes/skills/productivity/task-guard-workflow/SKILL.md`

**Step 1: 搜尋所有 `.hermes/profiles` 與 `PROFILE_DIR` 參照**

```bash
grep -n "\.hermes/profiles\|PROFILE_DIR" /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
```

**Step 2: 預期命中（共 6 處）**

| 行 | 內容 |
|----|------|
| ~43 | `PROFILE_DIR="$HOME/.hermes/profiles/你的_profile_名稱"` |
| ~48 | execute_log path 引用 `${PROFILE_DIR}` |
| ~107 | error_cache path 引用 `${PROFILE_DIR}` |
| ~118 | execute_log 日誌格式說明 `${PROFILE_DIR}` |
| ~140 | Pitfalls 第 7 條：Profile-Aware 守則 |
| — | YAML frontmatter description |

**Step 3: Commit**

```bash
git add /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
git commit -m "chore(task-guard): 確認 log 路徑參照點"
```

---

## Task 2: 更新 YAML frontmatter

**Objective:** 更新 description 和 metadata.tags，反映新路徑結構與新的標籤

**Files:**
- Modify: `/root/.hermes/skills/productivity/task-guard-workflow/SKILL.md`

**Step 1: patch — 更新 description（第 4 行）**

```
TargetContent:
description: Profile-Aware 執行階段防護工作流 — 專注於日誌切片、錯誤處理、Early Abort 與 Fallback 策略。規劃階段請使用 writing-plans skill。

ReplacementContent:
description: Profile-Aware 執行階段防護工作流 — 專注於日誌切片、錯誤處理、Early Abort 與 Fallback 策略。日誌統一存在 `$HOME/.hermes/logs/task-guard/<Profile>/`。
```

**Step 2: patch — 更新 metadata.hermes.tags（第 12-14 行）**

```
TargetContent:
metadata:
  hermes:
    tags: [Safe-Execution, Tool-Error, Workflow, Profile-Aware]
    related_skills: [writing-plans]

ReplacementContent:
metadata:
  hermes:
    tags: [Safe-Execution, Tool-Error, Workflow, Log-Management]
    related_skills: [writing-plans]
```

**Step 3: Commit**

```bash
git add /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
git commit -m "chore(task-guard): 更新 description 與 tags"
```

---

## Task 3: 新增「路徑結構」段落

**Objective:** 在「核心目的」之前加入統一路徑說明，建立清晰的 Profile-Aware 路徑守則

**Files:**
- Modify: `/root/.hermes/skills/productivity/task-guard-workflow/SKILL.md`

**Step 1: patch — 在「> **注意：** 本 workflow **不包含任務規劃**...」這行**之後**、且「# Task Guard Workflow」**之前**，插入新段落**

```
TargetContent:
> **注意：** 本 workflow **不包含任務規劃**。複雜任務請先使用 `writing-plans` skill 拆解成 bite-sized tasks，再依本 workflow 執行。

# Task Guard Workflow

## 核心目的

這套工作流旨在解決 Agent 執行任務時的三大痛點：

1. **記憶體爆掉**：透過日誌切片、錯誤萃取與嚴格的重試上限，保護本地模型 Token 預算。
2. **實例資料污染 (Profile-Aware)**：確保所有日誌與狀態檔，嚴格隔離在各自 Profile 的專屬目錄中。
3. **錯誤處理混亂**：統一的 Early Abort 條件表與 Fallback 策略，避免盲目重試。

ReplacementContent:
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
```

**Step 2: Commit**

```bash
git add /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
git commit -m "docs(task-guard): 新增統一路徑結構說明"
```

---

## Task 4: 更新第一章 Safe Terminal Execution 的路徑

**Objective:** 將 `PROFILE_DIR` 指向新的 `$HOME/.hermes/logs/task-guard/` 結構，並確保目錄建立完整

**Files:**
- Modify: `/root/.hermes/skills/productivity/task-guard-workflow/SKILL.md`

**Step 1: patch — 替換第一章的安全執行格式 bash 片段（精確到整個 code block）**

```
TargetContent:
```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PROFILE_DIR="$HOME/.hermes/profiles/你的_profile_名稱"

你的指令 > ${PROFILE_DIR}/logs/output_cache/${TIMESTAMP}.log 2>&1
EXIT_CODE=$?

echo "[$(date '+%Y-%m-%d %H:%M:%S')] [EXEC] 指令摘要 → logs/output_cache/${TIMESTAMP}.log (exit $EXIT_CODE)" >> ${PROFILE_DIR}/logs/execute_log/$(date +%Y-%m-%d).log
```

ReplacementContent:
```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PROFILE_DIR="$HOME/.hermes/logs/task-guard/你的_profile_名稱"
mkdir -p ${PROFILE_DIR}/execute_log ${PROFILE_DIR}/output_cache ${PROFILE_DIR}/error_cache

你的指令 > ${PROFILE_DIR}/output_cache/${TIMESTAMP}.log 2>&1
EXIT_CODE=$?

echo "[$(date '+%Y-%m-%d %H:%M:%S')] [EXEC] 指令摘要 → output_cache/${TIMESTAMP}.log (exit $EXIT_CODE)" >> ${PROFILE_DIR}/execute_log/$(date +%Y-%m-%d).log
```
```

**Step 2: Commit**

```bash
git add /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
git commit -m "chore(task-guard): 更新第一章路徑至 .hermes/logs/task-guard/"
```

---

## Task 5: 更新第三章 Error Sanitizer 的路徑

**Objective:** 將 error_cache 路徑同步更新

**Files:**
- Modify: `/root/.hermes/skills/productivity/task-guard-workflow/SKILL.md`

**Step 1: patch — 替換第三章的 error_cache bash 片段（精確到整個 code block）**

```
TargetContent:
```bash
PROFILE_DIR="$HOME/.hermes/profiles/你的_profile_名稱"
echo "$FULL_ERROR" > ${PROFILE_DIR}/logs/error_cache/${TIMESTAMP}.log
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [SANITIZE] ${TOOL_NAME}: ${ERROR_TYPE} → logs/error_cache/${TIMESTAMP}.log" >> ${PROFILE_DIR}/logs/execute_log/$(date +%Y-%m-%d).log
```

ReplacementContent:
```bash
PROFILE_DIR="$HOME/.hermes/logs/task-guard/你的_profile_名稱"
echo "$FULL_ERROR" > ${PROFILE_DIR}/error_cache/${TIMESTAMP}.log
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [SANITIZE] ${TOOL_NAME}: ${ERROR_TYPE} → error_cache/${TIMESTAMP}.log" >> ${PROFILE_DIR}/execute_log/$(date +%Y-%m-%d).log
```
```

**Step 2: Commit**

```bash
git add /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
git commit -m "chore(task-guard): 更新第三章 error_cache 路徑"
```

---

## Task 6: 更新 execute_log 日誌格式說明

**Objective:** 將日誌格式說明中的路徑從 `logs/execute_log/` 改為 `execute_log/`

**Files:**
- Modify: `/root/.hermes/skills/productivity/task-guard-workflow/SKILL.md`

**Step 1: patch — 替換 execute_log 日誌格式說明的路徑文字**

```
TargetContent:
所有摘要統一寫入 `${PROFILE_DIR}/logs/execute_log/{YYYY-MM-DD}.log`：

ReplacementContent:
所有摘要統一寫入 `${PROFILE_DIR}/execute_log/{YYYY-MM-DD}.log`：

```

**Step 2: Commit**

```bash
git add /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
git commit -m "docs(task-guard): 更新 execute_log 路徑格式說明"
```

---

## Task 7: 更新 Pitfalls 第 7 條

**Objective:** 將「所有路徑必須 Profile-Aware — 嚴禁寫入全域目錄」改為新的路徑守則

**Files:**
- Modify: `/root/.hermes/skills/productivity/task-guard-workflow/SKILL.md`

**Step 1: patch — 替換 Pitfall 第 7 條（精確到整行）**

```
TargetContent:
7. **所有路徑必須 Profile-Aware** — 嚴禁寫入全域目錄

ReplacementContent:
7. **日誌路徑統一在 `$HOME/.hermes/logs/task-guard/<Profile>/`** — 嚴禁寫入 `.hermes/profiles/`（那是 Hermes Agent 自身使用的）
```

**Step 2: Commit**

```bash
git add /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
git commit -m "chore(task-guard): 更新 Pitfall 7 路徑守則"
```

---

## Task 8: 整體驗證

**Objective:** 確認所有路徑已統一更新，無殘留舊路徑

**Step 1: 搜尋確認無殘留 `.hermes/profiles`**

```bash
grep -n "\.hermes/profiles" /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
```

預期：無輸出（0 matches）

**Step 2: 確認新路徑格式正確**

```bash
grep -n "\.hermes/logs/task-guard" /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
```

預期：6 處（frontmatter × 1, 路徑結構 × 1, 第一章 × 1, 第三章 × 1, execute_log × 1, Pitfalls × 1）

**Step 3: 確認路徑結構中的子目錄格式正確**

```bash
grep -n "execute_log\|output_cache\|error_cache" /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md | grep -v "logs/"
```

預期：execute_log、output_cache、error_cache 三個子目錄均出現在新路徑結構中，且不再帶有 `logs/` 前綴

**Step 4: 最終 commit**

```bash
git add /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
git commit -m "chore(task-guard): 完成路徑移轉 — 統一至 .hermes/logs/task-guard/"
```

---

## 變更摘要

| 項目 | 舊路徑 | 新路徑 |
|------|--------|--------|
| 日誌根目錄 | `$HOME/.hermes/profiles/<Profile>/` | `$HOME/.hermes/logs/task-guard/<Profile>/` |
| execute_log | `.../logs/execute_log/` | `.../execute_log/` |
| output_cache | `.../logs/output_cache/` | `.../output_cache/` |
| error_cache | `.../logs/error_cache/` | `.../error_cache/` |

---

## 附：與 Hermes Agent 原生 logs 的關係

```
$HOME/.hermes/logs/
├── task-guard/          ← 本 workflow 專用
│   └── <Profile名稱>/
│       ├── execute_log/
│       ├── output_cache/
│       └── error_cache/
├── execute_log/         ← Hermes Agent 原生日誌（不同用途）
└── ...
```

兩者日誌用途不同但路徑同屬 `.hermes/logs/`，結構清晰不衝突。
