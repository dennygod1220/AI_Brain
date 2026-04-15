---
name: SCHEMA
description: "Wiki structure, conventions, and taxonomy rules"
version: 1.3.0
updated: 2026-04-15
---
# Wiki Schema

## Domain
個人數位花園 (Personal Digital Garden) 與綜合實驗沙盒。

## Conventions
- **File names**: 使用小寫、連字符、不含空格 (例如: `ai-agent-test.md`)
- **Links**: 使用 `[[wikilinks]]` 進行連結
- **Frontmatter**: 每頁必須包含 YAML 區塊 (title, created, updated, type, tags, sources)
- **Updates**: 修改內容後必須更新 `updated` 日期，並在 `log.md` 紀錄
- **Index**: 建立或刪除任何頁面後，必須同步更新 `index.md`（新增條目 / 移除條目）
- **Archiving**: 移出舊的內容請移至 `_archive/` 並刪除索引

## Tag Taxonomy (極度寬鬆且具備高擴充性)

**重要規則：若遇到無法涵蓋舊標籤的新領域，請 Agent 主動建立新標籤，並自動更新 SCHEMA.md 裡的標籤清單，以保持分類系統的與時俱進。**

### 核心標籤 (Core Tags)
- #idea: 靈感、初步想法、未經過實證的直覺
- #learning: 正在學習的主題、課程、新知識點
- #resource: 外部參考資料、文章、影片、書籍、工具
- #project: 正在進行中的專案、實驗、任務
- #testing: 工具測試、經驗評測、實驗結果
- #daily: 日常紀錄、隨手筆記、心情
- #concept: 抽象概念、理論、定義、定律
- #entity: 人物、組織、產品、特定模型
- #comparison: 不同事物間的對比分析
- #query: 針對特定問題的搜尋與整理結果
- #archive: 已過時或不再使用的內容
- #safe-execution: 安全執行規範、工作流程優化、工具使用守則
- #workflow: 重複性任務的標準作業流程 (SOP)
- #tool-error: 工具錯誤處理、重試防護、迴圈偵測
- #extension: 軟體擴充套件研究與分析（SillyTavern 等）
- #story: 原創短篇故事、文學創作

### 自動擴充標籤 (Auto-generated)
- (將由 Agent 根據內容動態新增)

## Page Thresholds
- **Create a page**: 當一個概念在 2+ 原始來源出現，或是是一個新的想法時
- **Split a page**: 當頁面超過 200 行時，切分為子主題
- **Archive a page**: 當內容已過時或不再符合 Domain 時

## 目錄結構

| 目錄 | 用途 |
|------|------|
| `concepts/` | 抽象概念、理論、定義（人類可讀版） |
| `entities/` | 實體、人、組織、工具的專屬頁面 |
| `entities/stories/` | 原創短篇故事（md 為主，images/ 存放生圖） |
| `entities/skills/` | Hermes Agent Skill 的備份（可攜式，檔名固定為 SKILL.md） |
| `raw/` | 原始資料（文章、論文、訪談 transcript） |
| `_meta/` | 系統元資料 |
| `_archive/` | 已過時的內容 |

> `entities/skills/` 下的 SKILL.md 保持標準格式，複製到 `.hermes/skills/` 可直接使用。

## Hermes Skill SKILL.md 格式規範（歸檔時必須遵守）

### 標準 Frontmatter 欄位

```yaml
---
name: {skill-name}                    # 必填：技能識別名（小寫、連字符）
category: {category}                  # 必填：分類（如 productivity, mlops, devops 等）
description: {description}            # 必填：一行說明（觸發時 agent 可見）
version: 1.0.0                       # 建議填寫：語義化版本
author: Hermes Agent                  # 建議填寫：作者
license: MIT                          # 建議填寫：授權
metadata:
  hermes:
    tags: [tag1, tag2, tag3]          # 觸發關鍵字（精準、可被 agent 匹配）
    related_skills: [skill-a, skill-b] # 相關技能名稱陣列
prerequisites:                        # 條件式（有需要才加）
  commands: [cmd1, cmd2]             # 需要預裝的 shell 指令
  env_vars: [VAR1, VAR2]             # 需要預設的環境變數
---
```

### 欄位說明

| 欄位 | 必要性 | 說明 |
|------|--------|------|
| `name` | **必填** | 小寫、連字符，與目錄名一致 |
| `category` | **必填** | 上層分類目錄名 |
| `description` | **必填** | 一行描述，agent 據此判斷是否觸發 |
| `version` | 建議 | 語義化版本，預設 `1.0.0` |
| `author` | 建議 | `Hermes Agent` 或 `community` |
| `license` | 建議 | `MIT` |
| `metadata.hermes.tags` | **建議** | 觸發關鍵字，影響 skill 匹配 |
| `metadata.hermes.related_skills` | 可選 | 相關技能名稱陣列 |
| `prerequisites.commands` | 條件式 | 需要預裝的指令（如 `pygount`、`gh`） |
| `prerequisites.env_vars` | 條件式 | 需要設定的環境變數（如 `NOTION_API_KEY`） |

### tags 命名原則

- 使用大寫開頭的駝峰式（如 `GitHub`、`Code-Review`）
- 避免太泛的標籤（如 `workflow`、`productivity`），用更具體的（如 `safe-execution`、`retry-guard`）
- 每個 skill 控制在 3~7 個標籤

### 歸檔檢查清單

當從 `raw/` 消化歸檔一個 skill 到 `entities/skills/` 時：

- [ ] `name` 與目錄名一致
- [ ] `category` 正確
- [ ] `description` 為一行，說明用途
- [ ] `version` 已填寫
- [ ] `metadata.hermes.tags` 已填寫（使用駝峰式）
- [ ] `metadata.hermes.related_skills` 已填寫（如適用）
- [ ] `prerequisites` 已填寫（如適用）
- [ ] 正文結構包含 `## Trigger Conditions`、`## Pitfalls` 等標準章節

## Agent Log 目錄結構（Hermes 專用）

```
.hermes/logs/
├── execute_log/
│   └── {YYYY-MM-DD}.log          ← 每日執行日誌（單行摘要）
├── output_cache/
│   └── {YYYYMMDD_HHMMSS}.log     ← 完整輸出（結果太大時）
└── error_cache/
    └── {YYYYMMDD_HHMMSS}.log     ← 完整錯誤訊息（太長時）
```

## Archive Policy
- 若發現矛盾，請在頁面中註明兩者觀點並標記日期
- 所有的變動必須記錄在 `log.md`

### 來源歸檔規則（Source Archiving）

當 Layer 1 原始來源已完成消化（已轉化為 Layer 2 wiki 頁面並建立 cross-reference），應移至 `_archive/raw/`：

```
_raw/ sources that have been fully digested → _archive/raw/
```

判斷標準：
- 來源的關鍵資訊已存在於 Layer 2 wiki 頁面
- wiki 頁面的 `sources` frontmatter 已註明該原始檔案
- 不再需要以原始檔案為起點查詢

歸檔時：
1. 在 `_archive/raw/` 下保留原始檔案結構（`articles/`, `papers/`, `transcripts/`）
2. 不更新 wiki 頁面的 `sources` frontmatter（指向歸檔後的路徑）
3. 在 `log.md` 記錄歸檔動作
