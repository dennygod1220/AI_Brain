---
name: log
description: "Chronological record of all wiki actions"
version: 1.1.0
updated: 2026-04-30
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
## [2026-04-09] create | ComfyUI Workflow 技能分析
- 建立 raw/transcripts/hermes-comfyui-workflow-analysis.md
- 原始來源：Hermes ComfyUI Workflow Plugin 官方文件分析
- 標籤：#extension #comfyui #workflow

## [2026-04-09] create | WSL DNS 修復
- 建立 [[concepts/wsl-dns-resolution]] 頁面
- 原始來源：WSL DNS 故障排除經驗
- 新增標籤：#wsl #system-administration 到 SCHEMA.md（透過自動擴充）

## [2026-04-09] create | Safe Execution Workflow
- 建立 [[concepts/safe-execution-workflow]]（取代舊 safe-terminal-execution）
- 重新設計為 Profile-Aware 狀態機：dev / prod / debug 三種 profile
- 整合三個防護層：終端輸出 / 工具錯誤 / Artifact 產出防護
- 移除了 `raw/transcripts/`（內容已完全消化至 wiki 頁面）

## [2026-04-09] archive | 原始 transcript 歸檔
- 將 `raw/transcripts/hermes-comfyui-workflow-analysis.md` 移至 `_archive/raw/`
- 內容已完全消化至 [[entities/plugins/comfyui-workflow/ANALYSIS.md]]

## [2026-04-10] archive | WSL transcript 原始檔歸檔
- 已不存在（直接建立 wiki 頁面無原始檔需歸檔）

## [2026-04-10] create | Illustrious Prompt Guide
- 建立 [[concepts/illustrious-prompt-guide]]
- 原始來源：官方 SDXL Prompt 指南（Hugging Face）
- 內容：模型選擇、Prompt 結構、官方參數建議

## [2026-04-10] create | Illustrious Prompt 生成策略
- 建立 [[concepts/illustrious-prompt-generation-strategy]]
- 原始來源：SillyTavern Quick Reply + BetterSimTracker macro 實務經驗
- 內容：Tag→自然語言 fallback 策略

## [2026-04-11] create | SOUL.md 概念頁面
- 建立 [[concepts/soul-md]]
- 定義 Hermes Agent 的人格系統底層概念

## [2026-04-11] create | Hermes Skills System
- 建立 [[entities/skills/autonomous-ai-agents/hermes-skills-system/SKILL.md]]
- 正式建立 Skills Hub 章節、外部技能目錄、skill_manage

## [2026-04-11] archive | ComfyUI raw transcript 歸檔確認
- `_archive/raw/hermes-comfyui-workflow-analysis.md` 已確認存在

## [2026-04-13] create | Agent Skills Index
- 建立 [[concepts/agent-skills-index]]
- 從 Skills Hub 資料提煉：各領域 skill 的簡短描述對照表

## [2026-04-13] create | Hermes Agent 生態系清單
- 建立 [[lists/hermes-agent-ecosystem]]
- 95+ 專案、12 分類、~159.3K Stars 完整整理

## [2026-04-13] update | Hermes Skills System SKILL.md
- 補充 External Directory Linking 設定內容

## [2026-04-13] create | SOUL.md 設計模式研究
- 建立 [[concepts/hermes-agent-soul-craft]]
- 5+ archetypes、3 大寫作技巧、3 組最佳實踐

## [2026-04-13] create | SOUL.md 模板速查表
- 建立 [[lists/hermes-soul-templates-quickref]]
- 3 大 archetype 一頁式參考

## [2026-04-15] create | Hermes Gateway Systemd 修復
- 建立 [[entities/hermes/hermes-gateway-systemd-fix]]
- UV Python 路徑衝突 + Systemd Override 完整解法

## [2026-04-15] create | Hermes 雙 Agent Discord 系統
- 建立 [[entities/hermes/hermes-multiagent-discord-system]]
- 6 階段修復歷程 + 3 大核心 discord.py 修改

