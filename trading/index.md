---
title: Trading 交易知識庫
created: 2026-04-27
updated: 2026-04-29
sources:
  - trading/trade-log.yaml
type: index
tags: [trading, index]
---

# Trading 交易知識庫

> MNQ 交易日記、練習筆記與市場觀察。
> 最後更新：2026-04-30

## 📋 Sessions（交易日記）

> ⚠️ 此目錄包含個人交易盈虧紀錄，由 `.gitignore` 排除版本控制。

- [[trading/trade-log]] — 結構化交易紀錄（機器可解析，用於自動統計）

> ⚠️ 以下為人類可讀版交易日記：

- [[trading/sessions/2026-04-29-mnq-morning]] — 2026-04-29 早盤：+8pt 🟢
- [[trading/sessions/2026-04-29-mnq-night]] — 2026-04-29 夜盤：-39.25→+77.5 = **+38.25pt** 🚀（驗證 ADX DI>20 + KDJ 模式）
- [[trading/sessions/2026-04-30-mnq-morning]] — 2026-04-30 早盤：27,299.5→27,325.5/27,383.75 = **+110.25pt** 🚀（兩口拆分教科書 +110.25pt）
- [[trading/sessions/2026-04-30-mnq-night]] — 2026-04-30 夜盤：27,461.25→27,505.5 +44.25pt / 27,511.25 進行中 = 本日已實現 **+173.25pt** 🚀🔥
- [[trading/sessions/2026-04-28-mnq-morning]] — 2026-04-28 早盤：兩口多單(+14.5點) = **+14.5點** 🚀
- [[trading/sessions/2026-04-27-mnq-night]] — 2026-04-27 夜盤：交易一(-56.5) + 交易二(+72.75) + 交易三(+11.5) = **+27.75點** 🎯

## 📝 Journal（練習筆記／覆盤心得）

- [[trading/journal/kdj-mnq-threshold-calibration]] — KDJ 在 MNQ 的閾值校正：極端 J 值需到 0~-5 / 105+
- [[trading/journal/second-oversold-trap]] — 第二次超賣陷阱：首次有效，後續衰減
- [[trading/journal/ema-collapse-warning]] — EMA 三線坍縮 = 無效壓力牆，差距 <5 點時不可靠
- [[trading/journal/entry-hesitation-signal]] — 入場猶豫本身就是信號：當你在問「要不要等」，答案永遠是「等」

## 📊 Indicators（指標學習筆記）

- [[trading/indicators/kdj-for-mnq]] — KDJ 指標 MNQ 實戰用法與校正後閾值
- [[trading/indicators/di-indicator]] — DI 方向指標（原名客製ADX）：DI 交叉 + 門檻值 Alert，不含 ADX 混淆
- [[trading/indicators/stochrsi-extreme-behavior]] — StochRSI 極端值(100/100)在強趨勢下可長時間持續
- [[trading/indicators/adx-for-mnq]] — ADX 盤整過濾 + 多時間框架（避免盤整日雙巴）
- [[trading/indicators/ema-kdj-ppo-adx-correlation]] — 四指標趨勢 vs 盤整行為對照表（實證分析）

## 🌏 Market Notes（市場觀察）

- [[trading/market-notes/asian-session-liquidity]] — 亞洲盤流動性模式：06:00/08:00/09:00 時間節點
- [[trading/market-notes/cme-data-pricing]] — CME 即時數據訂閱方案與費用比較（IBKR/Binance/Databento 等）

## 📋 Strategy（策略文件）

- [[trading/strategy/mnq-scalping-system]] — MNQ Scalping 系統策略參考：完整進出場規則、Train Mode 🚃、手機速查表

## 📐 Templates（交易日記模板）

- [[trading/templates/session-journal]] — 交易日記 Template：統一格式，供 Agent 自動生成 session 紀錄
