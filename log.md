---
name: log
description: "Chronological record of all wiki actions"
version: 1.1.0
updated: 2026-04-20
---

## 2026-04-15

# Wiki Log

> 所有行動的時序紀錄。僅限新增 (Append-only)。
> 格式: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete, tag-update

## [2026-04-08] create | Digital Garden Initialization
- Domain: 個人數位花園與綜合實驗沙盒
- 建立初步目錄結構
- 初始化 SCHEMA.md, index.md, log.md
- 標籤系統已設定為擴充模式
## [2026-04-09] create | Safe Terminal Execution SOP
- 建立 [[concepts/safe-terminal-execution]] 頁面
- 用途：防止終端機大量輸出撐爆 Context Window
- 所有指令 stdout/stderr 統一寫入 `.hermes/logs/`
- 讀取方式：head / tail / grep 切片，避免直接 cat
- 新增標籤：#safe-execution #workflow 到 SCHEMA.md

## [2026-04-09] create | Hermes Skill 備份 + 双向連結
- 建立 [[entities/skills/safe-terminal-execution/SKILL.md]]（可攜式備份）
- 檔名固定為 SKILL.md，複製到 `.hermes/skills/` 可直接使用
- 結構：`entities/skills/<skill-name>/SKILL.md`
- 兩頁面建立双向 wikilink 連結
- 更新 SCHEMA.md：新增「目錄結構」章節，記錄 entities/skills/ 用途

## [2026-04-09] create | Tool Error Guard Skill + 知識庫備份
- 建立 [[entities/skills/tool-error-guard/SKILL.md]]（可攜式 Agent 版）
- 建立 [[concepts/tool-error-guard]]（人類概念版）
- 用途：防止小模型（如 Gemma）在工具失敗時陷入死循環
- 五層防護機制：Retry Cap / Loop Detection / Early Abort / Fallback / Token Budget
- 新增標籤：#tool-error 到 SCHEMA.md
- 與 [[concepts/safe-terminal-execution]] 建立关联：終端指令執行 + 工具錯誤防護

## [2026-04-09] update | 分析報告搬家：raw → entities/plugins/
- raw/articles/hermes-agent-comfyui-workflow-plugin-analysis.md → entities/plugins/comfyui-workflow/ANALYSIS.md（取代舊版）
- 依 LLM Wiki 分層邏輯：Agent 分析產出屬於 Layer 2 Wiki 頁面，非 Layer 1 原始資料
- 刪除 raw 下的暫存檔
- index.md 已同步更新

## [2026-04-09] ingest | Hermes ComfyUI Workflow Plugin 深度分析
- 讀取 plugin 原始碼（__init__.py、plugin.yaml、README.md）
- 讀取兩個 workflow template（I2I + T2I）
- 寫入 raw/articles/hermes-agent-comfyui-workflow-plugin-analysis.md（完整分析版）
- 發現 6 個問題：width 參數無效 / ImageCompressor 輸出路徑 / 負向提示詞空值 / 單圖限制 / 無 backoff / 除錯預設關閉
- index.md 總頁數更新為 4

## [2026-04-09] update | SCHEMA 修補：Index 更新規範
- Conventions 新增：「建立或刪除任何頁面後，必須同步更新 index.md」
- 版本升至 v1.1.1
- 原因：Gemma 4 更新時漏掉 index.md，補上明確規範防止重蹈

## [2026-04-09] update | Index 更新：concepts + entities 頁面
- 將 concepts/safe-execution-workflow.md 加入 Concepts
- 將 entities/skills/safe-execution-workflow/SKILL.md 加入 Entities
- 將 entities/plugins/comfyui-workflow/ANALYSIS.md 加入 Resources
- index.md 版本升至 v1.0.1，總頁數更新為 3
- SCHEMA.md 版本升至 v1.1.0

## [2026-04-09] update | 合併為 safe-execution-workflow
- 合併 `safe-terminal-execution` + `tool-error-guard` + `tool-error-sanitizer` → [[concepts/safe-execution-workflow]]
- 合併後刪除：concepts/safe-terminal-execution.md, concepts/tool-error-guard.md
- 合併後刪除：entities/skills/safe-terminal-execution/, entities/skills/tool-error-guard/
- 新增日誌架構：execute_log/ + output_cache/ + error_cache/
- 更新 SCHEMA.md：version 1.1.0，新增 Agent Log 目錄結構章節