## [2026-04-15] create | BetterSimTracker Custom Stat
- 建立 [[entities/extensions/bettersimtracker-custom-stat]]
- 服裝/姿勢/位置 + Illustrious 生圖應用規劃

## [2026-04-18] create | 舊唱片的餘溫
- 建立 [[entities/stories/warm-echoes-of-old-records]]（短篇故事）
- 4 scenes + AI 生圖規劃

## [2026-04-18] update | index.md 同步更新
- 新增 stories 條目

## [2026-04-18] archive | raw 目錄中已消化的原始檔案歸檔
- `raw/hermes-comfyui-workflow-analysis.md` → `_archive/raw/`（4/09 已歸檔）
- `raw/articles/hermes-agent-v0.3-release.md` → `_archive/raw/articles/`
- `raw/research/hermes-agent-extension-system.md` → `_archive/raw/research/`

## [2026-04-19] create | US Market Daily Skill 開發紀錄
- 建立 [[concepts/us-market-daily-skill-development]]
- 記錄美股 Discord 推送建置歷程：技術選型、4 個 bug、時區問題

## [2026-04-19] create | 客製ADX 指標頁面（KDJ + DI 聯動腳本起點）
- 建立 `trading/indicators/客製ADX.md`
- 原始碼來源：`raw/TradingView指標-客製ADX.md`

## [2026-04-27] create | KDJ 指標實戰筆記
- 建立 `trading/indicators/kdj-for-mnq.md`
- 整理背離、無效交叉、StochRSI 比較

## [2026-04-29] create | ADX 盤整過濾 + 多時間框架
- 建立 `trading/indicators/adx-for-mnq.md`
- ADX 值 15 門檻實證 + 週期切換規則

## [2026-04-29] create | StochRSI 極端值行為分析
- 建立 `trading/indicators/stochrsi-extreme-behavior.md`
- 2026-04-29 實戰記錄：2.12 / 2.58 假超賣驗證

## [2026-04-29] create | EMA-KDJ-PPO-ADX 相關性探索
- 建立 `trading/indicators/ema-kdj-ppo-adx-correlation.md`
- 四大指標脫鉤現象：強趨勢下的訊號回溯

## [2026-04-30] rename | 客製ADX → DI方向指標
- `trading/indicators/客製ADX.md` → `trading/indicators/di-indicator.md`
- 更名原因：指標核心為 DI 方向訊號，ADX 主線僅供參考
- 同步修改：Pine Script title, 參數名 adxOver→diThresh, Alert 名稱, bgcolor 邏輯
- 影響檔案：kdj-di-combo.md（來源連結更新）
- 交易者需手動更新 TradingView Pine Editor + 重建 Alert

## [2026-04-30] create | KDJ + DI 聯動腳本
- 建立 `trading/indicators/kdj-di-combo.md`
- 合併 KDJ Pine Script + DI 方向過濾為單一腳本
- 邏輯：KDJ 金叉/死叉決定 Alert 觸發時間，DI 方向 + 門檻值作為趨勢過濾器
- 原始碼來源：`raw/TradingView指標-KDJ.md` + `trading/indicators/客製ADX.md`
- 提供四層 Alert：一般做多/做空、超賣/超買強化版
- index.md 頁數 40→41

## [2026-04-30] archive | raw 原始碼歸檔
- `raw/TradingView指標-KDJ.md` → `_archive/raw/`（已消化至 `kdj-di-combo.md` + `kdj-for-mnq.md`）
- `raw/TradingView指標-客製ADX.md` → `_archive/raw/`（已消化至 `客製ADX.md` + `kdj-di-combo.md` + `adx-for-mnq.md`）
- `raw/` 目錄已清空刪除（所有內容皆已消化或歸檔）

