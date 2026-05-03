---
title: Chrome MCP WSL 連線設定
created: 2026-05-03
updated: 2026-05-03
type: entity
tags: [hermes-agent, chrome, mcp, wsl, workflow, setup-guide]
sources: []
confidence: high
---

# Chrome MCP：從 WSL 連線到 Windows Chrome

> 連線 Hermes Agent（WSL 中執行）到 Windows 主機上正在使用的 Chrome 瀏覽器，透過 `chrome-devtools-mcp` 實現 AI 直接操控 Chrome 分頁。

## 背景

Hermes Agent 在 WSL2 中執行，Chrome 在 Windows 主機上執行。兩者不在同一網路命名空間中，因此需要以下橋接：

1. **Windows** 防火牆規則（允許連入）
2. **Chrome** 遠端除錯功能（UI toggle）
3. **Portproxy**（將 Windows 127.0.0.1 綁定的埠轉發到外部）
4. **WebSocket 端點**（Chrome 144+ 使用 WebSocket 而非傳統 HTTP CDP）

## 總體連線架構

```
WSL Hermes Agent
  │
  ├─ ws-endpoint.sh (動態讀取 DevToolsActivePort)
  │    │
  │    └─ /root/.hermes/node/bin/chrome-devtools-mcp
  │         │
  │         └─ ws://172.27.16.1:PORT/devtools/browser/UUID  (WebSocket)
  │              │
  │              ▼
  └─ Windows Host (172.27.16.1:PORT)
       │
       ├─ netsh portproxy: 0.0.0.0:PORT → 127.0.0.1:PORT
       │
       └─ Chrome DevTools Server (127.0.0.1:PORT)
```

## 設定步驟

### 1. 開啟 Chrome 遠端除錯

Chrome 144+ 不需要 `--remote-debugging-port` CLI 參數。只需：
- 在 Chrome 網址列輸入 `chrome://inspect/#remote-debugging`
- 勾選 **「Allow remote debugging for this browser instance」**
- 確認顯示 `Server running at: 127.0.0.1:PORT`

### 2. 安裝 chrome-devtools-mcp（WSL 端）

```bash
npm install -g chrome-devtools-mcp
```

### 3. 建立 Windows 防火牆規則（管理員身分 PowerShell）

```powershell
netsh advfirewall firewall add rule name="Chrome MCP WSL" dir=in protocol=tcp localport=9222 action=allow
```

這個防火牆規則只需要建立一次。

### 4. 建立 Portproxy（每個 Chrome port 都需要）

Chrome 的除錯埠每次啟動可能不同。從 `DevToolsActivePort` 取得目前 port：

```powershell
# 先確認目前 port
Get-Content "C:\Users\<username>\AppData\Local\Google\Chrome\User Data\DevToolsActivePort"
# 第一行是 port，第二行是 WebSocket 路徑

# 建立 portproxy（管理員身分）
netsh interface portproxy add v4tov4 listenport=<PORT> listenaddress=0.0.0.0 connectport=<PORT> connectaddress=127.0.0.1
```

> ⚠️ 每次切換 Chrome profile 或重啟 Chrome 後 port 都可能變動，需要重新執行此命令。

### 5. WSL 的 ws-endpoint.sh 包裝腳本

路徑：`/root/.hermes/scripts/ws-endpoint.sh`

```bash
#!/bin/bash
DEVPORT_FILE="/mnt/c/Users/denny/AppData/Local/Google/Chrome/User Data/DevToolsActivePort"
if [ -f "$DEVPORT_FILE" ]; then
    PORT=$(head -1 "$DEVPORT_FILE")
    WSPATH=$(tail -1 "$DEVPORT_FILE")
    WS_IP=$(grep nameserver /etc/resolv.conf | awk '{print $2}')
    exec /root/.hermes/node/bin/chrome-devtools-mcp \
        --wsEndpoint "ws://${WS_IP}:${PORT}${WSPATH}" \
        --no-category-network \
        --no-category-performance \
        --no-usage-statistics \
        "$@"
else
    echo "DevToolsActivePort not found" >&2
    exit 1
fi
```

