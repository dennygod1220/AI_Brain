---
title: KDJ + DI 聯動腳本（含 Alert 條件）
created: 2026-04-30
updated: 2026-04-30
type: entity
tags: [trading, indicator, mnq, technical-analysis]
sources:
  - raw/TradingView指標-KDJ.md
  - trading/indicators/di-indicator.md
---

# KDJ + DI 聯動腳本

合併 KDJ 與 DI 兩個獨立 Pine Script 為單一腳本，**減少假 Alert**。
由 KDJ 金叉/死叉觸發 Alert，DI 方向 + 門檻值作為趨勢過濾器。

## 原始碼

```pine
//@version=6
indicator(title="KDJ + DI 聯動", shorttitle="KDJ+DI", format=format.price, precision=2, timeframe="", timeframe_gaps=true)

// ═══ 參數 ═══
kdjPeriod = input.int(9, "KDJ 週期")
kdjSignal = input.int(3, "KDJ 平滑")
diLen     = input.int(14, "DI Length")
diThresh  = input.int(25, "DI 有效門檻")

// ═══ KDJ ═══
bcwsma(s, l, m) =>
    var float _bcwsma = na
    _bcwsma := (m * s + (l - m) * nz(_bcwsma[1])) / l
    _bcwsma

RSV = 100 * ((close - ta.lowest(low, kdjPeriod)) / (ta.highest(high, kdjPeriod) - ta.lowest(low, kdjPeriod)))
pK = bcwsma(RSV, kdjSignal, 1)
pD = bcwsma(pK, kdjSignal, 1)
pJ = 3 * pK - 2 * pD

kGolden = ta.crossover(pK, pD)
kDeath  = ta.crossunder(pK, pD)

// ═══ DI ═══
up = ta.change(high)
down = -ta.change(low)
plusDM  = na(up) ? na : (up > down and up > 0 ? up : 0)
minusDM = na(down) ? na : (down > up and down > 0 ? down : 0)
trur = ta.rma(ta.tr, diLen)
plus  = fixnan(100 * ta.rma(plusDM, diLen) / trur)
minus = fixnan(100 * ta.rma(minusDM, diLen) / trur)

// ═══ 聯動 Alert ═══
// 做多：KDJ金叉 + +DI > -DI 且 +DI 在門檻之上
longAlert  = kGolden and (plus > minus) and (plus > diThresh)
// 做空：KDJ死叉 + -DI > +DI 且 -DI 在門檻之上
shortAlert = kDeath  and (minus > plus) and (minus > diThresh)

// 進階：加上 J 值超買/超賣過濾
longEntry  = longAlert  and pJ < 20
shortEntry = shortAlert and pJ > 80

alertcondition(longAlert,  title="🟢 金叉 + DI順勢(門檻上)",
    message="KDJ 金叉，+DI > -DI 且 +DI > 門檻")
alertcondition(shortAlert, title="🔴 死叉 + DI順勢(門檻上)",
    message="KDJ 死叉，-DI > +DI 且 -DI > 門檻")

alertcondition(longEntry,  title="🎯 超賣金叉 + DI順勢(門檻上)",
    message="KDJ 超賣區金叉，+DI > -DI 且 +DI > 門檻")
alertcondition(shortEntry, title="🎯 超買死叉 + DI順勢(門檻上)",
    message="KDJ 超買區死叉，-DI > +DI 且 -DI > 門檻")

// ═══ 圖表繪製 ═══
plot(pK, color=#1E88E5, title="K")
plot(pD, color=#FF6F00, title="D")
plot(pJ, color=color.rgb(180, 140, 255), title="J")
hline(80, color=color.gray, linestyle=hline.style_dashed)
hline(20, color=color.gray, linestyle=hline.style_dashed)

plot(math.round(plus, 2),  color=#3bff29, title="+DI")
plot(math.round(minus, 2), color=color.rgb(255, 3, 3), title="-DI")
hline(diThresh, color=color.white, linestyle=hline.style_dashed)

plotshape(longEntry,  style=shape.triangleup,   location=location.bottom, color=color.new(#00ff00, 20), size=size.tiny, offset=-1)
plotshape(shortEntry, style=shape.triangledown, location=location.top,    color=color.new(#ff0303, 20), size=size.tiny, offset=-1)
```

## 設計邏輯

### 角色分工

| 指標 | 角色 | 說明 |
|------|------|------|
| **KDJ 交叉** | 🕐 觸發時機 | KDJ 快、先出訊號，決定 Alert 何時叫 |
| **DI 方向** | 🚦 趨勢過濾 | +DI > -DI 做多、-DI > +DI 做空 |
| **DI 門檻 (>25)** | 🛡️ 能量過濾 | 優勢方 DI 必須在白虛線之上，排除低能量狀態 |

### 為何不是 DI 交叉？

KDJ 比 DI 敏感（KDJ 週期 9 vs DI 週期 14），KDJ 金叉/死叉通常比 DI 交叉早好幾根 K 棒。
所以做法是：**KDJ 交叉那刻檢查當下 DI 方向是否正確 + 優勢方是否在門檻之上**，而非要求兩者同時交叉。

### Alert 層級

| Alert 名稱 | 觸發條件 | 強度 |
|-----------|---------|------|
| 🟢 金叉 + DI順勢 | KDJ金叉 + +DI > -DI > 門檻 | 一般做多 |
| 🔴 死叉 + DI順勢 | KDJ死叉 + -DI > +DI > 門檻 | 一般做空 |
| 🎯 超賣金叉 + DI順勢 | 同上 + J < 20（超賣區反轉） | 🔥 最強做多 |
| 🎯 超買死叉 + DI順勢 | 同上 + J > 80（超買區反轉） | 🔥 最強做空 |

## 參數

| 參數 | 預設值 | 說明 |
|------|--------|------|
| KDJ 週期 | 9 | KDJ RSV 取樣長度 |
| KDJ 平滑 | 3 | K/D 線平滑參數 |
| DI Length | 14 | DI 計算週期 |
| DI 有效門檻 | 25 | 白色虛線，DI 須高於此值才視為有效方向 |

## 使用方式

1. 複製上方程式碼貼入 TradingView Pine Editor
2. 加到圖表後，右鍵指標 → **Add Alert**
3. 選擇 Condition 為 `"🟢 金叉 + DI順勢(門檻上)"` 或自選需要的 Alert
4. 可同時開啟多個 Alert，分別設定 Webhook URL / Discord / Email

## 來源

- KDJ 原始腳本：[[raw/TradingView指標-KDJ.md]]
- DI 原始腳本（原名客製ADX）：[[_archive/raw/TradingView指標-客製ADX.md]] → [[trading/indicators/di-indicator]]
