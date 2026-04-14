# task-guard-workflow Sync Implementation Plan

> **For Hermes:** Direct execution — single task, no subagent needed.

**Goal:** 用 `/root/.hermes/skills/productivity/task-guard-workflow/SKILL.md` (v3.0.0) 覆蓋知識庫中的 `entities/skills/productivity/task-guard-workflow/SKILL.md`

**Source:** `/root/.hermes/skills/productivity/task-guard-workflow/SKILL.md` (v3.0.0, updated 2026-04-14)
**Target:** `/mnt/c/Users/denny/Downloads/SillyTavern/koboldcpp-config/AI_Brain/entities/skills/productivity/task-guard-workflow/SKILL.md`

---

## Task 1: 覆蓋 SKILL.md

**Objective:** 用 source 完整覆蓋 target

**Files:**
- Source: `/root/.hermes/skills/productivity/task-guard-workflow/SKILL.md`
- Target: `/mnt/c/Users/denny/Downloads/SillyTavern/koboldcpp-config/AI_Brain/entities/skills/productivity/task-guard-workflow/SKILL.md`

**Step 1: Copy source to target (overwrite)**

```bash
cp /root/.hermes/skills/productivity/task-guard-workflow/SKILL.md \
   /mnt/c/Users/denny/Downloads/SillyTavern/koboldcpp-config/AI_Brain/entities/skills/productivity/task-guard-workflow/SKILL.md
```

**Step 2: Verify file exists and size matches source**

```bash
ls -la /mnt/c/Users/denny/Downloads/SillyTavern/koboldcpp-config/AI_Brain/entities/skills/productivity/task-guard-workflow/SKILL.md
wc -l /mnt/c/Users/denny/Downloads/SillyTavern/koboldcpp-config/AI_Brain/entities/skills/productivity/task-guard-workflow/SKILL.md
```
Expected: 164 lines (same as source)

---

## Task 2: 更新 index.md

**Objective:** 同步更新 index.md 中的版本與描述資訊

**Files:**
- Modify: `/mnt/c/Users/denny/Downloads/SillyTavern/koboldcpp-config/AI_Brain/index.md`

**Step 1: Patch index.md — 更新 Entities 中 task-guard-workflow 條目**

TargetContent:
```
- [[entities/skills/productivity/task-guard-workflow/SKILL.md]] — Task Guard Workflow v2.0.0（加強版）：Profile-Aware 狀態機 + 終端輸出防護 + 工具錯誤防護 + Artifact 產出
```

ReplacementContent:
```
- [[entities/skills/productivity/task-guard-workflow/SKILL.md]] — Task Guard Workflow v3.0.0：日誌切片 + 錯誤處理 + Early Abort + Fallback 策略
```

**Step 2: Verify patch**

```
grep "task-guard-workflow" index.md
```
Expected: line contains "v3.0.0"

---

## Task 3: 更新 log.md

**Objective:** 記錄此次同步動作

**Files:**
- Modify: `/mnt/c/Users/denny/Downloads/SillyTavern/koboldcpp-config/AI_Brain/log.md`

**Step 1: Append to log.md**

```bash
echo "## [2026-04-14] sync | task-guard-workflow v3.0.0 sync
- /root/.hermes/skills/ → AI Brain 覆蓋同步
- version 2.0.0 → 3.0.0
- index.md 版本描述已更新" >> \
  /mnt/c/Users/denny/Downloads/SillyTavern/koboldcpp-config/AI_Brain/log.md
```

**Step 2: Verify log appended**

```bash
tail -5 /mnt/c/Users/denny/Downloads/SillyTavern/koboldcpp-config/AI_Brain/log.md
```
Expected: last 5 lines include the new sync entry

---

## Task 4: Git Commit

**Objective:** 將變更提交至 AI Brain Git 版本控制

**Files:**
- Working tree: `/mnt/c/Users/denny/Downloads/SillyTavern/koboldcpp-config/AI_Brain/`

**Step 1: Stage changed files**

```bash
cd /mnt/c/Users/denny/Downloads/SillyTavern/koboldcpp-config/AI_Brain
git add entities/skills/productivity/task-guard-workflow/SKILL.md \
         index.md \
         log.md \
         docs/plans/2026-04-14-task-guard-workflow-sync.md
```

**Step 2: Commit with descriptive message**

```bash
git commit -m "sync: update task-guard-workflow to v3.0.0

- overlay from ~/.hermes/skills/productivity/task-guard-workflow/SKILL.md
- version 2.0.0 → 3.0.0
- log path refactored: .hermes/profiles/ → .hermes/logs/task-guard/"
```

**Step 3: Verify commit**

```bash
git log -1 --stat
```
Expected: commit shows SKILL.md, index.md, log.md, plan file

---

## Verification Checklist

- [ ] `entities/skills/productivity/task-guard-workflow/SKILL.md` 為 164 lines
- [ ] frontmatter `version: 3.0.0`
- [ ] `index.md` Entities 條目顯示 v3.0.0
- [ ] `log.md` 包含今日 sync 記錄
- [ ] Git commit successful with correct files staged

---

## Summary of Changes (v2.0.0 → v3.0.0)

| 差異 | v2.0.0 | v3.0.0 |
|------|--------|--------|
| 章節結構 | 6 章（狀態機 + Artifact） | 4 章（移除狀態機 + Artifact） |
| 日誌路徑 | `$HOME/.hermes/profiles/<Profile>/` | `$HOME/.hermes/logs/task-guard/<Profile>/` |
| 標籤 | Safe-Execution, Tool-Error, State-Management, Workflow, Profile-Aware, Artifact | Safe-Execution, Tool-Error, Workflow, Log-Management |
| related_skills | `[]` | `[writing-plans]` |
| description | 工業級任務執行工作流 | Profile-Aware 執行階段防護工作流 |
