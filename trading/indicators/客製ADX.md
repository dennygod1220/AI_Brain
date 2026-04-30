---
title: 客製ADX（含 Alert 條件）
created: 2026-04-30
updated: 2026-04-30
type: entity
tags: [trading, indicator, mnq, technical-analysis]
sources: [raw/TradingView指標-客製ADX.md]
---

# 客製ADX

TradingView Pine Script 自訂 ADX 指標，基於原始版擴充 DI 交叉 Alert 條件。

```
//@version=6

indicator(title="客製ADX", shorttitle="客製ADX", format=format.price, precision=4, timeframe="", timeframe_gaps=true)

lensig = input.int(14, title="ADX Smoothing", minval=1)

len = input.int(14, minval=1, title="DI Length")

adxOver = input.int(25, 'ADX有效值')

up = ta.change(high)

down = -ta.change(low)

plusDM = na(up) ? na : (up > down and up > 0 ? up : 0)

minusDM = na(down) ? na : (down > up and down > 0 ? down : 0)

trur = ta.rma(ta.tr, len)

plus = fixnan(100 * ta.rma(plusDM, len) / trur)

minus = fixnan(100 * ta.rma(minusDM, len) / trur)

sum = plus + minus

adx = 100 * ta.rma(math.abs(plus - minus) / (sum == 0 ? 1 : sum), lensig)

plot(adx, color=color.rgb(255, 248, 40), title="ADX")

plot(math.round(plus, 2), color=#3bff29, title="+DI")

plot(math.round(minus, 2), color=color.rgb(255, 3, 3), title="-DI")

DIBuy = plus > minus
DISell = minus > plus

// --- 交叉訊號 (僅DI線高於有效值時觸發) ---
bullCross = ta.crossover(plus, minus) and plus > adxOver
bearCross = ta.crossunder(plus, minus) and minus > adxOver

plotshape(bullCross, style=shape.triangleup, location=location.bottom, color=color.new(#3bff29, 30), size=size.tiny, offset=-1)
plotshape(bearCross, style=shape.triangledown, location=location.top, color=color.new(#ff0303, 30), size=size.tiny, offset=-1)

// --- Alert條件 ---
alertcondition(bullCross, title="ADX 多頭交叉", message="+DI 向上穿越 -DI，DI 高於有效值")
alertcondition(bearCross, title="ADX 空頭交叉", message="-DI 向上穿越 +DI，DI 高於有效值")

hline(adxOver, color=color.white, linewidth=1, linestyle=hline.style_dashed)

bgcolor(DIBuy and adx > adxOver ? color.rgb(192, 245, 194, 81) : na)
bgcolor(DISell and adx > adxOver ? color.rgb(253, 191, 191, 86) : na)
```

## 修改說明

- **原始來源**: `raw/TradingView指標-客製ADX.md`
- **新增 alertcondition**: `"ADX 多頭交叉"`（+DI 上穿 -DI **且 DI > 水平線**）、`"ADX 空頭交叉"`（-DI 上穿 +DI **且 DI > 水平線**）
- **圖表視覺**: 交叉發生時顯示綠色 ▲ / 紅色 ▼ 標記
- **使用方式**: 直接複製上方程式碼貼入 TradingView Pine Editor 即可

## 參數

| 參數 | 預設值 | 說明 |
|------|--------|------|
| ADX Smoothing | 14 | ADX 平滑週期 |
| DI Length | 14 | DI 計算週期 |
| ADX有效值 | 25 | ADX 有效門檻（白色虛線） |
