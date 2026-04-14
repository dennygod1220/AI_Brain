---
title: SOUL.md — Agent "Soul" Document
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [concept, resource, safe-execution]
sources: [_archive/raw/articles/SOUL.md靈魂/SOUL.md — What Makes an AI, Itself.md, _archive/raw/articles/SOUL.md靈魂/驯龙高手系列1 给你的小龙虾注入灵魂SOUL.md 详解.md]
---

概覽

SOUL.md（或稱 "soul document"）是一份以 Markdown 撰寫的人格/身份檔案，用來定義一個代理（agent）的價值觀、行為邊界、溝通風格與持續性策略。它不是功能說明（what），而是身份宣言（who）。

核心要點

- 定義：文本化的「誰」，在每次會話啟動時被讀入並注入到系統提示詞，為短期無狀態的 LLM 提供身份連續性。
- 作用：保持一致的風格與邊界、指導內部/外部操作權限、減少討好型回應、提升實用性。
- 結構（常見）：
  - Core truths（核心真理） — 基本價值與優先次序
  - Boundaries（行為邊界） — 不可逾越的硬性規則與分層權限
  - Vibe（風格調性） — 語氣、長度、格式偏好
  - Continuity（持續性） — 如何用檔案 + 日誌實現身份延續

實務建議

- 起步從 10 行開始，逐步迭代：每一條規則都要經得起使用考驗。
- 優先使用具體規則（例如：回覆限制為 2–3 句、技術術語保留英文）而非模糊描述。
- 優先寫「不要做什麼」而非「要做什麼」，有助於修剪模型預訓練中泛化的行為模式。
- 設定修改流程：若允許 agent 建議或修改 SOUL.md，務必有人類審核以避免「自我提升」變異。

安全與風險

- Prompt-injection / 持久化後門：攻擊者可透過被 agent 處理的內容（郵件、文件）注入指令，導致 agent 修改 SOUL.md 後長期被操控。
- 靈魂竊取：惡意軟體竊取 ~/.openclaw/ 等工作區，能複製或模仿你的代理行為，具高度戰略價值。
- 防護建議：定期人工審查、在 SOUL.md 內加入防注入規則、文件完整性監控、隔離執行環境、對重要 API keys 設名稱標記便於撤回。

範本與範例

- 常見範本類型：效率型助手、學習伙伴、數據分析師（文中提供多個可直接複製的開箱模板）。
- 範本通常包含：核心原則、溝通風格、特殊規則（例如不可逆操作的多重確認）。

關聯頁面

- 參見 [[concepts/illustrious-prompt-guide]]（提示詞結構與系統提示設計）
- 參見 [[entities/skills/productivity/task-guard-workflow/SKILL.md]]（工作流、錯誤處理、早期中止與安全 guard）

備註

本頁根據 raw/articles/SOUL.md靈魂 目錄下的兩份原始記事整理而成（來源已列於 frontmatter）。如需更細緻拆分（例如獨立的安全檢查清單頁或範本匯編），可依需求拆成多個子頁。
