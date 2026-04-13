# Hermes 多 Agent (Discord) 通訊與教學流程修復報告

本文件總結了修復「主 Agent (蝦搬)」與「本地 Agent (小低能)」之間通訊障礙的完整過程。

## 1. 核心目標
實現主 Agent 與本地 Agent 在 Discord 討論串中的雙向通訊，以便主 Agent 能教導本地 Agent 知識。

---

## 2. 遇到的問題與解決方案

### 問題 A：Bot 訊息靜音 (白名單過濾)
- **現象**：主 Agent 發送標記消息，小低能完全沒有反應，Log 無紀錄。
- **分析**：Hermes 的 Discord Adapter 預設會過濾非白名單內的使用者。Bot 的訊息預設被視為「不可信」。
- **解決方法**：
    - 在兩邊的 `.env` 中設定 `DISCORD_ALLOWED_USERS`，明確放入三方 ID (你、主 Agent、小低能)。
    - 設定 `DISCORD_ALLOW_BOTS=mentions`。

### 問題 B：Gateway 啟動崩潰 (Python 路徑衝突)
- **現象**：執行 `gateway restart` 後，主 Agent 服務掛掉，回報 `ModuleNotFoundError: No module named 'yaml'`。
- **分析**：Systemd 服務在重啟時使用了系統 Python (3.11/3.12)，而非虛擬環境 (venv) 中的 Python，導致找不到依賴庫。
- **解決方法**：
    - 建立 Systemd Override 配置，強制指定 `ExecStart` 為 venv 中的 Python 路徑。
    - 在手動修復時，直接調用 `/root/.hermes/hermes-agent/venv/bin/python`。

### 問題 C：身分組標記解析失敗 (Role Mentions)
- **現象**：標記 `@小低能` 時，小低能無反應。
- **分析**：使用者或 Bot 在標記時，Discord 常自動選擇「身分組 (Role)」標記 (`<@&ID>`) 而非「使用者 (User)」標記。Hermes 原生代碼僅檢查使用者標記。
- **解決方法**：
    - **修改底層代碼**：更新 `gateway/platforms/discord.py`，加入對 `message.role_mentions` 的檢測邏輯。

### 問題 D：討論串成員資格 (Thread Membership)
- **現象**：小低能已連線但仍對討論串訊息無感。
- **分析**：Bot 如果不是討論串的「成員」，就收不到該討論串的事件。標記身分組不會自動讓成員加入討論串。
- **解決方法**：
    - **修改底層代碼**：在 `_auto_create_thread` 建立討論串後，加入「自動邀請」邏輯，強制將訊息中標記的所有對象拉入討論串。

### 問題 E：主 Agent 搶答與主動性不足
- **現象**：主 Agent 在別人被標記時跳出來說話，且不會主動對小低能發起教學。
- **分析**：過濾邏輯不夠嚴謹，且 `SOUL.md` 缺乏明確的跨 Agent 指令。
- **解決方法**：
    - **強化過濾**：更新代碼，若無直接標記自己則絕對沉默。
    - **更新 SOUL.md**：注入「主動教學協議」，要求主 Agent 收到指令後直接對小低能輸出。

---

## 3. 關鍵 ID 參考表
- **JASON**: `873204562079678484`
- **主 Agent (蝦搬)**: `1491405019159724082`
- **小低能 (Local)**: `1493073520421376191`
- **小低能身分組 ID**: `1493073889213939844`

---

## 4. 目錄結構與檔案路徑
- **核心通訊程式碼**: `/root/.hermes/hermes-agent/gateway/platforms/discord.py`
- **主 Agent 協議**: `/root/.hermes/SOUL.md`
- **本地 Agent 配置**: `/root/.hermes/profiles/koboldcpp_local/.env`

---
*報告完成時間：2026-04-13*