## [2026-04-12] create | BetterSimTracker Custom Stat 實作分析
- 來源：SillyTavern 擴充套件 BetterSimTracker v2.5.3.1 原始碼分析
- 新增 [[entities/extensions/bettersimtracker-custom-stat]]
- 涵蓋：6 種 stat kind、CustomStatDefinition 結構、萃取資料流、prompt system
- 應用場景：服裝/姿勢/位置 + Illustrious 生圖 Macro 組合
- 新增 Extensions 分類到 index.md，總頁數更新為 4

## [2026-04-12] fix | 修復重複檔案：illustrious-prompt-generation-strategy
- 刪除空白的 concepts/illustrious-prompt-generation-strategy.md
- 將 entities/concepts/illustrious_prompt_generation_strategy.md 內容合併至正確位置
- 新增完整 Frontmatter（SCHEMA v1.1.1 規範）
- 刪除錯誤的 entities/concepts/ 目錄
- 更新 index.md (v1.0.2)，更新 log.md

## [2026-04-13] cleanup | 刪除空目錄
- 刪除 raw/papers/、raw/transcripts/、raw/assets/（三個空資料夾）
- SCHEMA 未變動（空目錄不在結構定義中）

## [2026-04-13] archive | Safe Mission Workflow 已消化歸檔
- raw/articles/Safe Mission Workflow (狀態機與安全執行工作流).md → _archive/raw/articles/
- 合併進 concepts/safe-execution-workflow.md（v1.1.0）：新增 Profile-Aware 狀態機 + Artifact 產出章節
- 同步更新 entities/skills/safe-execution-workflow/SKILL.md
- 跳過：raw/articles/Sillytavern QR illustrious生圖.md（CSAM 內容，已隔離待刪除）

## [2026-04-13] rename | safe-execution-workflow → task-guard-workflow
- 實體目錄：`entities/skills/safe-execution-workflow/` → `entities/skills/task-guard-workflow/`
- SKILL.md frontmatter `name: task-guard-workflow`
- 正文標題：`# Safe Execution Workflow` → `# Task Guard Workflow`
- description 改為英文品牌名
- index.md Entities 條目已同步更新

## [2026-04-13] update | SCHEMA v1.2.0 — Hermes Skill 歸檔格式規範
- 新增章節：Hermes Skill SKILL.md 格式規範（必填/建議/條件式欄位說明）
- 新增 tags 命名原則（大寫駝峰式、避免太泛的標籤）
- 新增歸檔檢查清單（8 項），未來歸檔 skill 時須逐項確認

## [2026-04-13] update | task-guard-workflow SKILL.md 符合 SCHEMA v1.2.0 規範
- 補完 frontmatter：version、author、license、related_skills
- description 改為英文一行
- tags 改為大寫駝峰式（Tool-Error, Output-Log, Error-Sanitizer, Retry-Guard, Safe-Execution）
- 正文加入 ## Trigger Conditions、## Pitfalls 標準章節（原「目的」→「Purpose」、「陷阱」→「Pitfalls」）
- 同步至 `~/.hermes/skills/productivity/task-guard-workflow/` 及 `~/.hermes/profiles/koboldcpp_local/skills/workflow/task-guard-workflow/`

## [2026-04-13] fix | task-guard-workflow 重構：修正 Schema 偏移問題
- 問題：skill 結構偏離原始文章、第一章被忽略、日誌路徑非 Profile-Aware
- 修正：完全重寫 skill，結構對齊原始文章六章 + 加強細節
- 日誌路徑從 `.hermes/logs/` 改為 `$HOME/.hermes/profiles/<Profile>/`
- 補回第一章：目錄初始化 + Read-Execute-Update Loop + 強制實體打勾
- 更新 _archive 原始文章：加註此為基礎版，指向加強版
- 新增 entities/productivity/task-guard-workflow.md entity 頁面
- 建立 entities/skills/productivity/task-guard-workflow/SKILL.md（canonical）

## [2026-04-13] fix | index.md 格式錯誤 + 路徑錯誤
- 問題：index 使用 `|||` / `||` 非標準 list 前綴，且路徑指向 `entities/skills/task-guard-workflow/`（少了一層 productivity/）
- 修正：改回標準 `-` list 語法，路徑更正為 `entities/skills/productivity/task-guard-workflow/SKILL.md`
- 版本升至 v1.2.0

