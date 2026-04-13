# Hermes Gateway 系統服務 (Systemd) 修復報告

## 1. 問題現象
在執行 `hermes gateway restart --system` 後，主 Agent 的 Gateway 服務無法啟動，並在系統日誌中出現以下錯誤：
`ModuleNotFoundError: No module named 'yaml'`

## 2. 根本原因分析
### Python 版本衝突
- **系統預設 Python**：`3.12.3` (位於 `/usr/bin/python3`)
- **服務偵錯路徑**：服務試圖執行 `/root/.local/share/uv/python/cpython-3.11.15-linux-x86_64-gnu/bin/python3.11`

### 為什麼會發生？
1. **UV 套件管理員**：Hermes 內部使用了 `uv` 工具，它下載了一個獨立的 `3.11` 版本的 Python 用於特定內部任務。
2. **CLI 產生 Bug**：當你使用 `hermes gateway start/restart --system` 指令時，Hermes 的程式碼邏輯誤抓了這個「純淨的」`3.11` 路徑來建立 Systemd 設定檔，而不是使用已經安裝好所有套件的虛擬環境 (`venv`)。
3. **缺少套件**：這個 `uv` 管理的 `3.11` 只是基礎環境，並沒有安裝 Hermes 執行所需的 `PyYAML`, `discord.py` 等套件，因此導致 `ModuleNotFoundError`。

## 3. 已執行的修復方案
為了確保服務能穩定運行並減少被 Hermes CLI 再次覆蓋的風險，我們執行了以下動作：

1. **手動修正路徑**：將 `/etc/systemd/system/hermes-gateway.service` 中的 `ExecStart` 指向正確的虛擬環境：
   `ExecStart=/root/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run --replace`

2. **建立持久化覆蓋 (Systemd Override)**：
   建立設定檔：`/etc/systemd/system/hermes-gateway.service.d/python-override.conf`
   內容強制鎖定 `ExecStart` 使用虛擬環境的 Python。

## 4. 後續建議
- **避免使用 --system**：如果不需要全系統權限，建議直接使用 `hermes gateway restart` (不帶參數)，這會以當前使用者身份執行 User Service，通常較不容易出錯。
- **手動修復指令**：如果未來執行 `--system` 指令後發現服務又掛掉了，可以執行以下指令一鍵修復：
  ```bash
  sudo sed -i 's|ExecStart=.*/python3\.11 -m hermes_cli\.main gateway run|ExecStart=/root/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run|' /etc/systemd/system/hermes-gateway.service && sudo systemctl daemon-reload && sudo systemctl restart hermes-gateway.service
  ```

---
*文件紀錄時間：2026-04-13*
