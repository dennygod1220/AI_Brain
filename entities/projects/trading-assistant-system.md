---
name: trading-assistant-system
title: 自動化交易輔助系統
description: "Python 自動化交易輔助系統：市場資料蒐集、技術指標計算、交易策略回測、績效評估與圖表生成"
version: 1.0.0
created: 2026-04-20
updated: 2026-04-26
type: project
tags: [Trading, Python, Backtesting, TechnicalAnalysis, QuantitativeFinance, Automation]
sources: [/root/.hermes/profiles/koboldcpp_local/trading_assistant/]
---

# 自動化交易輔助系統

> 一個基於 Python 的自動化交易輔助系統，提供市場資料蒐集、技術指標計算、策略回測與績效評估功能。
> ⚠️ **本系統僅供學習與研究用途，不構成任何投資建議。**

## 📋 概述

此系統是一個模組化的量化交易研究框架，旨在幫助使用者學習技術分析、理解交易策略邏輯，並練習程式設計。系統包含四大核心模組：

1. **市場資料蒐集** - 即時獲取股價數據
2. **技術指標計算** - RSI、MACD、布林通道等
3. **交易策略** - 移動平均線交叉策略、RSI 策略
4. **回測框架** - 歷史績效評估與視覺化

## 🏗️ 系統架構

```
trading_assistant/
├── __init__.py           # 套件初始化
├── main.py               # 主程式入口
├── data_collector.py     # 市場資料蒐集模組
├── indicators.py         # 技術指標計算模組
├── strategies.py         # 交易策略模組
└── README.md             # 本檔案
```

## 🔧 依賴套件

| 套件 | 用途 |
|------|------|
| `yfinance` | 獲取股票市場數據 |
| `pandas` | 數據處理與分析 |
| `ta` | 技術指標計算 |
| `matplotlib` | 圖表視覺化 |
| `mplfinance` | 金融圖表繪製 |
| `backtrader` | 回測框架 |

### 安裝指令

```bash
pip3 install --break-system-packages yfinance pandas ta matplotlib mplfinance backtrader
```

## 📊 核心功能

### 1. 市場資料蒐集 (`data_collector.py`)

```python
from data_collector import MarketDataCollector

collector = MarketDataCollector(['AAPL', 'GOOGL', 'MSFT'])
data = collector.fetch_all_tickers(period="1y")
```

**功能：**
- 獲取歷史股價數據（支援多種時間週期）
- 獲取當前價格
- 市場摘要生成

### 2. 技術指標計算 (`indicators.py`)

```python
from indicators import TechnicalIndicators

indicators = TechnicalIndicators(df)
df_with_indicators = indicators.calculate_all_indicators()
```

**計算指標：**
| 指標類型 | 具體指標 |
|----------|----------|
| 移動平均線 | SMA(20), SMA(50), EMA(12), EMA(26) |
| 動量指標 | RSI(14) |
| 趨勢指標 | MACD, Signal, Histogram |
| 波動率指標 | 布林通道 (上軌、中軌、下軌) |
| 成交量指標 | 成交量加權平均價格 |

### 3. 交易策略 (`strategies.py`)

#### 移動平均線交叉策略

```python
from strategies import MovingAverageCrossoverStrategy

strategy = MovingAverageCrossoverStrategy(fast_period=20, slow_period=50)
results = strategy.backtest(df)
```

**邏輯：**
- 當快速均線 > 慢速均線 → 做多
- 當快速均線 < 慢速均線 → 做空

#### RSI 策略

```python
from strategies import RSIBasedStrategy

strategy = RSIBasedStrategy(rsi_period=14, oversold=30, overbought=70)
results = strategy.backtest(df)
```

**邏輯：**
- RSI < 30（超賣）→ 買入
- RSI > 70（超買）→ 賣出

### 4. 主程式 (`main.py`)

```bash
python3.12 main.py
```

**功能：**
- 自動蒐集多標的數據
- 執行完整策略回測
- 生成績效報告
- 產出視覺化圖表

## 📈 回測結果範例

| 標的 | 當前價格 | MA 策略報酬 | RSI 策略報酬 |
|------|----------|-------------|--------------|
| AAPL | $270.23 | +33.05% | +1.86% |
| GOOGL | $341.68 | +86.07% | -10.09% |
| MSFT | $422.79 | +7.02% | -8.70% |

> ⚠️ 以上為過去一年的歷史回測結果，不代表未來表現。

## ⚠️ 重要限制與警告

### 不適用於實際交易的原因

1. **過度擬合 (Overfitting)**
   - 策略是針對過去數據最佳化的
   - 類似考試前背答案，下次考試可能失效

2. **忽略交易成本**
   - 未包含手續費、滑價、稅金
   - 頻繁交易會大幅降低實際報酬

3. **未考慮風險管理**
   - 未設定停損停利機制
   - 最大回撤可能非常顯著

