---
title: "美股事件每日 Discord 推送 — 開發過程記錄"
name: us-market-daily-skill-dev
description: "美股事件每日 Discord 推送 skill 建置過程：技術決策、bug 修復架構記錄"
version: 1.0.0
created: 2026-04-23
updated: 2026-04-23
type: concept
tags: [project, workflow, hermes-skill, discord, python, finviz]
sources: []
---

# 美股事件每日 Discord 推送 — 開發過程記錄

## 目的

建立一個 Hermes cron skill，每天台灣時間 06:00 和 17:00 自動抓取美股重要事件（Fed/FOMC 動態、重量級財報、經濟數據），格式化後推送到 Discord 頻道。

## 約束條件

- **Discord 頻道 ID 不寫死**：透過環境變數 `DISCORD_CHANNEL_ID` 配置，預設 `1496298887714046216`
- **Python 環境統一**：`/usr/bin/python3`（WSL 系統 Python），不走 venv，避免 cron 與終端環境不一致
- **財報名單精簡**：只追蹤真正撼動 S&P 500 的核心巨頭 — AAPL、MSFT、NVDA、AMZN、META、GOOGL、TSLA、SPY
- **Fed 事件嚴格定義**：ticker=`FDTR`（Fed 政策聲明/官員演講），加上 `UNITEDSTACENBANBALSH`（Fed Balance Sheet）
- **經濟數據門檻**：只留 importance ≥ 2，並排除國債標售、區域 Fed 指數等干擾
- **不走 Discord Webhook**：直接用 Hermes `send_message` 推送

---

## 第一層：資料來源決策

### 為什麼用 finviz.com？

一開始考慮過多個資料來源：

| 來源 | 優點 | 缺點 |
|------|------|------|
| Yahoo Finance Calendar API | 免費 | 不穩定，EPS 預估有限 |
| Investing.com | 資料完整 | 需要登入/付費，爬蟲風險高 |
| Finviz.com | 免費、HTML 内嵌 JSON、importance 欄位清晰 | JS 動態載入，不能直接爬 HTML 表格 |

最終選擇 finviz，代價是需要從 HTML 的 `<script>` 標籤中用 regex 提取 JSON。

### 為什麼用 yfinance 查財報 EPS？

yfinance 可以抓到 Yahoo Finance 的 EPS 預估資料，缺點是延遲（約 15-20 分鐘）。但對每日早報來說可接受。

---

## 第二層：核心技術問題與修復

### Bug 1：finviz HTML 是 JS 動態渲染

**現象**：直接 `requests.get(finviz.com/calendar.ashx)` 回傳的 HTML 裡沒有行事曆資料，表格是空的。

**原因**：finviz 的行事曆資料不是 AJAX API，而是直接埋在 HTML 的 `<script>` 標籤中的 JSON：
```html
<script>
  window.fc_data = {"data":{"initialDateFrom":"...","entries":[...]}}
</script>
```

**修復**：用 regex 找到 `"entries":[` 開始位置，再手動對括號計數找到匹配的 `]`，取出 JSON 陣列。

```python
def _extract_finviz_entries(html: str) -> list:
    start = html.find('"entries":[')
    if start == -1:
        return []
    depth = 0
    i = start + len('"entries":[')
    while i < len(html):
        ch = html[i]
        if ch == '[':   depth += 1
        elif ch == ']':
            if depth == 0: break
            depth -= 1
        i += 1
    json_str = '[' + html[start + len('"entries":['):i] + ']'
    return json.loads(json_str)
```

---

### Bug 2：時區跨日導致 Initial Jobless Claims 消失

**現象**：早上推送時，Initial Jobless Claims（20:30 ET）常常不在清單中，但明明那天有這個數據。

**原因**：finviz 的 date 是 UTC 時間。例如 IJC 在美東時間 4/22 20:30 發布，UTC 時間是 `2026-04-23T08:30:00Z`。而 cron 在台灣 06:00（UTC 前一天 22:00）執行，查的是「美東當天 4/23」的行事曆。UTC 0:00 = ET 前一天 20:00，所以 IJC 的 UTC 08:30 已經是 ET 前一天的 20:30，落在「目標日的前一天」，被 `date_et == '2026-04-23'` 這個比對擋掉了。

**修復**：加入 `_date_in_window()` 函式，把窗口擴大到「目標日期全天 + 前一天 16:00 ET 以後」：

```python
def _date_in_window(dt_et: datetime, target_date: str, include_prior_evening: bool = True) -> bool:
    target = datetime.strptime(target_date, "%Y-%m-%d").date()
    event_date = dt_et.date()
    if event_date == target:
        return True
    if include_prior_evening:
        prior_date = target - timedelta(days=1)
        if event_date == prior_date and dt_et.hour >= 16:  # 16:00 ET = 盤後
            return True
    return False
```

---

### Bug 3：Fed Balance Sheet 被錯誤分類

