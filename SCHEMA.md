---
name: SCHEMA
description: "Wiki structure, conventions, and taxonomy rules"
version: 1.1.1
updated: 2026-04-09
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
| `entities/skills/` | Hermes Agent Skill 的備份（可攜式，檔名固定為 SKILL.md） |
| `raw/` | 原始資料（文章、論文、訪談 transcript） |
| `_meta/` | 系統元資料 |
| `_archive/` | 已過時的內容 |

> `entities/skills/` 下的 SKILL.md 保持標準格式，複製到 `.hermes/skills/` 可直接使用。

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

## Update Policy
- 若發現矛盾，請在頁面中註明兩者觀點並標記日期
- 所有的變動必須記錄在 `log.md`
