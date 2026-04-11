---
name: log
description: "Chronological record of all wiki actions"
version: 1.0.1
updated: 2026-04-12
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

## [2026-04-12] fix | 修復重複檔案：illustrious-prompt-generation-strategy
- 刪除空白的 concepts/illustrious-prompt-generation-strategy.md
- 將 entities/concepts/illustrious_prompt_generation_strategy.md 內容合併至正確位置
- 新增完整 Frontmatter（SCHEMA v1.1.1 規範）
- 刪除錯誤的 entities/concepts/ 目錄
- 更新 index.md (v1.0.2)，更新 log.md