此腳本會：
- 動態讀取 Windows 端 Chrome 的 `DevToolsActivePort` 檔案（透過 `/mnt/c/` 存取）
- 自動取得目前 port 與 WebSocket UUID
- 取得 WSL gateway IP（即 Windows 主機的虛擬網路位址）
- 組合成完整的 WebSocket URL 傳給 chrome-devtools-mcp

### 6. Hermes Agent MCP 設定

在 `~/.hermes/config.yaml` 中加入：

```yaml
mcp_servers:
  chrome:
    command: bash
    args:
      - /root/.hermes/scripts/ws-endpoint.sh
```

### 7. 啟用連線

在 Hermes session 中輸入：

```
/reload-mcp
```

確認工具載入後即可操控：

| 工具 | 功能 |
|------|------|
| `mcp_chrome_list_pages` | 列出所有分頁 |
| `mcp_chrome_select_page` | 切換到指定分頁 |
| `mcp_chrome_navigate_page` | 導航到新 URL |
| `mcp_chrome_click` | 點擊網頁元素 |
| `mcp_chrome_fill` | 填寫表單欄位 |
| `mcp_chrome_take_snapshot` | 取得頁面文字快照 |
| `mcp_chrome_take_screenshot` | 截取頁面截圖 |
| `mcp_chrome_new_page` | 開新分頁 |
| `mcp_chrome_close_page` | 關閉分頁 |
| `mcp_chrome_evaluate_script` | 執行 JavaScript |
| `mcp_chrome_list_console_messages` | 檢視主控台訊息 |

## 關鍵技術細節

### WebSocket 而不是 HTTP

Chrome 144+ 的 `chrome://inspect/#remote-debugging` toggle 產生的除錯伺服器**不走傳統的 CDP HTTP 端點**（`/json/version`、`/json/list` 等回傳 404），而是直接使用 WebSocket 協定。

在 `DevToolsActivePort` 檔案中：
- 第 1 行：port 號碼（如 `54096`）
- 第 2 行：WebSocket 路徑（如 `/devtools/browser/uuid`）

完整 WebSocket URL 格式：
```
ws://<WINDOWS_IP>:<PORT>/devtools/browser/<UUID>
```

### WSL2 網路特性

WSL2 使用虛擬網路介面，Windows 主機的 IP 可從 `/etc/resolv.conf` 的 `nameserver` 取得（通常是 `172.xx.x.1` 格式）。

WSL2 的 `localhost` 指向 WSL 虛擬機本身，**不指向 Windows 主機**。因此連線 Windows 服務必須使用 Windows IP 或透過 portproxy。

### 分頁過多時的超時問題

當 Chrome 開啟大量分頁（20+），chrome-devtools-mcp 在初始化時執行的 `Network.enable` 命令會因遍歷所有分頁而超時。

解決方案：
- `--no-category-network`：跳過 Network 域的啟用
- `--no-category-performance`：跳過 Performance 域的啟用
- `--slim`：僅暴露導航、截圖、JS 執行三個核心工具（最輕量）

## 已知問題與注意事項

| 問題 | 說明 | 解決方案 |
|------|------|----------|
| Port 變動 | Chrome 重啟或切換 profile 後 debug port 會變 | 重新執行 portproxy 命令 + `/reload-mcp` |
| UUID 變動 | Chrome 重啟後 WebSocket UUID 改變 | `ws-endpoint.sh` 動態讀取，無需手動處理 |
| Network.enable 超時 | 分頁過多時初始化超時 | `--no-category-network` 旗標 |
| 安全提醒 | 遠端除錯開啟後，外部應用可完整控制瀏覽器 | 僅在可信環境使用 |

## 參考連結

- chrome-devtools-mcp (npm) — 預設的 Hermes skill（`chrome-mcp-wsl-windows`）
- Chrome DevTools MCP：https://github.com/ChromeDevTools/chrome-devtools-mcp
- Hermes MCP 設定：https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
