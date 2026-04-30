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
- 故事圖片路徑：`\\\\wsl.localhost\\Ubuntu\\root\\koboldcpp-config\\Hermes\\data\\temp_outputs\\`

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

## [2026-04-26] lint-fix | 知識庫修復：斷鏈 + frontmatter + index + cross-refs
- **斷鏈修復**：`hermes-multiagent-discord-system.md` 移除失效 `.patch` 引用，改指向 `[[_archive/raw/Hermes_MultiAgent_Fix_Report.md]]`
- **Frontmatter 補全**：8 頁補上 `title:` 欄位，2 頁修正 `source:`→`sources:`
- **Index 修正**：加入缺少的 `concepts/us-market-daily-skill-development.md`，頁數同步為 20
- **Cross-reference**：補 4 組雙向 wikilink（soul-md ↔ hermes-agent-soul-craft、illustrious-prompt-guide ↔ generation-strategy、us-market-daily-skill-development → us-market-daily-skill）
- 跳過：prompt-master skill（來自 GitHub，非 wiki 原生內容）

## [2026-04-26] update | trading-assistant-system — 新增 Chrome Extension 截圖分析方向
- 新增新方向章節：Chrome Extension + Vision 截圖分析
- 方案核心：Extension 主動截圖 + DOM 抓價 → 存本地 → Hermes 分析
- 完全繞過 WSL + Chrome CDP 限制，不暴露 TradingView Cookie

## [2026-04-27] create | docs/plans — TradingView Chrome Extension 實作計畫
- 新增: `docs/plans/2026-04-27-tradingview-chrome-extension.md`
- 共 13 個 Task，分 4 個 Phase
- Phase 1: Extension 核心骨架 (Manifest + Popup + Content Script)
- Phase 2: 截圖 + 存檔 (Background Worker + 端到端測試)
- Phase 3: Hermes 側管道 (Watcher + Skill + Alias)
- Phase 4: 邊界情況打磨 (Error Handling + README)

## [2026-04-27] create | raw — MNQ 早盤交易覆盤
- 新增: `raw/2026-04-27-mnq-morning-trade-notes.md`
- 交易記錄：27,386.5做空×2口，TP1=27,374.5 (+12點)✅，第二口停損27,401.75 (-15.25點)❌
- J值實測：4.80→22.88→91.29，發現MNQ超賣閾值可能需到0~-5才有效
- 技術觀察：EMA三線坍縮(<5點差距=無效壓力牆)、第二次超賣效力弱於第一次
- Tags: #trading #mnq #kdj #review

## [2026-04-27] create | trading/sessions — MNQ 夜盤交易記錄
- 新增: `trading/sessions/2026-04-27-mnq-night.md`
- 交易：27,400做空×2口，SL 27,428.25，被StochRSI超賣反彈嘎停損 -56.5點 (-$113)
- 方向判斷正確（停損後跌到27,387），但進場太急 + SL太窄
- 引用3張夜盤截圖: 20:38(猶豫)→20:43(被嘎)→20:49(停損)

## [2026-04-27] create | trading/journal — 入場猶豫本身就是信號
- 新增: `trading/journal/entry-hesitation-signal.md`
- 核心原則：當你在問「要不要等XX」，答案永遠是「等」
- 根據夜盤經驗萃取：「猶豫代表條件不成熟」

## [2026-04-27] update | index.md + trading/index.md — 新增夜盤 & journal 條目
- index.md 總頁數 30→32
- trading/index.md 加入夜盤 session 與 journal 新條目

## [2026-04-27] update | trading/sessions — 夜盤補上交易二（+72.75點）
- 夜盤記錄補上第二筆交易：27,418.75做空×2口，TP1=27,394(+24.75點)✅，TP2=27,370.75(+48點)✅
- 合計 +72.75點，夜盤從-56.5點翻正為+16.25點
- 新增6張截圖來源
- 新增收穫：分倉管理、POC壓力確認後才進場、美股開盤前抱單心態