## [2026-04-30] create | MNQ 夜盤交易記錄
- 建立 `trading/sessions/2026-04-30-mnq-night.md`
- 交易一（27,461.25→27,505.5）：+44.25pt ✅ — 完美符合 Jason's Pattern（KDJ金叉 + DI+28.41 >20 + DI gap 17.6）
- 交易二（27,511.25）：+5.25pt ✅ 停損入場價上方鎖利，躲過崩盤
- 本日已實現：早盤 +129pt + 夜盤 +49.5pt = **+178.5pt ($357)** 🚀
- index.md 頁數更新
- 2026-04-30 創下個人單日最佳紀錄 🏆

## [2026-04-30] create | 交易日記 Template
- 建立 `trading/templates/session-journal.md`
- 統一格式：YAML frontmatter → 逐筆交易（進場/出場/覆盤）→ 本日總計 → 模式驗證 → 參考截圖 → 累計績效
- 參考 4/27、4/29、4/30 三份 session 共通結構歸納
- 含 Train Mode 出場條件對照表 + Jason's Pattern 驗證表

## [2026-05-02] create | docs/plans — Jason's Pattern 自動回測引擎
- 建立 `docs/plans/2026-05-02-mnq-jasons-pattern-backtest-engine.md`
- 三階段計畫：Phase 1 回測引擎 → Phase 2 參數優化器 → Phase 3 即時通知骨架
- 使用 yfinance 拉 NQ=F 歷史資料，Python 實作 KDJ / DI+/DI- / EMA 計算
- Grid Search 參數優化防 overfitting
- 相關：[[trading/strategy/mnq-scalping-system]], [[entities/projects/trading-assistant-system]]
- 更新 index.md: 新增 Plans 條目

## [2026-05-03] create | Chrome MCP WSL 連線設定
- 建立 `entities/chrome-mcp-wsl-setup.md` — 從 WSL 連線到 Windows Chrome 的完整架設指南
- 涵蓋：防火牆規則、portproxy、ws-endpoint.sh 動態腳本、WebSocket 端點（Chrome 144+ 不走 HTTP CDP）
- 記錄排錯過程：svchost 搶佔 port 9222、Network.enable 超時（分頁過多）、Chrome profile 切換 port 變動
- 更新 index.md: Entities 新增 chrome-mcp-wsl-setup 條目，頁數 41→42

## [2026-05-03] fix | lint 修復：index 斷鏈 + 缺失條目
- `index.md`: 修復 `客製ADX`→`di-indicator` 斷鏈連結（`#92`)
- `index.md`: 補上 `2026-04-30-mnq-night`、`cme-data-pricing`、`templates/session-journal`（頁數 42→45）
- `trading/index.md`: 修復 `[[trading/trade-log]]` 斷鏈，改為可解析的 `trading/trade-log.yaml`
- `trading/indicators/kdj-di-combo.md`: `sources` 與內文 `raw/` 路徑更新為 `_archive/raw/`
- `entities/chrome-mcp-wsl-setup.md`: 修復 `[[chrome-devtools-mcp]]` 斷鏈，改為純文字引用

## [2026-05-03] archive | trading-assistant-system
- `entities/projects/trading-assistant-system.md` → `_archive/entities/projects/`
- 原因：用戶要求刪除
- `index.md`: 移除條目，頁數 45→44
- `docs/plans/2026-05-02-mnq-jasons-pattern-backtest-engine.md`: wikilink 改為純文字 + (已歸檔)

## [2026-05-03] update | chrome-mcp-wsl-setup — MCP _rpc_lock 死結修復紀錄
- `entities/chrome-mcp-wsl-setup.md`: 新增「_rpc_lock 死結問題詳解」章節
- Root cause: `_refresh_tools()` 中的 `list_tools()` 無 timeout，在背景 task 中 hang 住後永久佔有 `_rpc_lock`，導致所有 tool call 死等 120 秒
- Fix: 對 `list_tools()` 加上 15 秒 `asyncio.wait_for` timeout
- 相關檔案：`/root/.hermes/hermes-agent/tools/mcp_tool.py`（已 patch）、`chrome-mcp-wsl-windows/scripts/patch-mcp-rpc-lock.py`（可重複執行）
- 更新 index.md: 無（條目已存在）