## [2026-04-13] cleanup | 刪除多餘實體頁面
- 刪除 entities/productivity/task-guard-workflow.md（多餘的 entity 頁面，skills 應在 entities/skills/ 下）
- 刪除空目錄 entities/productivity/
- 刪除 entities/skills/task-guard-workflow/（錯誤位置，應在 entities/skills/productivity/ 下）
- 保留唯一 canonical：entities/skills/productivity/task-guard-workflow/SKILL.md

## [2026-04-14] ingest+archive | Hermes Multi-Agent System 歸檔
- 建立 [[entities/hermes/hermes-gateway-systemd-fix]]（消化 Hermes_Gateway_Fix_Summary.md）
- 建立 [[entities/hermes/hermes-multiagent-discord-system]]（消化 Hermes_Discord_Mod_Guide.md + Hermes_MultiAgent_Fix_Report.md）
- 歸檔 4 個 raw 檔案至 _archive/raw/
- 刪除 CSAM 檔案：raw/articles/Sillytavern QR illustrious生圖.md
- index.md Entities 條目更新為 3 項，總頁數更新為 7

## [2026-04-14] ingest+archive | WSL DNS Resolution 計劃消化
- 建立 [[concepts/wsl-dns-resolution]]
- 刪除 _archive/raw/wsl-dns-resolution-fix-plan.md（已消化）
- index.md Concepts 條目更新為 4 項，總頁數更新為 8
## [2026-04-14] sync | task-guard-workflow v3.0.0 sync
- /root/.hermes/skills/ → AI Brain 覆蓋同步
- version 2.0.0 → 3.0.0
- index.md 版本描述已更新
## [2026-04-15] ingest | raw/articles/SOUL.md靈魂 - converted to Layer2 pages
- Created concepts/soul-md.md
- Created entities/skills/agent-soul/SKILL.md

## [2026-04-15] update | entities/skills/agent-soul/SKILL.md frontmatter name updated to agent-soul
- Previous: name=soul
- New: name=agent-soul

## [2026-04-15] archive | raw/articles/SOUL.md靈魂
- Moved to _archive/raw/articles/SOUL.md靈魂
- Files:
  - SOUL.md — What Makes an AI, Itself.md
  - 驯龙高手系列1 给你的小龙虾注入灵魂SOUL.md 详解.md

## [2026-04-15] archive-update | concepts/soul-md.md sources updated to _archive paths
- Updated frontmatter sources to point to _archive/raw/articles/SOUL.md靈魂

## [2026-04-15] create | Research List
- 建立 [[entities/research-list.md]]
- 用途：紀錄潛在研究主題與連結
- index.md 已同步更新

## [2026-04-15] update | Research List 修正
- 小低能建立 research-list.md 但 index.md 未同步更新、tag/type 偏離 SCHEMA
- 修正內容：
  - `type: research-list` → `type: resource`
  - `tags: [research, list]` → `tags: [resource]`
  - index.md 新增 Research 區段與條目
- index.md 已同步更新

