---
title: KDJ 指標實戰筆記（MNQ 適用）
created: 2026-04-27
updated: 2026-04-27
type: indicator
tags: [trading, mnq, kdj, technical-analysis]
related-sessions: [trading/sessions/2026-04-27-mnq-morning]
sources: [trading/journal/kdj-mnq-threshold-calibration]
---

# KDJ 指標實戰筆記（MNQ 適用）

## 基本設定

- 預設參數：K=9, D=3, J=3（TradingView 預設）
- 時間框架：5 分 K（日內）/ 3 分 K（短線）
- 與其他指標搭配：PPO（趨勢確認）+ StochRSI（極端確認）

## MNQ 專用閾值（校正後）

| 訊號 | 條件 | 行動 |
|------|------|------|
| 極度超賣 | J < **0** (非傳統 20) | 考慮做多 |
| 深度超賣 | J < 5 | 注意反彈 |
| 超買警戒 | J > **105** (非傳統 80) | 考慮減倉 |
| 健康區 | J 80-105 + K/D 多頭 | 可順勢做多 |
| K/D 金叉 | K 上穿 D | 確認反轉 |
| K/D 死叉 | K 下穿 D | 確認反轉 |

## 優先級

1. **K/D 多空排列 > J 值** — 排列方向決定趨勢立場
2. **J 值加速度 > J 值絕對值** — 快速變動比靜態值更有意義
3. **第 X 次超買/超賣 > 第 1 次** — 首次有效，後續衰減

## 搭配用法

- **PPO > 0 + K/D 多頭** → 只做多，不做空
- **PPO < 0 + K/D 空頭** → 只做空，不做多
- **StochRSI 極端 + J 回檔** → 趨勢健康，不是反轉
