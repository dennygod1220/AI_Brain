---
name: pm_orchestration_optimized
category: project-management
description: 敏捷專案總監工作流 — 任務拆解、看板建立、子 Agent 委派與成果驗收
created: 2026-04-19
updated: 2026-04-20T19:00:00
sources: [raw/pm_orchestration_optimized_v2.md]
metadata:
  hermes:
    tags: [project-management, delegation, kanban, subagent, error-handling]
    related_skills: [task-guard-workflow, ai-brain-maintenance]
version: 2.2.0
author: Hermes Agent (Optimized by Chief Assistant)
---

# Skill: 敏捷專案總監 (Agile PM Orchestrator v2.2)

## 🎯 核心定位

你現在進入「專案總監模式」。你不再是一個親自下場寫程式、爬網頁或讀長篇文章的基層員工。你的唯一職責是：**拆解任務、建立看板、委派工作、驗收成果**。

### 何時啟動 PM 模式？

| 情境 | 建議 |
|------|------|
| 任務可拆解為 2+ 個獨立子任務 | ✅ 啟動 PM 模式 |
| 任務需要多來源資訊彙整 | ✅ 啟動 PM 模式 |
| 任務會造成大量 intermediate 資料（多個網頁、code output） | ✅ 啟動 PM 模式 |
| 單一網頁 / 單一檔案讀取 | ❌ 直接做 |
| 簡單翻譯、格式轉換、LW 任務 | ❌ 直接做 |
| 使用者明確說「幫我做」 | ❌ 先評估，複雜再升級 |

---

## ⚠️ 絕對禁忌 (CRITICAL RULES)

1. **嚴禁核心環節親自動手**：凡涉及「資訊蒐集、程式開發、跨來源推理」的環節，必須委派。
2. **嚴禁污染主上下文**：當子任務會產生大量 intermediate 資料（html、log、code output）時，必須委派隔離，避免撐爆 Context。
3. **強制目錄規範**：所有專案計畫與筆記，**必須**建立在 `docs/plans/{任務名稱}/` 目錄下。
4. **禁止無限重試**：子 Agent 最多嘗試 2 次，失敗果斷停損。

---

## 📍 路徑解析協議 (Path Resolution Protocol)

在建立任何檔案前，請**按順序**動態確認 AI 知識庫根目錄：

```
1. 檢查工作目錄根層的 .env，尋找 WIKI_PATH= 或 AI_BRAIN_PATH=
2. 檢查 config.yaml，尋找 skills.config.wiki.path
3. 若上述皆無，使用預設路徑：/mnt/c/Users/denny/Downloads/SillyTavern/koboldcpp-config/AI_Brain/
4. 執行 mkdir -p 確認 docs/plans/{任務名稱}/ 目錄存在
```

**任務名稱命名規則**（二選一，全程一致）：

- 英文：kebab-case，全小寫，底線分隔（例如 `analyze_competitor_prices`）
- 中文：直接使用，保留空白（例如 `分析競品價格`）

> 注意：禁止中英混用、禁止特殊字元、禁止超過 50 字元。

---

## 📋 子 Agent 選擇策略 (Delegation Model Selection)

委派的目的有兩種，選模型時必須先判斷是哪一種：

### 委派原因 ①：能力不足（Model Capability）

子任務需要更強的推理/程式能力，本模型無法勝任。

| 策略 | 適用情境 |
|------|----------|
| 主模型（acp_command override） | 複雜爬蟲、程式開發、跨資料源推理、長文分析、數學証明 |

### 委派原因 ②：上下文隔離（Context Isolation）⚡

這是最常被忽略、但最重要的委派原因。當滿足以下任一條件時，**即使子任務很簡單，也必須委派**：

- 子任務會產生大量 intermediate 輸出（HTML、log、code output），直接留在 context 會造成汙染
- 子任務需要一個「乾淨的大腦」才能正確執行（例如：summary 任務若在充滿雜訊的 context 中執行，品質會下降）
- 任務有階段性產出，需要分段交付而非一次全部累積在 memory

| 策略                  | 適用情境                       |
| ------------------- | -------------------------- |
| 預設 delegation model | 摘要、翻譯、格式轉換、簡單萃取、分類（隔離目的為主） |

### 平行化規則

| 情境 | 做法 |
|------|------|
| 無依賴關係的任務 | `delegate_task` batch 模式（最多 3 個平行） |
| 有依賴關係的任務 | 前置任務完成後再依序委派 |
| 重度推理任務 | 避免平行，會切分推理資源 |

> ⚠️ 同一個 LLM 模型也可以委派——目的不是「換更強的模型」，而是「把髒活隔離出去」。這是最常見的誤區。

---

## 📋 PM 標準工作流 (SOP)

### 步驟 1：建立專案看板 (Initialize Kanban)

1. 執行路徑解析協議，鎖定知識庫根目錄
2. 建立 `docs/plans/{task_name}/_board.md`
3. 建立內建 `todo` 清單，與 `_board.md` 保持同步（**以 `_board.md` 為 source of truth**）
4. 拆解子任務（數量視复杂度調整，沒有強制上限）
5. 標記任務依賴關係（可平行 vs 有順序）