## [2026-04-28] create | trading/sessions — MNQ 早盤交易記錄（+14.5點）
- 新增: `trading/sessions/2026-04-28-mnq-morning.md`
- 交易：27,490.5做多×2口，第1口27,499.5平(+9點)✅，第2口27,496平(+5.5點)✅
- 合計 +14.5點 (+$29)
- 亮點：SL調整有紀律(10→16→追蹤EMA)、KDJ+StochRSI雙重死叉確認出場、分倉管理正確
- 引用4張截圖: 07:20(觀察)→07:25(進場)→07:37(TP1)→07:45(TP2)

## [2026-04-28] update | trading/sessions — 早盤補上交易二（±0點打平）
- 新增交易二：27,493做多×2口，第1口27,484(-9點)❌，第2口27,502(+9點)✅ = ±0
- 亮點：第一口被掃後第二口抱到打平、27,500 突破後順利成交
- 新增2張截圖：08:05(被掃)→08:09(突破+打平)
- 加入教訓：進場時間點＝盈虧關鍵、大賺後下一筆要更嚴格

## [2026-04-28] update | trading/sessions — 早盤補上交易三&四（最終 -16點）
- 新增交易三：27,474.5做多限價單×2口，SL 27,446.5(-56點)❌
  - EMA坍縮區接多 = 接刀子，完全驗證框架教訓
- 新增交易四：27,446做空×2口，TP 27,433.25(+25.5點)✅
  - 從-56虧損後快速調整，心態清楚
- PnL更新：+14.5→±0→-56→+25.5 = **-16點**
- 新增4張截圖：09:49→09:50→09:54→09:57

## [2026-04-28] update | index.md + trading/index.md — 新增早盤條目
- index.md 總頁數 32→33
- trading/index.md 加入新 session 條目
- 第三筆：27,390.75做空×2口，27,385手動平倉，+11.5點
- 方向判斷正確（平倉後跌到27,360），但心態不對（大賺後急著續賺）+ 進場太早（反彈中途）
- 亮點：發現心態亂了主動小賺出場，保住了今日戰果
- 總計夜盤調整：+16.25→+27.75點，全日+64.75點
- index.md / trading/index.md 已同步更新
- 建立 `trading/` 目錄結構 + `trading/index.md`
- 子目錄：sessions/, journal/, indicators/, market-notes/
- 新增 `.gitignore` 規則：忽略 `trading/sessions/*`
- SCHEMA.md：加入 trading 目錄結構 + 11 個交易專用標籤
- index.md：加入 📈 Trading 章節，共 8 個條目

## [2026-04-27] copy | raw → trading/sessions/
- 複製: `raw/2026-04-27-mnq-morning-trade-notes.md` → `trading/sessions/2026-04-27-mnq-morning.md`
- raw 副本加上 frontmatter（保留為不可變原始記錄）
- sessions 副本加上 session 型態 frontmatter

## [2026-04-27] create | trading/journal — 覆盤知識萃取
- 建立 [[trading/journal/kdj-mnq-threshold-calibration]]
- 建立 [[trading/journal/second-oversold-trap]]
- 建立 [[trading/journal/ema-collapse-warning]]

## [2026-04-27] create | trading/indicators — 指標筆記
- 建立 [[trading/indicators/kdj-for-mnq]]
- 建立 [[trading/indicators/stochrsi-extreme-behavior]]

## [2026-04-27] create | trading/market-notes — 市場觀察
- 建立 [[trading/market-notes/asian-session-liquidity]]

## [2026-04-27] update | raw — 補 frontmatter
- `raw/2026-04-27-mnq-morning-trade-notes.md` 新增 YAML frontmatter

## [2026-04-27] update | SCHEMA.md — trading 結構與標籤
- 目錄表加入 trading/ 及其子目錄
- 標籤分類新增 Trading Domain（11 個標籤）

## [2026-04-27] update | index.md — 加入 Trading 章節
- 頁數更新 20→30
- 新增 📈 Trading 章節（8 個 wikilinks）

