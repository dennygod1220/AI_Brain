---
title: DI 方向指標（含 Alert 條件）
created: 2026-04-30
updated: 2026-04-30
type: entity
tags: [trading, indicator, mnq, technical-analysis]
sources:
  - _archive/raw/TradingView指標-客製ADX.md
---

# DI 方向指標

> 原名「客製ADX」，2026-04-30 更名。此指標實際上只使用 DI+/DI- 兩條線，ADX 主線僅供參考，核心邏輯是 **DI 交叉 + DI 門檻過濾**。

TradingView Pine Script — 基於 ADX 原始碼提取 DI 線，增加 DI 交叉 Alert + 門檻值過濾。

```pine
//@version=6

indicator(title="DI方向指標", shorttitle="DI", format=format.price, precision=4, timeframe="", timeframe_gaps=true)

lensig = input.int(14, title="ADX Smoothing", minval=1)

len = input.int(14, minval=1, title="DI Length")

diThresh = input.int(25, 'DI有效門檻')

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

// --- 交叉訊號 (僅DI線高於有效門檻時觸發) ---
bullCross = ta.crossover(plus, minus) and plus > diThresh
bearCross = ta.crossunder(plus, minus) and minus > diThresh

plotshape(bullCross, style=shape.triangleup, location=location.bottom, color=color.new(#3bff29, 30), size=size.tiny, offset=-1)
plotshape(bearCross, style=shape.triangledown, location=location.top, color=color.new(#ff0303, 30), size=size.tiny, offset=-1)

// --- Alert條件 ---
alertcondition(bullCross, title="DI 多頭交叉", message="+DI 向上穿越 -DI，DI 高於有效門檻")
alertcondition(bearCross, title="DI 空頭交叉", message="-DI 向上穿越 +DI，DI 高於有效門檻")

hline(diThresh, color=color.white, linewidth=1, linestyle=hline.style_dashed)

bgcolor(DIBuy and plus > diThresh ? color.rgb(192, 245, 194, 81) : na)
bgcolor(DISell and minus > diThresh ? color.rgb(253, 191, 191, 86) : na)
```

## 修改說明

- **原始來源**: `_archive/raw/TradingView指標-客製ADX.md`
- **2026-04-30 更名**：原名「客製ADX」，因指標實際核心為 DI 方向訊號而非 ADX，故更名為「DI方向指標」
- **參數更名**：`adxOver` → `diThresh`，避免與 ADX 混淆
- **Alert 更名**：`"ADX 多頭交叉"` → `"DI 多頭交叉"` / `"DI 空頭交叉"`
- **背景邏輯修正**：`bgcolor` 條件從 `adx > adxOver` 改為 `plus > diThresh` / `minus > diThresh`，與 Alert 邏輯一致
- **使用方式**: 直接複製上方程式碼貼入 TradingView Pine Editor 即可

## 參數

| 參數 | 預設值 | 說明 |
|------|--------|------|
| ADX Smoothing | 14 | ADX 平滑週期（僅供圖面參考） |
| DI Length | 14 | DI 計算週期 |
| DI有效門檻 | 25 | 白色虛線，DI 須高於此值才觸發 Alert |

> ⚠️ **更名後需手動操作**：到 TradingView Pine Editor 取代舊腳本，並重建 Alert（Alert 名稱已變）。