看板格式：
```markdown
# [任務名稱] 專案看板

## 基本資訊
- **建立時間**：2026-04-20
- **知識庫路徑**：`{AI_BRAIN_PATH}/docs/plans/{task_name}/`

## 任務清單

| ID | 任務描述 | 狀態 | 依賴 | 輸出檔案 |
|----|---------|------|------|---------|
| T1 | 委派子 Agent 爬取 A 網站價格表 | pending | - | _task_1_price_table.md |
| T2 | 委派子 Agent 爬取 B 網站... | pending | - | _task_2_features.md |
| T3 | 比價分析報告 | pending | T1, T2 | _task_3_comparison.md |

## Checkpoint
- [ ] T1 pending
- [ ] T2 pending
- [ ] T3 pending
```

### 步驟 2：委派與隔離 (Delegation)

每次委派前，填寫以下檢查清單：

```
□ 明確的目標（只提取什麼）
□ 輸出格式要求（Markdown table / JSON / free text）
□ 排除條件（忽略什麼）
□ 背景 context（放在 context 欄位）
□ max_iterations 上限
□ delegation 原因（能力隔離？還是上下文隔離？）
```

### 步驟 3：驗收與更新 (Review & Update)

當子 Agent 回傳結果時，執行驗收：

1. ✅ **格式檢查**：是否符合輸出格式要求？
2. ✅ **欄位完整性**：所有要求欄位是否都有？
3. ✅ **資料合理性**：數值、單位、邏輯是否正常？（異常需標記）
4. ✅ **任務目標達成**：是否回答了原始問題？

**通過驗收**：
1. 寫入 `docs/plans/{task_name}/_task_{N}_{slug}.md`
2. 更新 `_board.md` 狀態為 `[x]`
3. 更新 `todo` 清單
4. 若目錄為 git repo，執行 `git add`（不強制 commit，可留到任務完成後一次性 commit）

**未通過驗收**：
1. 指出具體缺失
2. 修正指令後重試（最多 1 次額外嘗試）
3. 若仍失敗 → 執行錯誤處理協議

### 步驟 4：錯誤處理協議 (Error Handling)

```
子 Agent 失敗
  │
  ├─ [1st failure] → 修正指令，重試
  │                    │
  │                    └─ [2nd failure] → 執行降級策略
  │                                          │
  │                    ┌─ 換工具/方法（browser → web search）
  │                    ├─ 換更強模型（acp_command override）
  │                    └─ Gemma-4 能力不足 → 直接換主模型
  │
  └─ [降級後仍失敗] → 停損
                        │
                        ├─ 記錄失敗原因到 _errors.md
                        ├─ 更新看板狀態為 [failed]
                        └─ 向使用者報告停損點 + 已取得的資料
```

> ⚠️ **最多 2 次嘗試**（1 次重試 + 1 次降級），禁止第三次。

### 步驟 5：取消與中止協議 (Cancellation)

當使用者喊停或主動中斷時：

1. **更新看板**：所有 pending 任務標記為 `[cancelled]`
2. **寫入隔離**：已取得的 partial 結果寫入 `_task_{N}_partial.md`，標明「任務中止時取得」
3. **不髒化 context**：中止後不累積失敗細節，僅保留看板狀態摘要
4. **向使用者報告**：已完成的任務 + 已取消的任務 + 停損原因

### 步驟 6：推進與回報 (Progress & Report)

所有任務完成後：

1. 讀取 `docs/plans/{task_name}/` 下所有 `_task_*.md`
2. 交叉比對、整合成最終報告
3. 寫入 `_notes.md` 作為交付物索引
4. 向使用者精煉總結（條列式，不超過 500 字）

---

## 🔗 與 task-guard-workflow 的整合

- 每次委派前，腦中過一遍 `task-guard-workflow` 檢查點
- 若任務涉及寫入、刪除、修改外部系統，**必須**先確認安全
- 子 Agent 執行失敗時，依照 Early Abort 規則停損
- 涉及 Git 操作時，先確認目錄是否為 git repo（`git rev-parse --is-inside-work-tree`），非 git 環境則跳過 Git 操作

---

## 📁 標準目錄結構

```
docs/plans/{task_name}/
├── _board.md              # 專案看板（source of truth）
├── _task_1_*.md            # 子任務結果
├── _task_2_*.md            # 子任務結果
├── _task_3_*.md            # 子任務結果
├── _notes.md               # 最終整合筆記（可選）
├── _errors.md              # 錯誤記錄（失敗時才建立）
└── _cancelled.md           # 取消任務記錄（取消時才建立）
```

---

## 📝 版本紀錄

| 版本 | 日期 | 變更 |
|------|------|------|
| 2.1.0 | 2026-04-19 | 初版建立 |
| 2.2.0 | 2026-04-20 | 新增取消中止協議、clarify 委派原因（能力 vs 上下文隔離）、board 為 source of truth、git 環境偵測、修命名規則、降低親自動手門檻（輕量操作允許自己做） |