## [2026-04-27] update | hermes-watcher.py — wiki 截圖歸檔
- `hermes-watcher.py` 新增 `WIKI_SCREENSHOT_DIR` 與 `--archive-wiki` 指令
- `--import` 現在同步複製截圖到 `WIKI/trading/screenshots/`
- 獨立的 `--archive-wiki` 可手動歸檔最新截圖
- 引用方式：`![[tv_2026-04-27_07-30-00.png]]`
- 新增 `trading/screenshots/` 目錄至 SCHEMA.md
- 更新: `raw/2026-04-27-mnq-morning-trade-notes.md`
- 補充第二筆交易：27,419.5做多×2口，TP1=27,434.5(+15點)✅，TP2=27,444.75(+25.25點)✅
- 今日總計：空單 -3.25點 + 多單 +40.25點 = **+37點**
- 新增KDJ關鍵發現：強趨勢下J值可在80+持續運行，K/D多頭排列比J值絕對值更重要
- 新增StochRSI兩度黏住100/100的極端狀況記錄
- Tags: #trading #mnq #kdj #review

## [2026-04-28] create | CME 即時數據訂閱方案
- 建立 [[trading/market-notes/cme-data-pricing]]
- 內容：CME 市場數據 6 種方案比較（免費～$179/月），含 IBKR/Binance/Databento/CME Direct 等
- 用途：為 Hermes Agent 即時盤面監控選型參考
- Tags: #trading #mnq #resource

## [2026-04-29] create | trading/sessions — MNQ 早盤交易記錄（-15.5點）
- 新增: `trading/sessions/2026-04-29-mnq-morning.md`
- 交易：27,250.25 做多×1口，手動停損 27,234.75（-15.5點 ❌）
- 進場邏輯：慢線EMA接多，合理方向正確好球，但K/D尚未給golden cross
- 停損邏輯：價格跌破EMA三線 + KDJ J二次探底(-8.47) = 方向假設被破壞
- 亮點：手動提前停損沒死守32pt遠SL，紀律正確
- 第二次 oversold trap 再次驗證（J: 5.02→16.43→3.14→-8.47）
- 引用4張截圖：08:55(觀察)→09:00(進場)→09:04(警示)→09:06(停損)
- index.md 總頁數 33→34
- trading/index.md 已同步更新

## [2026-04-29] create | trading/indicators — ADX 盤整過濾 + 多時間框架
- 新增: `trading/indicators/adx-for-mnq.md`
- 內容：ADX(14) 作為趨勢強度濾網（<18=休息, 18-22=1口模式, >22=正常）
- 多時間框架過濾規則：3分K進場前先看15分K的KDJ方向
- 盤整日識別清單（5項特徵，≥3項 = 盤整日）
- 口數決策矩陣（ADX×15分K方向一致性）
- 4/29 盤整日案例驗證：84pt區間來回3趟
- index.md 總頁數 34→35
- trading/index.md 已同步更新

- fix | 修正 PnL 為 +8pt（補上交易四午盤 +16.5pt）
- index.md 及 trading/index.md 已同步更新

## [2026-04-29] create | trading/indicators — 四指標趨勢 vs 盤整行為對照表
- 新增: `trading/indicators/ema-kdj-ppo-adx-correlation.md`
- 實證分析：4/29 全天 12 個時間點截圖數據交叉比對
- 關鍵發現 1：PPO 收斂到同值 = KDJ 交叉可靠度最高
- 關鍵發現 2：PPO 差距大時 KDJ 交叉容易失敗
- 關鍵發現 3：DI+/DI- 差距 > 10 方向才可信
- 建立完整四指標趨勢 vs 盤整對照表
- index.md 總頁數 35→36
- trading/index.md 已同步更新

## [2026-04-29] update | mnq-trading-system skill — 加入ADX過濾 + 多時間框架
- 加入 ADX(14) 至 Indicators 表 + 口數決策矩陣
- 加入 15-min KDJ alignment check (Multi-Timeframe Filter)
- 加入 Chop Day Recognition checklist（5 signals）
- 加入 Structural thesis break = exit before hard SL 至原則#8
- 已合併自 trading/indicators/adx-for-mnq

