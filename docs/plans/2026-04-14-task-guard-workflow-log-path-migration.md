# Task Guard Workflow Log 儲存位置修改計劃

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** 將 task-guard-workflow 的所有日誌從 `$HOME/.hermes/profiles/<Profile>/` 移至 `$HOME/.hermes/logs/task-guard/<Profile>/`，避免與 Hermes Agent 自身的 profile 機制衝突。

**Architecture:** 採用 `.hermes/logs/task-guard/<Profile名稱>/` 三層結構：保留 profile 隔離（避免不同任務的日誌混在一起），但收攏到統一日誌根目錄（與 Hermes Agent 其他日誌一致）。

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
| — | YAML frontmatter description（若有的話） |

**Step 3: Commit**

```bash
git add /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
git commit -m "chore(task-guard): 確認 log 路徑參照點"
```

---

## Task 2: 更新 YAML frontmatter 與頂部宣告

**Objective:** 更新 description 和 metadata，反映新路徑結構

**Files:**
- Modify: `/root/.hermes/skills/productivity/task-guard-workflow/SKILL.md:4,13`

**Step 1: 更新 description**

```yaml
description: Profile-Aware 執行階段防護工作流 — 專注於日誌切片、錯誤處理、Early Abort 與 Fallback 策略。日誌統一存在 `$HOME/.hermes/logs/task-guard/<Profile>/`。
```

**Step 2: 更新 metadata.hermes.tags**

移除 `Profile-Aware`，新增 `Log-Management`：

```yaml
tags: [Safe-Execution, Tool-Error, Workflow, Log-Management]
```

**Step 3: Commit**

```bash
git add /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
git commit -m "chore(task-guard): 更新 description 與 tags"
```

---

## Task 3: 新增「路徑結構」到頂部

**Objective:** 在「核心目的」前加入統一路徑說明

**Files:**
- Modify: `/root/.hermes/skills/productivity/task-guard-workflow/SKILL.md（在 `## 核心目的` 之前）

**Step 1: 在 `## 核心目的` 之前插入**

```markdown
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
```

**Step 2: Commit**

```bash
git add /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
git commit -m "docs(task-guard): 新增統一路徑結構說明"
```

---

## Task 4: 更新第一章 Safe Terminal Execution 的路徑

**Objective:** 將 `PROFILE_DIR` 指向新的 `$HOME/.hermes/logs/task-guard/` 結構

**Files:**
- Modify: `/root/.hermes/skills/productivity/task-guard-workflow/SKILL.md:39-49`

**Step 1: 更新 bash 片段**

舊：
```bash
PROFILE_DIR="$HOME/.hermes/profiles/你的_profile_名稱"
```

新：
```bash
PROFILE_DIR="$HOME/.hermes/logs/task-guard/你的_profile_名稱"
mkdir -p ${PROFILE_DIR}/execute_log ${PROFILE_DIR}/output_cache ${PROFILE_DIR}/error_cache
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
- Modify: `/root/.hermes/skills/productivity/task-guard-workflow/SKILL.md（~107 行附近）`

**Step 1: 更新 error_cache bash 片段**

確認舊：
```bash
PROFILE_DIR="$HOME/.hermes/profiles/你的_profile_名稱"
```

新：
```bash
PROFILE_DIR="$HOME/.hermes/logs/task-guard/你的_profile_名稱"
```

**Step 2: Commit**

```bash
git add /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
git commit -m "chore(task-guard): 更新第三章 error_cache 路徑"
```

---

## Task 6: 更新 execute_log 日誌格式說明

**Objective:** 將 `${PROFILE_DIR}/logs/execute_log/` 更新為新路徑格式

**Files:**
- Modify: `/root/.hermes/skills/productivity/task-guard-workflow/SKILL.md:118`

**Step 1: 更新說明文字**

舊：
```
所有摘要統一寫入 `${PROFILE_DIR}/logs/execute_log/{YYYY-MM-DD}.log`
```

新：
```
所有摘要統一寫入 `${PROFILE_DIR}/execute_log/{YYYY-MM-DD}.log`
```

**Step 2: Commit**

```bash
git add /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
git commit -m "docs(task-guard): 更新 execute_log 路徑格式說明"
```

---

## Task 7: 更新 Pitfalls 第 7 條

**Objective:** 將「Profile-Aware 嚴禁寫入全域目錄」改為新的路徑守則

**Files:**
- Modify: `/root/.hermes/skills/productivity/task-guard-workflow/SKILL.md:~140`

**Step 1: 更新 Pitfall 7**

舊：
```
7. **所有路徑必須 Profile-Aware** — 嚴禁寫入全域目錄
```

新：
```
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

**Step 1: 搜尋確認無殘留**

```bash
grep -n "\.hermes/profiles\|PROFILE_DIR.*profiles" /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
```

預期：無輸出（0 matches）

**Step 2: 確認新路徑格式正確**

```bash
grep -n "\.hermes/logs/task-guard" /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
```

預期：6 處（frontmatter × 1, 路徑結構 × 1, 第一章 × 1, 第三章 × 1, execute_log × 1, Pitfalls × 1）

**Step 3: 最終 commit**

```bash
git add /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md
git commit -m "chore(task-guard): 完成路徑移轉 — 統一至 .hermes/logs/task-guard/"
```

---

## 變更摘要

| 項目 | 舊路徑 | 新路徑 |
|------|--------|--------|
| 日誌根目錄 | `$HOME/.hermes/profiles/<Profile>/` | `$HOME/.hermes/logs/task-guard/<Profile>/` |
| execute_log | `.../logs/execute_log/` | `.../execute_log/`（少了一層 logs） |
| output_cache | `.../logs/output_cache/` | `.../output_cache/` |
| error_cache | `.../logs/error_cache/` | `.../error_cache/` |

**注意：** 目錄結構從 `profiles/<Profile>/logs/` 簡化為 `task-guard/<Profile>/`，少了一層 `logs/` 嵌套，更直觀。

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