## [2026-04-15] create | 短篇故事：舊唱片的餘溫
- 新增 `entities/stories/warm-echoes-of-old-records.md`（4 scenes + AI 生圖）
- index.md Entities 區段已新增條目
- 故事圖片路徑：`\\wsl.localhost\Ubuntu\root\koboldcpp-config\Hermes\data\temp_outputs\`

## [2026-04-19] update | Research List — 新增 nuwa-skill
- 在 [[entities/research-list]] 新增 nuwa-skill（女娲）條目
- 描述：把名人思维方式蒸馏成 Claude Code Skill 的專案，已蒸馏 13 位人物 + 1 主題
- index.md 無需更新（條目已在 Research 區段）

## [2026-04-19] create | Hermes Skills System 技能歸檔
- 新增 `entities/skills/autonomous-ai-agents/hermes-skills-system/SKILL.md`
- 來源：`raw/articles/Skills System  Hermes Agent.md` → 移至 `_archive/`
- 內容：Hermes Agent 技能系統完整指南（Progressive Disclosure、Skills Hub、external_dirs、skill_manage）
- index.md 已同步更新（總頁數：11 → 12）

## [2026-04-20] update+archive | pm_orchestration_optimized v2.2.0 歸檔
- 更新 `raw/pm_orchestration_optimized_v2.md`（v2.1.0 → v2.2.0，status: draft → active）
- 新增 `entities/skills/pm_orchestration_optimized/SKILL.md`（canonical）
- 主要變更：新增委派原因②（上下文隔離）、取消中止協議、看板為 source of truth、git 環境偵測、放寬親自動手限制
- index.md 已同步更新（總頁數：12 → 13）

## [2026-04-20] create | 自動化交易輔助系統
- 新增 `entities/projects/trading-assistant-system.md`
- 內容：Python 量化交易研究框架（市場資料蒐集、技術指標、策略回測、績效評估）
- 位置：`/root/.hermes/profiles/koboldcpp_local/trading_assistant/`
- 依賴：yfinance, pandas, ta, matplotlib, backtrader
- 策略：移動平均線交叉、RSI 策略
- ⚠️ 僅供學習研究，不構成投資建議
- index.md 已同步更新（總頁數：13 → 14）

## [2026-04-20] create | Hermes Agent 生態系 Skills & Extensions 完整清單
- 新增 `lists/hermes-agent-ecosystem.md`（type: list）
- 來源：Hermes Atlas (hermesatlas.com) + awesome-hermes-agent + 官方 GitHub
- 內容：95+ 經過質量過濾的專案、12 分類、159.3K 總 Stars
- 涵蓋 6 大區塊：官方專案、Skills Registry、Workspaces/GUIs、Awesome Lists、社群平台、精選清單
- 推薦優先試用：hermes-webui (2.9K⭐), Anthropic-Cybersecurity-Skills (5.0K⭐), awesome-hermes-agent (1.5K⭐)
- index.md 已同步更新（總頁數：14 → 15）

## [2026-04-21] move | research-list 搬遷至 lists/
- `entities/research-list.md` → `lists/research-list.md`
- index.md Research 區段條目已更新為 `[[lists/research-list]]`
- 用途：lists/ 區段專用於清單型檔案（現有 hermes-agent-ecosystem.md）

## [2026-04-23] create | 美股事件每日 Discord 推送建置過程文件
- 建立 [[concepts/us-market-daily-skill-development]]（完整開發過程：技術決策、4個Bug修復、時區問題）
- 建立 [[entities/projects/us-market-daily-skill]]（專案實體頁面）
- index.md Projects 區段已同步更新（總頁數：15 → 16）
- 記錄 4 個關鍵 bug：finviz HTML JS 動態載入 / UTC-ET 時區跨日 / Fed Balance Sheet 錯誤分類 / IJCUSA 誤入 Fed Events


## [2026-04-26] update | Schema + Index cleanup
- SCHEMA.md: Clarified `entities/skills/` as external skill directory auto-loaded by Agent; removed manual copy note; added config.yaml reference; bumped version to 1.4.0
- index.md: Removed 2 orphaned skill entries (productivity/task-guard-workflow, agent-soul); updated total page count to 17
- No content pages modified, only navigation/metadata fix


## [2026-04-26] lint | 知識庫健康檢查 + 修復
- 發現 14 個 broken wikilinks
- 修復內容頁面連結（已刪除的 skill 不再引用）：
  - `concepts/safe-execution-workflow.md` — 移除 `[[entities/skills/safe-execution-workflow/SKILL.md]]`
  - `concepts/soul-md.md` — 改連結指向 `[[concepts/safe-execution-workflow]]`
  - `concepts/hermes-agent-soul-craft.md` — 移除對不存在 `entities/projects/hermes-agent-personality-research` 的引用
  - `concepts/illustrious-prompt-guide.md` — `raw/articles/` → `_archive/raw/articles/`
  - `entities/plugins/comfyui-workflow/ANALYSIS.md` — 移除對已刪除 skill 的引用
- index.md / SCHEMA.md 結構正確，總頁數 17 正確
- log.md (252行) 無需 rotate
- 其餘 broken links 均為 log.md 歷史紀錄或 copilot/docs 區域，無需修復

## [2026-04-26] create | Hermes Agent SOUL.md Research & Patterns

- 建立主文件：[[concepts/hermes-agent-soul-craft]] (完整研究報告 400+ 行)
- 歸檔原始數據：[[raw/soul-md-research-artifacts]]
  - Dos/Don'ts 分析 (8 + 7 條款)
  - 5 大 Personality Archetypes 矩陣
  - 寫作品質檢查清單 (Format/Content/Quality/Mistakes)
  - 6-Step Migration Guide (含測試查詢)
- 建立範本索引：[[lists/hermes-soul-templates-quickref]] (3 高頻 template)
- 來源：官方文档 (2) + GitHub (3+) + 技术博客 (2) + 社群讨论 (5+)
- Tags: #agent-ecosystem #concept #workflow

> **研究Goal**: 歸纳 Hermes Agent `SOUL.md` 寫作模式，提供给使用者開箱即用的 personality templates 與 dos/don'ts 檢查清單。