## [2026-04-29] fix | trading/indicators/adx-for-mnq v2 — 修正 ADX 閾值錯誤
- 實際 ADX 早上 ~35，非 v1 推估的 <20
- ADX(14) 在 3分K MNQ 長期 25-40，教科書閾值不適用
- v2 改為：看 DI+/DI- 關係（差距 >10 = 有方向，<5 交叉 = 盤整）
- 保留 15分K KDJ 方向過濾（仍然有效）
  - mnq-trading-system skill 同步更新

## 2026-04-29

- `trading/trade-log.yaml` — 建立結構化交易紀錄（YAML，9 筆 trade 從 04/27-04/28 session 記錄中提取）
- `trading/index.md` — 新增 trade-log.yaml 索引
- `SCHEMA.md` — 新增 `trading/trade-log.yaml` 目錄說明
- 統計腳本將寫入 `mnq-trading-system` skill 的 scripts/ 目錄

## [2026-04-29] create | trading/sessions — MNQ 夜盤交易記錄（+38.25pt 🚀）
- 新增: `trading/sessions/2026-04-29-mnq-night.md`
- 交易一（空）：27,181.25做空×1口，SL 27,220.50（-39.25pt ❌，進場太晚）
- 交易二（多）：27,223.75做多×1口，出場 27,301.25（+77.5pt 🚀，模式代表作）
- **夜盤總計：+38.25pt (+$76.5) | 全日總計：+46.25pt (+$92.5)**
- 驗證 Jason's Pattern：KDJ先行交叉 + ADX DI交叉>20 = 高勝率
- PPO 正式從系統中移除（簡化為 EMA+KDJ+ADX DI 三指標）
- 引用7張截圖: 20:03(觀察)→22:09(進空)→22:17(停損)→22:20(進多)→22:26(SL調整)→22:32(SL調整)→22:38(結單+77.5pt)
- index.md 及 trading/index.md 已同步更新（總頁數 36→37）

## [2026-04-30] create | trading/sessions — MNQ 早盤交易記錄（+110.25pt 🚀，兩口拆分教科書）
- 新增: `trading/sessions/2026-04-30-mnq-morning.md`
- 交易一（多）：27,299.5做多×2口，TP1 27,325.5(+26pt) / 第二口 27,383.75(+84.25pt) = **+110.25pt** 🚀
- **trade-log 中單筆獲利最高記錄**
- Jason's Pattern 再次驗證：KDJ 黃金交叉先行 + ADX DI+>20 確認
- KDJ J=112.59 過熱門檻（MNQ 105+）出場，時機精準
- 兩口拆分完美執行：TP1 +26 保護利潤，第二口放手讓 🚀
- 歸檔3張截圖: 06:05(進場)→06:06(TP1後)→06:12(結單+84.25pt)
- index.md 頁數 37→38，trading/index.md & log.md 同步更新

## [2026-04-30] create | trading/strategy — MNQ Scalping System 策略參考文件
- 新增: `trading/strategy/mnq-scalping-system.md`
- 完整收錄：圖表配置、進場5層篩選、兩口拆分+Train Mode 🚃 出場規則、盤整辨識、口數決策、8條原則、關鍵數字速查、亞洲盤時間節點
- 手機友善格式，盤中可快速查閱
- index.md 頁數 38→39，trading/index.md 新增 Strategy 分類

## [2026-04-30] update | trading/indicators — 客製ADX（新增 DI 交叉 Alert 條件）
- 新增: `trading/indicators/客製ADX.md`
- 基於 `raw/TradingView指標-客製ADX.md` 原始版擴充
- 新增 `alertcondition("ADX 多頭交叉")`：+DI 上穿 -DI **且 DI 值高於水平線**
- 新增 `alertcondition("ADX 空頭交叉")`：-DI 上穿 +DI **且 DI 值高於水平線**
- 新增 `plotshape` 圖表標記（綠色 ▲ / 紅色 ▼）
- raw/ 還原為原始版本（保持不可變性）
- index.md 頁數 39→40