4. **市場非靜態**
   - 過去表現不代表未來
   - 黑天鵝事件無法預測

### 正確的使用方式

✅ **適合用途：**
- 學習技術分析概念
- 理解策略邏輯與限制
- 練習程式設計能力
- 建立交易紀律意識

❌ **不適合用途：**
- 直接用於實際交易
- 作為投資決策依據
- 保證獲利預測工具

## 🚀 未來擴展方向

1. **風險管理模組** - 加入停損停利、資金管理
2. **更多策略** - MACD、布林通道、海龜交易法
3. **即時監控** - 價格警報、自動通知
4. **圖表儀表板** - 整合視覺化報告
5. **多資產支援** - 加密貨幣、外匯、期貨
6. **機器學習** - 使用 ML 優化策略參數

## 📁 專案位置

```
/root/.hermes/profiles/koboldcpp_local/trading_assistant/
```

## 🔗 相關概念

- [[concepts/safe-execution-workflow]] — 安全執行工作流
- [[concepts/agent-skills-index]] — Agent Skills 用途一覽

## 📝 開發日誌

| 日期 | 版本 | 變更內容 |
|------|------|----------|
| 2026-04-20 | 1.0.0 | 初始版本：基本架構與兩大策略 |
| 2026-04-26 | 1.1.0 | 新增 Chrome Extension 截圖分析方向：Vision + Extension 協作架構 |

---

## 🧩 新方向：Chrome Extension + Vision 截圖分析 (2026-04-26)

> 基於 Hermes Agent 的 Vision 能力，開發 Chrome Extension 在 TradingView 上截圖並傳送分析，繞過 WSL 無法操控 Chrome + 不暴露 Cookie 的雙重限制。

### 📌 問題背景

- WSL 無法透過 CDP 操控 Windows Chrome
- TradingView 有反爬機制，用自動化工具可能封鎖付費帳號（內含即時數據費用）
- 先前租用 Vast.ai 4080S 跑 Qwen 看圖，已停租

### 💡 方案核心設計

**反過來 — 不是 Agent 去操控 Chrome，而是 Chrome Extension 主動把數據丟過來。**

### 🔄 完整 Workflow

1. 用戶在 TradingView 看到 setup，按下 Extension 按鈕/快捷鍵
2. Extension 同時做三件事：
   - `chrome.tabs.captureVisibleTab()` 截圖
   - 從 DOM 抓取當前價格 + 3-5 個常用指標數值
   - Popup 輸入框：方向（做多/做空）、進場價位（自動帶入）、停損、目標、備註
3. 數據存到本地路徑 `C:\Users\{user}\TradingScreenshots\`
4. Hermes Agent 經 `/mnt/c/` 讀取圖片 + JSON
5. Vision 分析型態、趨勢線、K 棒排列
6. 同步掃 finviz 行事曆 + 最新新聞
7. 回覆完整分析 + 風險提醒（含今日事件提醒）

### 🏗️ 技術架構

```
┌─────────────────────┐     截圖 + DOM 數據
│  Chrome Extension   │ ──────────────────→ 本地檔案系統
│  (TradingView 上)   │                    (C:\Users\...\TradingScreenshots\)
└─────────────────────┘
                                              │
                                              ▼
                                      ┌─────────────────┐
                                      │  Hermes Agent   │
                                      │  (WSL)          │
                                      │  ┌───────────┐  │
                                      │  │ Vision     │  │ ← 分析截圖
                                      │  │ Web Search │  │ ← 掃新聞/事件
                                      │  │ Knowledge  │  │ ← 交易日記
                                      │  └───────────┘  │
                                      └─────────────────┘
                                              │
                                              ▼
                                      Discord 推送分析結果
```

### 📦 Extension 功能細節

| 功能 | 實作方式 | 備註 |
|------|----------|------|
| 截圖 | `chrome.tabs.captureVisibleTab()` | 最簡單，vision 可讀型態/趨勢線 |
| DOM 抓價 | `document.querySelector()` | 當前價格 + MA/RSI 等 3-5 個數值 |
| Popup 輸入 | Extension Action Popup | 方向、進場價、停損、目標、備註 |
| 存檔 | 存 PNG + JSON 到本地 | 用 `chrome.downloads` 或 File API |

### ❗ 風險考量

- ✅ **不暴露 TradingView Cookie**，無封號風險
- ✅ **不需租用 GPU**，Hermes Agent Vision 即可
- ⚠️ Vision 分析約 15-30 秒，價格數字偶有誤差
- ⚠️ 開發需 Chrome Extension 技能（用戶有舊經驗但需重新學習）

### 🔗 相關概念

- [[concepts/hermes-agent-soul-craft]] — Hermes Agent 人格設計
- [[lists/hermes-agent-ecosystem]] — Hermes Agent 生態系
- [[docs/plans/2026-04-27-tradingview-chrome-extension]] — 實作計畫
