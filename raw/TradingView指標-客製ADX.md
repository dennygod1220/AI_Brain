---
source_url: ""
ingested: 2026-04-30
---

```
//@version=6

indicator(title="客製ADX", shorttitle="客製ADX", format=format.price, precision=4, timeframe="", timeframe_gaps=true)

lensig = input.int(14, title="ADX Smoothing", minval=1)

len = input.int(14, minval=1, title="DI Length")

adxOver = input.int(25 , 'ADX有效值')

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

plot(math.round(plus,2), color=#3bff29, title="+DI")

plot(math.round(minus,2), color=color.rgb(255, 3, 3), title="-DI")

  

DIBuy = plus > minus ? true : false

DISell = minus > plus ? true : false

  

hline(adxOver, color=color.white, linewidth=1, linestyle=hline.style_dashed)

bgcolor(DIBuy and adx > adxOver ? color.rgb(192, 245, 194, 81) : na)

bgcolor(DISell and adx > adxOver ? color.rgb(253, 191, 191, 86) : na)
```
