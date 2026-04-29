---
title: CME 即時數據訂閱方案與費用
created: 2026-04-28
updated: 2026-04-28
type: resource
tags: [trading, mnq, resource, technical-analysis]
sources:
  - cmegroup.com/market-data
  - insigniafutures.com/cme-data-fees
  - interactivebrokers.com/en/pricing/market-data-pricing.php
  - databento.com/pricing
---

# CME 即時數據訂閱方案與費用

> 查詢日期：2026-04-28。價格可能隨時間變動。

## 背景

為了讓 Hermes Agent 能即時看到 MNQ 盤面狀況（價位、技術指標），需要 CME 市場數據來源。以下是各種方案的比較，從最便宜到最貴排列。

---

## 方案比較總表

| 方案                           |      月費       | 即時性  |   API 可串接    | 說明                         |
| ---------------------------- | :-----------: | :--: | :----------: | -------------------------- |
| **Binance NAS100 永續合約**      |    **$0**     | ✅ 即時 | ✅ WebSocket  | 跟 CME MNQ 高度連動，價差 tracking |
| **IBKR 美國證券+期貨 Bundle**      | **$10**（佣金可抵） | ✅ 即時 | ✅ Python API | 需 IBKR 帳戶，最便宜的真 CME 數據     |
| **Insignia Futures Level 1** |    **$9**     | ✅ 即時 |    ❌ 僅平台看    | 純報價無 API                   |
| **CME Direct 官方直連**          |  ~**$43/月**   | ✅ 即時 |    ⚠️ 需另建    | 官方非專業方案，API 需額外開發          |
| **Databento Standard**       |  **$179/月**   | ✅ 即時 | ✅ Python SDK | 純 API，含 15 年歷史，免券商         |
| **Polygon.io**               | **$49-199/月** | ✅ 即時 |  ✅ REST/WS   | 方案彈性                       |

---

## 詳細說明

### 一、Binance NAS100 永續合約 — 免費 🆓

- **費用：$0**
- **資料：** Binance 的 NAS100/USD 永續合約即時報價
- **與 MNQ 關係：** 高度連動但存在價差（spread difference），可量化 tracking
- **串接方式：** Python + Binance WebSocket API，每秒接收即時 tick
- **優點：** 完全免費、即時、可自行計算 KDJ/PPO/EMA
- **缺點：** 不是 CME 官方數據，價差在極端波動時可能擴大

### 二、Interactive Brokers — $10/月（佣金可抵）💎 推薦

- **方案：** US Securities Snapshot and Futures Value Bundle
- **費用：** $10/月（若每月佣金 $30+ 可折抵）
- **資料：** Level 1（best bid/ask, last price, volume, OHLC），涵蓋 CME 期貨
- **串接方式：** `ib_insync` Python library → WebSocket streaming
- **優點：** 最便宜的真 CME 數據、成熟 API、可同時拿多個商品報價
- **缺點：** 需要開 IBKR 帳戶並入金
- **非專業 vs 專業：** 個人交易者適用非專業費率（需符合定義）

### 三、Insignia Futures — $9/月（純報價）

- **費用：** Level 1 $9/月（4 個交易所捆綁），Level 2 $41/月
- **資料：** CME/CBOT/NYMEX/COMEX 非專業費率
- **限制：** 僅限平台內看報價，無公開 API 可程式化串接
- **用途：** 如果只是要在平台看盤不適合本需求

### 四、CME Direct 官方直連 — ~$43/月

- **費用明細：**
  - Non-Professional Top of Book（4 交易所捆綁）：$4.65/月
  - Non-Display API（Category A 單一自然人）：$38/月
  - **合計：約 $43/月**
- **資料：** CME Globex MDP 3.0 原生數據
- **優點：** 官方直連、數據最權威
- **缺點：** 需要 CME Direct 帳戶、API 開發門檻較高

### 五、Databento — $179/月 🚀

- **方案：** Standard 方案（2025 年新推出）
- **費用：** $179/月
- **資料：** CME Globex MDP 3.0 完整數據，含 15 年歷史（650,000+ 期貨/選擇權）
- **串接方式：** Python SDK，簡單幾行程式碼即可串流
- **優點：** 最成熟的 CME 數據 API、不需券商帳戶、歷史+即時一條龍
- **缺點：** 價格較高

### 六、Polygon.io — $49-199/月

- **方案：** 依 API 調用次數分級
- **費用：** 約 $49-199/月，期貨即時數據需較高方案
- **串接方式：** REST API + WebSocket

---

## 實作建議（給 Agent 自己看）

如果要將即時數據導入 Hermes Agent 做盤中監控：

```python
# 推薦架構（IBKR 方案）
# 背景進程：ib_stream.py
from ib_insync import *
import json, time

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

contract = Futures('MNQ', 'CME', '20260619')
ib.reqMktData(contract, '', False, False)

def onPendingTickers(tickers):
    for t in tickers:
        state = {
            'time': time.time(),
            'last': t.last,
            'bid': t.bid,
            'ask': t.ask,
            'volume': t.volume,
            'high': t.high,
            'low': t.low
        }
        with open('/tmp/mnq_state.json', 'w') as f:
            json.dump(state, f)

ib.pendingTickersEvent += onPendingTickers
ib.run()
```

此架構可與 cron job 搭配：cron 每 1-3 分鐘讀 `/tmp/mnq_state.json`，比對前次狀態，有變化才觸發分析。