**現象**：`UNITEDSTACENBANBALSH`（Fed Balance Sheet）一開始被歸在 `economic_data` 列表中，但 importance=1，會被 `imp < 2` 的規則過濾掉。

**原因**：Fed Balance Sheet 的 ticker 不在黑名單中，所以進入了經濟數據的處理邏輯。但它重要性只有 1，而經濟數據只留 imp≥2。

**修復**：
1. 把 Fed Balance Sheet 從 `economic_data` 分離，加入 `fetch_fed_events()` 的白名單
2. 在 `fetch_economic_data()` 中明確將其加入 `skipped_tickers`
3. Fed Balance Sheet 永遠保留（不受 imp 限制）

---

### Bug 4：IJCUSA 被錯誤放進 Fed Events

**現象**：含 "Fed" 字樣的經濟指標（如 IJCUSA、某區域 Fed 指數）被錯誤識別為 Fed 事件。

**原因**：一開始用 `ticker in ["FDTR"]` 或簡單的字串包含 "Fed" 來判斷。

**修復**：用严格的 ticker 白名單，只有 `FDTR` 和 `UNITEDSTACENBANBALSH` 才算 Fed 事件：

```python
FED_TICKERS = {"FDTR", "UNITEDSTACENBANBALSH"}
```

並在 `fetch_economic_data()` 的 `skipped_tickers` 中排除所有區域 Fed 指數（USAKFCI、UNITEDSTAKFMI、UNITEDSTACONJOBCLA 等）。

---

## 第三層：架構決策

### 為什麼不走 Discord Webhook？

Hermes 已有 `send_message` 功能，直接推送不需要另外設定 Webhook URL。且 Webhook 無法指定頻道（只能發到 Webhook 設定的頻道），用 `send_message` 可以動態指定頻道 ID。

### 為什麼用 `/usr/bin/python3` 而不是 venv？

Hermes cron job 在獨立的 session 執行，venv 的路徑綁定在 shell profile 載入邏輯上，容易造成「終端能執行、cron 不能執行」的問題。系統 Python 路徑固定，減少環境不一致的風險。

### Cron 排程

| Job | Cron 表達式 | 台灣時間 | 用途 |
|-----|------------|---------|------|
| us-market-daily-morning | `0 22 * * *` | 06:00 | 開盤前早報 |
| us-market-daily-afternoon | `0 9 * * *` | 17:00 | 盤中補充 |

---

## 最終檔案結構

```
~/.hermes/skills/my-hermes-skills/us-market-daily/
├── SKILL.md                          # 技能說明文件
├── scripts/
│   ├── config.py                     # 設定檔（WATCHED_TICKERS, DISCORD_CHANNEL_ID）
│   ├── fetch_events.py               # 資料抓取主程式
│   │   ├── _extract_finviz_entries() # HTML embedded JSON 解析
│   │   ├── _parse_finviz_entry()     # 標準化 entry
│   │   ├── _date_in_window()         # 日期窗口判斷（含跨日）
│   │   ├── fetch_fed_events()        # Fed/FOMC 事件
│   │   ├── fetch_economic_data()     # 經濟數據（imp≥2 + 黑名單）
│   │   └── fetch_earnings()          # yfinance 財報 EPS
│   └── formatters.py                  # Discord 訊息格式化
└── references/
    └── DISCORD_TEMPLATE.md            # 訊息格式範本
```

---

## 關鍵技術筆記

### finviz JSON 格式

```json
{
  "date": "2026-04-23T08:30:00Z",  // UTC 時間
  "ticker": "IJCUSA",
  "event": "Initial Jobless Claims",
  "category": "Leading Indicators",
  "importance": 2,                   // 1/2/3
  "previous": "208K",
  "forecast": "212K",
  "actual": ""
}
```

### 時區對照

| 事件時間 | ET（美東） | UTC | 台灣 |
|---------|-----------|-----|------|
| IJC 發布 | 20:30 ET | 00:30+1Z | 08:30 |
| Fed Balance Sheet | 04:30 ET | 08:30Z | 16:30 |
| PMI Flash | 09:45 ET | 14:45Z | 22:45 |

### Fed 事件 ticker 白名單

| Ticker | 事件 | 說明 |
|--------|------|------|
| `FDTR` | Fed Funds Target Rate | Fed 政策利率，核心 Fed 事件 |
| `UNITEDSTACENBANBALSH` | Fed Balance Sheet | 量化緊縮/寬鬆信號 |

---

## 待優化方向

1. **財報公佈時間**：目前用 yfinance calendar 的小時判斷 BMO/AMC，但 finviz 的財報事件也有精確時間，未來可以整合
2. **前值/預期值的快取**：yfinance 的前值/預期值有時抓不到，可以考慮從 finviz 的經濟數據直接取得
3. **市場假日偵測**：目前 config.py 寫死假日清單，未來可以自動判斷（NYSE holiday calendar）
4. **下午報的內容差異**：目前早報和午報格式相同，未來午報可以只推送已確認的數據（actual 值）

專案實體頁面：[[entities/projects/us-market-daily-skill]]
