---
title: Hermes Gateway Systemd Fix
created: 2026-04-13
updated: 2026-04-13
type: entity
tags: [Hermes, Discord, Systemd, Python, Bug-Fix]
sources: [_archive/raw/Hermes_Gateway_Fix_Summary.md]
---

# Hermes Gateway Systemd Fix

## Overview
2026-04-13 修復 Hermes Gateway 服務在執行 `hermes gateway restart --system` 後無法啟動的問題。

## 問題現象
執行 `hermes gateway restart --system` 後，Gateway 服務崩潰，系統日誌出現：
`ModuleNotFoundError: No module named 'yaml'`

## 根本原因
1. **UV Python 路徑衝突**：Hermes 內部使用 `uv` 下載獨立的 CPython 3.11，但服務嘗試用這個乾淨的 3.11 執行，而非已安裝所有依賴的 venv。
2. **CLI 產生 Bug**：`--system` 參數讓 CLI 抓錯 Python 路徑，導致 Systemd 服務檔指向無依賴的 `uv` Python。

## 修復步驟
1. 手動修正 `/etc/systemd/system/hermes-gateway.service` 中 `ExecStart` 指向正確 venv：
   `/root/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run --replace`
2. 建立持久化覆蓋：`/etc/systemd/system/hermes-gateway.service.d/python-override.conf`

## 未來建議
- 避免使用 `--system` 參數，改用 `hermes gateway restart`（User Service）
- 一鍵修復指令：
  `sudo sed -i 's|ExecStart=.*/python3\\.11 -m hermes_cli\\.main gateway run|ExecStart=/root/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run|' /etc/systemd/system/hermes-gateway.service && sudo systemctl daemon-reload && sudo systemctl restart hermes-gateway.service`

## 相關頁面
- [[concepts/safe-execution-workflow]] — 安全執行工作流（含 Systemd 日誌處理）
- [[entities/hermes/hermes-multiagent-discord-system]] — 多 Agent Discord 系統
