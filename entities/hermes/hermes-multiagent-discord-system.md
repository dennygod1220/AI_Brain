---
title: Hermes Multi-Agent Discord System
created: 2026-04-13
updated: 2026-04-13
type: entity
tags: [Hermes, Discord, Multi-Agent, Bot, Discord.py]
sources: [_archive/raw/Hermes_Discord_Mod_Guide.md, _archive/raw/Hermes_MultiAgent_Fix_Report.md, _archive/raw/hermes_multiagent_discord.patch]
---

# Hermes Multi-Agent Discord System

## Overview
Hermes 雙 Agent（主 Agent 蝦蝦 + 本地 Agent 小低能）在 Discord 環境下的通訊障礙修復總結。涵蓋 6 階段修復歷程與 3 大核心代碼修改。

## 修復歷程

### 階段一：底層通訊架構
| 問題 | 根因 | 解法 |
|------|------|------|
| Bot 訊息靜音 | Discord Adapter 預設過濾 Bot 訊息 | 設定 `DISCORD_ALLOW_BOTS=mentions`，雙方 ID 互加至 `DISCORD_ALLOWED_USERS` |
| Systemd 啟動崩潰 | UV Python 路徑衝突 | 建立 Systemd Override，綁定正確 venv Python |

### 階段二：標記偵測與討論串邀請
| 問題 | 根因 | 解法 |
|------|------|------|
| 身分組標記解析失敗 | `on_message` 只看 `mentions` 未看 `role_mentions` | 修改 `discord.py` 增加 Role Mention 比對 |
| 討論串成員資格盲區 | Discord 不會自動拉 Bot 進私密討論串 | 在 `_auto_create_thread` 加入 `thread.add_user()` 自動邀請邏輯 |

### 階段三：解決搶話與視覺屏障
| 問題 | 根因 | 解法 |
|------|------|------|
| 雙機搶話 (Crosstalk) | Agent 監聽所有討論串發言 | 嚴格沉默原則：其他 Bot 被標記時，未被標記的自己強制 Return |
| 小模型幻覺 | LLM 角色扮演假裝自己權限受限 | 重寫 `SOUL.md`，強制具體指令 |

## 三大核心修改（discord.py）

### 修改 1：讓 Bot 听懂「身分組 (@Role)」標記
讓 Bot 在收到其他 Bot 傳來的訊息時，正確識別被身分組標記的情況。

核心邏輯：同時檢查 `message.mentions` 與 `message.role_mentions`，並確保自己的身分組在 `role_mentions` 中。

### 修改 2：多 Agent 防搶話過濾器
當訊息中標記了「其他 Bot 或別人的身分組」，且自己未被標記時，強制 Return 丟棄封包。

### 修改 3：討論串自動拉人功能
在 `message.create_thread` 後自動邀請被標記的使用者與身分組成員。

## Patch 檔
代碼補丁位於 `[[_archive/raw/hermes_multiagent_discord.patch]]`。

## 未來協作最佳實踐
1. **單點指揮**：直接 `@蝦蝦` 或 `@小低能` 交付獨立任務
2. **傳遞工作流**：`@小低能，請將該成果展示給 @蝦蝦 繼續處理`

## 相關頁面
- [[concepts/safe-execution-workflow]] — 安全執行工作流
- [[entities/hermes/hermes-gateway-systemd-fix]] — Gateway Systemd 修復
