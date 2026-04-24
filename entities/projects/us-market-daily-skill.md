---
name: us-market-daily-skill
description: "Hermes cron skill：每日美股事件 Discord 推送"
version: 1.0.0
created: 2026-04-23
updated: 2026-04-23
type: project
tags: [project, hermes-skill, discord, python, finviz, cron]
sources:
  - concepts/us-market-daily-skill-development.md
---

# 美股事件每日 Discord 推送

## 概述

Hermes cron skill，每天自動抓取並推送美股重要事件到 Discord。

## 推送時間

| 時段 | Cron | 台灣時間 |
|------|------|---------|
| 早報 | `0 22 * * *` | 06:00 |
| 午報 | `0 9 * * *` | 17:00 |

## 涵蓋內容

- **Fed/FOMC 動態**：政策聲明、官員演講、Fed Balance Sheet
- **重量級財報**：AAPL、MSFT、NVDA、AMZN、META、GOOGL、TSLA、SPY
- **經濟數據**：GDP、CPI、Jobs Report、NFP、PMI、Retail Sales 等（importance ≥ 2）

## 核心技術棧

- **資料來源**：finviz.com（HTML 内嵌 JSON）+ yfinance
- **推送方式**：Hermes `send_message`（不走 Webhook）
- **Python 環境**：`/usr/bin/python3`（系統 Python，無 venv）

## 關鍵技術決策

1. **finviz HTML JSON 解析**：不走 JS 動態 AJAX，直接 regex 提取 `<script>` 中的 `window.fc_data.entries`
2. **UTC/ET 時區跨日**：`_date_in_window()` 把窗口擴大到「目標日期 + 前一天 16:00 ET 以後」
3. **Fed 事件嚴格分類**：ticker 白名單 `{"FDTR", "UNITEDSTACENBANBALSH"}`，排除含 "Fed" 字樣的經濟指標

## 相關檔案

- 技能目錄：`~/.hermes/skills/my-hermes-skills/us-market-daily/`
- 開發過程：[[concepts/us-market-daily-skill-development]]
