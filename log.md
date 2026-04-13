---
name: log
description: "Chronological record of all wiki actions"
version: 1.1.0
updated: 2026-04-13
---

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
