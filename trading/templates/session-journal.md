---
title: 交易日記 Template
created: 2026-04-30
updated: 2026-05-03
type: template
tags: [trading, template, meta]
sources: []
---

# 交易日記 Template

> 使用方式：複製此 template 到 `trading/sessions/YYYY-MM-DD-mnq-{morning|night}.md`，填入實際數據。
> 每個交易日的早盤和夜盤各一篇，方便日後回測與模式歸納。
>
> 區段順序遵循 [[SCHEMA]] 的交易日記格式規範。

```yaml
---
title: MNQ {早盤|夜盤}交易記錄 — 一句話總結
date: YYYY-MM-DD
product: MNQ1!
timeframe: 3分K
pnl: "+Xpt (+$X)"
session: {morning|night}
tags: [trading, mnq, session]
sources:
  - trading/screenshots/tv_YYYY-MM-DD_HH-MM-SS.png
  - trading/screenshots/...
---
```

---

## 交易一（{方向}×{口數}）：{一句結果}

### 進場

| 項目 | 數值 |
|------|------|
| 方向 | 多 Long / 空 Short |
| 口數 | {1口 / 2口} |
| 進場 | XX,XXX.XX @ ~HH:MM |
| 出場 | XX,XXX.XX @ ~HH:MM（或：進行中） |
| **損益** | **+/-X.XXpt (+/-$X.XX)** |
| 持倉時間 | ~X 分鐘 |

### 進場邏輯

- **KDJ** — K/D 交叉狀態，J 值位置
- **ADX DI** — DI+ / DI- 數值，DI gap
- **EMA 結構** — 價格 vs EMA10/30/60
- **背景** — 市場情境補充

### 📸 進場截圖

![[trading/screenshots/tv_YYYY-MM-DD_HH-MM-SS.png]]
> 進場時的圖表狀況

### 持倉過程截圖（如有）

![[trading/screenshots/tv_YYYY-MM-DD_HH-MM-SS.png]]
> 持倉中追蹤截圖，按時間順序排列

### 出場分析

出場原因說明。

**對照 Train Mode 出場條件：**
| 條件 | 實際 | 結果 |
|:----|:----|:----:|
| 🅰️ 跌破 EMA10 | — | ✅/❌ 未觸發/觸發 |
| 🅱️ KDJ 死叉 + DI gap 腰斬 | — | ✅/❌ |
| 🅲 DI gap < 5 | — | ✅/❌ |
| 🅳 EMA30 被測試 | — | ✅/❌ |

→ 出場合理性判斷

### 📸 出場截圖

![[trading/screenshots/tv_YYYY-MM-DD_HH-MM-SS.png]]
> 出場時的圖表狀況

### 覆盤

#### 做對的 ✅
1. ...

#### 可以改進的 ⚠️
1. ...

#### 💡 教訓
- ...

---

## 交易二（{方向}×{口數}）：{一句結果}

（同上結構：進場明細 → 進場邏輯 → 📸 進場截圖 → 📸 持倉截圖 → 出場分析 → 📸 出場截圖 → 覆盤）

---

## 本日總計

| 交易 | 方向 | 進場 | 出場 | 損益 |
|:----|:---:|:----:|:----:|:----:|
| ☀️ 早盤/🌙 夜盤一（X口） | 多/空 | XX,XXX | XX,XXX | +/-Xpt |
| ☀️ 早盤/🌙 夜盤二（X口） | 多/空 | XX,XXX | XX,XXX | +/-Xpt |
| **已實現** | | | | **+/-Xpt ($X)** 🚀 |

---

## 模式驗證

### Jason's Pattern 驗證 {✅/❌}

> **KDJ 先行 + ADX DI+ > 20 確認 + DI gap > 10 + EMA30 上方**

| 交易 | KDJ金叉 | DI+>20 | DI gap>10 | EMA30上方 | 結果 |
|:----:|:-------:|:------:|:---------:|:---------:|:----:|
| 交易一 | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | +Xpt |
| 交易二 | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | +Xpt |

### 策略偏離記錄（如有）

哪些交易偏離了 [[trading/strategy/mnq-scalping-system]]，原因是什麼，下次如何避免。

---

## 累計績效

| 日期 | 損益 |
|:----|:----:|
| 2026-04-27 | +27.75pt |
| 2026-04-28 | -16pt |
| 2026-04-29 | +46.25pt |
| 2026-04-30 | **+178.5pt 🏆** |
| **總計** | **~+236.5pt** |
