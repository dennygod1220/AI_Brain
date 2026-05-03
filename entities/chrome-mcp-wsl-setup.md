---
title: Chrome MCP WSL 連線設定
created: 2026-05-03
updated: 2026-05-03-2
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
| **_rpc_lock 死結（已修復）** | Hermes 重啟後所有 chrome MCP tool call 全部 timeout | 見下方「_rpc_lock 死結問題詳解」 |
| 安全提醒 | 遠端除錯開啟後，外部應用可完整控制瀏覽器 | 僅在可信環境使用 |

---

## `_rpc_lock` 死結問題詳解（2026-05-03 發現並修復）

### 問題症狀

Hermes Agent session 重啟後，`mcp_chrome_list_pages` 以及所有其他 chrome MCP tool call 全部**無限 hang 住**，最終在 **120 秒後**回傳 `MCP call failed: TimeoutError`。

### 環境

- Hermes Agent（WSL2）
- chrome-devtools-mcp v0.23.0（Node.js）
- Windows 11 Chrome 147+
- MCP Python SDK 1.27.0

### 診斷過程

#### 測試 1：chrome-devtools-mcp 直接運作 ✅

手動透過 stdio pipe 執行 chrome-devtools-mcp 並發送 JSON-RPC request，**0.5 秒內正常回應**，24 個 tools 全部可呼叫。

```bash
/root/.hermes/node/bin/chrome-devtools-mcp \
  --wsEndpoint "ws://172.27.16.1:52785/devtools/browser/..." \
  --no-category-network --no-category-performance
# → tools/list: 0.5s, tools/call list_pages: 3.3s
```

#### 測試 2：hermes mcp test chrome 成功 ✅

```bash
hermes mcp test chrome
# ✓ Connected (833ms)
# ✓ Tools discovered: 24
```

獨立測試 session 完全正常。

#### 測試 3：WebSocket 連線穩定性 ✅

直接 Python CDP WebSocket 連線，開著等 **60 秒 idle** 後再發命令，**完全正常**：

```
Browser.getVersion → "Chrome/147.0.7727.138" (idle 60s 後仍正常)
```

排除 portproxy 連線不穩定的可能性。

#### 測試 4：完整的 MCP 初始化流程 ✅

手動模擬 Hermes 的完整 MCP 連線流程（initialize → notifications/initialized → tools/list → tools/call list_pages），正常完成。

#### 測試 5：問題重現 🔴

在 Hermes session 內呼叫 `mcp_chrome_list_pages`，回傳 `TimeoutError`（空訊息）。此時檢查：

| 狀態 | 結果 |
|------|------|
| MCP 子進程 | 存活（PID 1583420，fd 0/1 pipe 正常） |
| WebSocket socket | ESTABLISHED（fd 21 → 172.27.16.1:52785） |
| agent.log | "registered 28 tool(s)" 成功 |
| errors.log | "MCP tool chrome/list_pages call failed: "（空訊息） |

### 根因分析

#### 抓到了：`_rpc_lock` 死結

Hermes 的 MCP 客戶端程式碼在 `/root/.hermes/hermes-agent/tools/mcp_tool.py` 中有一個 `_rpc_lock`（`asyncio.Lock()`），用來序列化所有對 MCP 子程序的 JSON-RPC 請求：

```python
# tools/mcp_tool.py line 2024-2026
async def _call():
    async with server._rpc_lock:
        result = await server.session.call_tool(tool_name, arguments=args)
```

同時，MCP SDK 支援 notification 處理機制。當 chrome-devtools-mcp 初始化完成後，會發送 `ToolListChangedNotification` 給客戶端：

```python
# tools/mcp_tool.py line 932-966 — message handler
case ToolListChangedNotification():
    self._schedule_tools_refresh()  # 建立 background task
```

背景 task 執行時會呼叫 `_refresh_tools()`，而這個方法**也持有 `_rpc_lock`**：

```python
# tools/mcp_tool.py line 982-984 (修復前)
async with self._rpc_lock:
    tools_result = await self.session.list_tools()
```

**關鍵問題**：`session.list_tools()` 沒有 timeout。如果它 hang 住（在背景 context 中確實會發生 — 推測與 MCP SDK 的 `_receive_loop` 競爭條件有關），`_rpc_lock` 就永遠不釋放。所有後續的 `session.call_tool()` 都在 `async with server._rpc_lock` 這一行死等，直到 Hermes 的 120 秒外層 timeout 炸掉。

#### 發生時序

```
Hermes 啟動
  │
  ├─ _run_stdio() 啟動 MCP 子進程
  │    │
  │    ├─ session.initialize()  ✓
  │    ├─ _discover_tools() → list_tools()  ✓ (tools 註冊成功)
  │    │     └─ 此時 chrome-devtools-mcp 發出 ToolListChangedNotification
  │    │           └─ message handler 排程 _schedule_tools_refresh()
  │    │                 └─ background task 排隊中...
  │    ├─ _ready.set()
  │    └─ _wait_for_lifecycle_event()
  │
  ├─ [背景 task 開始執行]
  │    └─ _refresh_tools() 取得 _rpc_lock
  │         └─ session.list_tools()  →  HANG ❌
  │              └─ _rpc_lock 永遠被持有
  │
  └─ 使用者發送 mcp_chrome_list_pages
       └─ _call() → async with _rpc_lock → 永遠等待 ❌
            └─ 120 秒後 → TimeoutError
```

### 修復方式

#### 修改內容

在 `/root/.hermes/hermes-agent/tools/mcp_tool.py` 的 `_refresh_tools()` 中，對 `session.list_tools()` 加上 **15 秒 timeout**：

```python
# 修復後 (mcp_tool.py ~line 982)
async with self._rpc_lock:
    try:
        tools_result = await asyncio.wait_for(
            self.session.list_tools(), timeout=15,
        )
    except asyncio.TimeoutError:
        logger.warning(
            "MCP server '%s': tool refresh timed out — "
            "releasing _rpc_lock so tool calls can proceed",
            self.name,
        )
        return
```

#### 原理

- 如果 `list_tools()` 在背景 context 下 hang 住，15 秒後 timeout
- timeout 後 `_rpc_lock` 正常釋放（`async with` block 結束）
- 後續的 tool call 可以正常取得 lock 並執行
- background refresh 失敗只是暫時的 — 下次 notification 到來時會再觸發

#### 重新套用（Hermes 更新後）

Hermes 更新（`git pull`）會覆蓋 `mcp_tool.py`。重新套用 patch：

```bash
python3 /root/.hermes/profiles/stock_master/skills/my-hermes-skills/chrome-mcp-wsl-windows/scripts/patch-mcp-rpc-lock.py
```

這個 script 會偵測 patch 是否已套用，避免重複修改。

### 相關檔案

| 檔案 | 用途 |
|------|------|
| `entities/chrome-mcp-wsl-setup.md` | 本文件 — Chrome MCP 設定 + 已知問題 |
| `/root/.hermes/hermes-agent/tools/mcp_tool.py` | Hermes MCP 客戶端（已 patch） |
| skills `chrome-mcp-wsl-windows/scripts/patch-mcp-rpc-lock.py` | 可重複執行的 patch script |
| skills `chrome-mcp-wsl-windows/SKILL.md` | 技能文件（Known Issues 章節） |

## 參考連結

- chrome-devtools-mcp (npm) — 預設的 Hermes skill（`chrome-mcp-wsl-windows`）
- Chrome DevTools MCP：https://github.com/ChromeDevTools/chrome-devtools-mcp
- Hermes MCP 設定：https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
