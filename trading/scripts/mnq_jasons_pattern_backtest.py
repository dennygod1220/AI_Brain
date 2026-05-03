#!/usr/bin/env python3
"""
MNQ Jason's Pattern 自動回測引擎 (Phase 1)
============================================
使用 yfinance + pandas 對 Jason's Pattern 進行 2 分 K 歷史回測。

Long Entry:
  1. KDJ 黃金交叉 (J 上穿 K/D)
  2. DI+ > DI- 且 DI+ > 20
  3. DI gap > 10
  4. 15分K J 值上升中
  5. 價格在 EMA30 上方

Short Entry:
  1. KDJ 死亡交叉 (J 下穿 K/D)
  2. DI- > DI+ 且 DI- > 20
  3. DI gap > 10
  4. 15分K J 值下降中
  5. 價格在 EMA30 下方

Output: 回測報告 (console) + 圖表 (trading/screenshots/)
"""

import os
import sys
import json
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.rcParams.update({
    "figure.facecolor": "#1a1a2e",
    "axes.facecolor": "#16213e",
    "axes.edgecolor": "#4a4a6a",
    "axes.labelcolor": "#e0e0e0",
    "text.color": "#e0e0e0",
    "legend.facecolor": "#16213e",
    "legend.edgecolor": "#4a4a6a",
    "xtick.color": "#a0a0b0",
    "ytick.color": "#a0a0b0",
    "grid.color": "#2a2a4a",
    "grid.alpha": 0.5,
})

# 設定中文字型 (Noto Sans CJK TTC 集合字型)
import os
font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
if os.path.exists(font_path):
    from matplotlib import font_manager
    font_manager.fontManager.addfont(font_path)
    plt.rcParams["font.sans-serif"] = ["Noto Sans CJK JP"]
    plt.rcParams["font.family"] = "sans-serif"
else:
    pass

# ── 設定 ──────────────────────────────────────────

TICKER = "NQ=F"
LOOKBACK_DAYS = 55          # yfinance 5min 最大 ~60 天，取 55 安全值
MINOR_TF = "2m"
MAJOR_TF = "15m"
OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "screenshots"
)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Jason's Pattern 參數
KDJ_PERIOD = 9
DMI_PERIOD = 14
EMA_FAST = 10
EMA_MID = 30
EMA_SLOW = 60
DI_THRESHOLD = 20
DI_GAP_MIN = 10

# 交易參數 (點數, MNQ 1點 = $2)
SL_PTS = 18
TP1_PTS = 12
MIN_RR = 1.0

# 時間段 (UTC, 從 yfinance 拿到的 timestamp 是 UTC)
SESSIONS = {
    "亞洲盤": (22, 5),      # 06:00-13:00 UTC+8 → 22:00-05:00 UTC (跨午夜)
    "歐洲盤": (8, 12),      # 16:00-19:59 UTC+8 → 08:00-11:59 UTC
    "美盤": (12, 17),       # 20:00-01:00 UTC+8 → 12:00-17:00 UTC
}

# ── 指標計算 ──────────────────────────────────────


def calc_ema(df, period):
    return df["Close"].ewm(span=period, adjust=False).mean()


def calc_kdj(df, period=KDJ_PERIOD):
    """回傳 K, D, J 三條線 (pandas vectorized)"""
    low_min = df["Low"].rolling(window=period).min()
    high_max = df["High"].rolling(window=period).max()
    rsv = ((df["Close"] - low_min) / (high_max - low_min)) * 100
    # 用 SMA 模擬 KDJ 的平滑
    k = rsv.ewm(span=3, adjust=False).mean()
    d = k.ewm(span=3, adjust=False).mean()
    j = 3 * k - 2 * d
    return k, d, j


def calc_dmi(df, period=DMI_PERIOD):
    """回傳 DI+, DI-, ADX (pandas vectorized)"""
    high, low, close = df["High"], df["Low"], df["Close"]

    # True Range
    prev_close = close.shift(1)
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    # Directional Movement
    up_move = high - high.shift(1)
    down_move = low.shift(1) - low
    dm_plus = pd.Series(np.where(
        (up_move > 0) & (up_move > down_move), up_move, 0
    ), index=df.index)
    dm_minus = pd.Series(np.where(
        (down_move > 0) & (down_move > up_move), down_move, 0
    ), index=df.index)

    # Smooth
    tr_s = tr.ewm(span=period, adjust=False).mean()
    dm_plus_s = dm_plus.ewm(span=period, adjust=False).mean()
    dm_minus_s = dm_minus.ewm(span=period, adjust=False).mean()

    di_plus = (dm_plus_s / tr_s) * 100
    di_minus = (dm_minus_s / tr_s) * 100

    # ADX
    dx = (abs(di_plus - di_minus) / (di_plus + di_minus)) * 100
    adx = dx.ewm(span=period, adjust=False).mean()

    return di_plus, di_minus, adx


# ── 數據擷取 ──────────────────────────────────────


def fetch_data():
    """下載 2分K 和 15分K 數據"""
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=LOOKBACK_DAYS)

    print(f"⏬ 下載 {TICKER} {MINOR_TF} ({LOOKBACK_DAYS}天)...")
    df_minor = yf.download(TICKER, interval=MINOR_TF, start=start, end=end,
                           progress=False, multi_level_index=False)
    if df_minor.empty:
        print("❌ 無法取得 2分K 數據")
        sys.exit(1)

    print(f"⏬ 下載 {TICKER} {MAJOR_TF}...")
    df_major = yf.download(TICKER, interval=MAJOR_TF, start=start, end=end,
                           progress=False, multi_level_index=False)
    if df_major.empty:
        print("❌ 無法取得 15分K 數據")
        sys.exit(1)

    print(f"   → {MINOR_TF}: {len(df_minor)} 根 K 線")
    print(f"   → {MAJOR_TF}: {len(df_major)} 根 K 線")
    return df_minor, df_major


def prepare_data(df_minor, df_major):
    """計算所有指標並合併 15分K 方向的資訊"""
    df = df_minor.copy()
    df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]

    # ── 2分K 指標 ──
    df["EMA10"] = calc_ema(df, EMA_FAST)
    df["EMA30"] = calc_ema(df, EMA_MID)
    df["EMA60"] = calc_ema(df, EMA_SLOW)
    k, d, j = calc_kdj(df, KDJ_PERIOD)
    df["K"] = k
    df["D"] = d
    df["J"] = j
    di_plus, di_minus, adx = calc_dmi(df, DMI_PERIOD)
    df["DI+"] = di_plus
    df["DI-"] = di_minus
    df["ADX"] = adx
    df["DI_Gap"] = (df["DI+"] - df["DI-"]).abs()

    # 前一根 J (用於交叉檢測)
    df["J_prev"] = df["J"].shift(1)
    df["K_prev"] = df["K"].shift(1)
    df["D_prev"] = df["D"].shift(1)

    # ── 15分K 方向資訊 ──
    df_major.columns = [c[0] if isinstance(c, tuple) else c for c in df_major.columns]
    k_m, d_m, j_m = calc_kdj(df_major, KDJ_PERIOD)
    df_major["J_15m"] = j_m

    # 將 15分K 的 J 值對齊到 2分K (forward fill)
    j_15m_aligned = df_major["J_15m"].reindex(df.index, method="ffill")
    j_15m_prev = df_major["J_15m"].shift(1).reindex(df.index, method="ffill")
    df["J_15m"] = j_15m_aligned
    df["J_15m_prev"] = j_15m_prev
    df["J_15m_rising"] = df["J_15m"] > df["J_15m_prev"]
    df["J_15m_falling"] = df["J_15m"] < df["J_15m_prev"]

    return df


# ── 信號檢測 ──────────────────────────────────────


def detect_signals(df):
    """掃描所有符合 Jason's Pattern 的點位，回傳 Signal DataFrame"""
    signals = []

    for i in range(KDJ_PERIOD + DMI_PERIOD + 5, len(df)):
        row = df.iloc[i]

        # 需要前一根的數據
        if pd.isna(row["J_prev"]) or pd.isna(row["DI+"]) or pd.isna(row["EMA30"]):
            continue

        # KDJ 黃金交叉: J 上穿 K 和 D (前一根 J<=K 且 J<=D, 這根 J>K 且 J>D)
        golden_cross = (
            row["J_prev"] <= row["K_prev"]
            and row["J_prev"] <= row["D_prev"]
            and row["J"] > row["K"]
            and row["J"] > row["D"]
        )

        # KDJ 死亡交叉: J 下穿 K 和 D
        death_cross = (
            row["J_prev"] >= row["K_prev"]
            and row["J_prev"] >= row["D_prev"]
            and row["J"] < row["K"]
            and row["J"] < row["D"]
        )

        if golden_cross:
            # 做多條件
            if (row["DI+"] > row["DI-"]
                and row["DI+"] > DI_THRESHOLD
                and row["DI_Gap"] > DI_GAP_MIN
                and row["J_15m_rising"]
                and row["Close"] > row["EMA30"]):
                signals.append({
                    "idx": i,
                    "time": row.name,
                    "direction": "LONG",
                    "entry_price": row["Close"],
                    "di_plus": round(row["DI+"], 2),
                    "di_minus": round(row["DI-"], 2),
                    "di_gap": round(row["DI_Gap"], 2),
                    "j_2m": round(row["J"], 2),
                    "j_15m": round(row["J_15m"], 2),
                    "close_ema30": round(row["Close"] - row["EMA30"], 2),
                })

        elif death_cross:
            # 做空條件
            if (row["DI-"] > row["DI+"]
                and row["DI-"] > DI_THRESHOLD
                and row["DI_Gap"] > DI_GAP_MIN
                and row["J_15m_falling"]
                and row["Close"] < row["EMA30"]):
                signals.append({
                    "idx": i,
                    "time": row.name,
                    "direction": "SHORT",
                    "entry_price": row["Close"],
                    "di_plus": round(row["DI+"], 2),
                    "di_minus": round(row["DI-"], 2),
                    "di_gap": round(row["DI_Gap"], 2),
                    "j_2m": round(row["J"], 2),
                    "j_15m": round(row["J_15m"], 2),
                    "close_ema30": round(row["Close"] - row["EMA30"], 2),
                })

    return pd.DataFrame(signals)


# ── 交易模擬 ──────────────────────────────────────


def simulate_trades(df, signals):
    """對每個信號模擬兩口拆分 + Train Mode"""
    trades = []

    for _, sig in signals.iterrows():
        entry_idx = sig["idx"]
        entry_price = sig["entry_price"]
        direction = sig["direction"]

        if entry_idx + 5 >= len(df):  # 至少留 5 根 K 線
            continue

        multiplier = 1 if direction == "LONG" else -1
        tp1_hit = False
        sl_hit = False
        train_mode = False
        exit_price = entry_price
        exit_time = df.index[entry_idx]
        tp1_price = entry_price + (TP1_PTS * multiplier)
        sl_price = entry_price - (SL_PTS * multiplier)

        for j in range(entry_idx + 1, len(df)):
            bar = df.iloc[j]
            high, low, close = bar["High"], bar["Low"], bar["Close"]

            # 多頭
            if direction == "LONG":
                if not tp1_hit:
                    if high >= tp1_price:
                        tp1_hit = True
                        # 第一口獲利了結，第二口 EMA10 追蹤
                        trail_sl = bar["EMA10"]
                        # 最低不低於原 SL
                        sl_price = max(trail_sl, sl_price)
                    elif low <= sl_price:
                        sl_hit = True
                        exit_price = sl_price
                        exit_time = bar.name
                        break
                else:
                    # Train Mode
                    train_mode = True
                    trail_sl = bar["EMA10"]
                    sl_price = max(trail_sl, sl_price)
                    if low <= sl_price:
                        exit_price = sl_price
                        exit_time = bar.name
                        break

            # 空頭
            else:
                if not tp1_hit:
                    if low <= tp1_price:
                        tp1_hit = True
                        trail_sl = bar["EMA10"]
                        sl_price = min(trail_sl, sl_price)
                    elif high >= sl_price:
                        sl_hit = True
                        exit_price = sl_price
                        exit_time = bar.name
                        break
                else:
                    train_mode = True
                    trail_sl = bar["EMA10"]
                    sl_price = min(trail_sl, sl_price)
                    if high >= sl_price:
                        exit_price = sl_price
                        exit_time = bar.name
                        break
        else:
            # 跑到最後都沒出場
            exit_price = df.iloc[-1]["Close"]
            exit_time = df.index[-1]

        tp1_pnl = TP1_PTS * multiplier * 2  # 每點 $2, 半口 1 口
        if tp1_hit:
            # 第一口 TP1 鎖利，第二口看 Train Mode 結果
            leg1_pnl = TP1_PTS * 2  # $/pt for 1 lot
            leg2_pnl = (exit_price - entry_price) * multiplier * 2
            total_pnl = leg1_pnl + leg2_pnl
            total_pts = TP1_PTS + (exit_price - entry_price) * multiplier
            status = "TP1+TRAIN" if train_mode else "TP1_ONLY"
            if train_mode and ((direction == "LONG" and exit_price <= sl_price)
                              or (direction == "SHORT" and exit_price >= sl_price)):
                status = "TP1+Trail"
        elif sl_hit:
            total_pnl = (sl_price - entry_price) * multiplier * 4  # 2口全損
            total_pts = (sl_price - entry_price) * multiplier * 2  # 2口
            status = "SL"
        else:
            total_pnl = (exit_price - entry_price) * multiplier * 4  # 2口
            total_pts = (exit_price - entry_price) * multiplier * 2  # 2口
            status = "OPEN"

        trades.append({
            "time": sig["time"],
            "direction": direction,
            "entry": entry_price,
            "exit": exit_price,
            "exit_time": exit_time,
            "tp1_hit": tp1_hit,
            "sl_hit": sl_hit,
            "train_mode": train_mode,
            "pnl_pts": round(total_pts, 2),
            "pnl_usd": round(total_pnl, 2),
            "status": status,
            "di_gap": sig["di_gap"],
            "j_2m": sig["j_2m"],
            "j_15m": sig["j_15m"],
        })

    return pd.DataFrame(trades)


# ── 績效分析 ──────────────────────────────────────


def get_session(hour_utc):
    for name, (start, end) in SESSIONS.items():
        if start < end:
            # 正常區間
            if start <= hour_utc < end:
                return name
        else:
            # 跨午夜 (如 22~5)
            if hour_utc >= start or hour_utc < end:
                return name
    return "其他"


def analyze_performance(df, trades):
    """產出綜合績效報告"""
    if trades.empty:
        print("\n⚠️ 沒有符合條件的交易記錄")
        return {}

    total = len(trades)
    wins = trades[trades["pnl_pts"] > 0]
    losses = trades[trades["pnl_pts"] < 0]
    win_count = len(wins)
    loss_count = len(losses)
    win_rate = win_count / total * 100 if total else 0

    avg_win = wins["pnl_pts"].mean() if win_count else 0
    avg_loss = abs(losses["pnl_pts"].mean()) if loss_count else 0
    profit_factor = (
        wins["pnl_pts"].sum() / abs(losses["pnl_pts"].sum())
        if loss_count else float("inf")
    )
    rr_ratio = avg_win / avg_loss if avg_loss else 0

    total_pnl = trades["pnl_pts"].sum()
    equity = trades["pnl_pts"].cumsum()
    running_max = equity.cummax()
    drawdown = running_max - equity
    max_dd = drawdown.max()
    max_dd_pct = (max_dd / running_max.max() * 100) if running_max.max() > 0 else 0

    # Sharpe Ratio (假設無風險利率 = 0)
    returns = trades["pnl_pts"]
    sharpe = (returns.mean() / returns.std() * np.sqrt(252)
              ) if returns.std() > 0 else 0

    # 時間段統計
    trades_with_session = trades.copy()
    trades_with_session["session"] = trades_with_session["time"].apply(
        lambda t: get_session(t.hour)
    )

    session_stats = {}
    for sess_name in SESSIONS:
        sess_trades = trades_with_session[trades_with_session["session"] == sess_name]
        if len(sess_trades) > 0:
            sess_wins = len(sess_trades[sess_trades["pnl_pts"] > 0])
            session_stats[sess_name] = {
                "trades": len(sess_trades),
                "wins": sess_wins,
                "win_rate": sess_wins / len(sess_trades) * 100,
                "pnl": round(sess_trades["pnl_pts"].sum(), 2),
            }

    # 狀態統計
    status_stats = trades["status"].value_counts().to_dict()

    # 按月份統計
    trades_with_session["month"] = trades_with_session["time"].apply(
        lambda t: t.strftime("%Y-%m")
    )
    monthly = trades_with_session.groupby("month").agg(
        trades=("pnl_pts", "count"),
        wins=("pnl_pts", lambda x: (x > 0).sum()),
        pnl=("pnl_pts", "sum"),
    ).to_dict(orient="index") if False else {}

    monthly_data = {}
    for m, group in trades_with_session.groupby("month"):
        monthly_data[m] = {
            "trades": len(group),
            "wins": int((group["pnl_pts"] > 0).sum()),
            "pnl": round(group["pnl_pts"].sum(), 2),
        }

    return {
        "total_trades": total,
        "win_count": win_count,
        "loss_count": loss_count,
        "win_rate": round(win_rate, 2),
        "avg_win_pts": round(avg_win, 2),
        "avg_loss_pts": round(avg_loss, 2),
        "profit_factor": round(profit_factor, 3),
        "rr_ratio": round(rr_ratio, 2),
        "total_pnl_pts": round(total_pnl, 2),
            "total_pnl_usd": round(total_pnl * 2, 2),  # 2口 MNQ, $2/pt each → total_pts × 2
        "max_dd_pts": round(max_dd, 2),
        "max_dd_pct": round(max_dd_pct, 2),
        "sharpe": round(sharpe, 3),
        "session_stats": session_stats,
        "status_stats": status_stats,
        "monthly": monthly_data,
    }


# ── 輸出 ──────────────────────────────────────────


def print_report(stats, trades):
    """漂亮的績效報表輸出"""
    sep = "=" * 60
    print(f"\n{sep}")
    print("  📊 MNQ Jason's Pattern 回測報告")
    print(f"  時間框架: {MINOR_TF} | 回測期間: 最近 {LOOKBACK_DAYS} 天")
    print(f"{sep}")

    # ── 總覽 ──
    print(f"\n📈 總交易次數:    {stats['total_trades']}")
    print(f"   ✅ 盈利次數:    {stats['win_count']} ({stats['win_rate']}%)")
    print(f"   ❌ 虧損次數:    {stats['loss_count']}")
    print(f"   💰 總盈虧:      {stats['total_pnl_pts']:+.2f} pts ({stats['total_pnl_usd']:+.2f} USD)")
    print(f"   📉 最大回撤:    {stats['max_dd_pts']:.2f} pts ({stats['max_dd_pct']:.2f}%)")
    print(f"   ⚡ Sharpe Ratio: {stats['sharpe']}")

    # ── 勝率細項 ──
    print(f"\n🎯 勝率分析:")
    print(f"   勝率:        {stats['win_rate']}%")
    print(f"   平均盈利:    +{stats['avg_win_pts']} pts")
    print(f"   平均虧損:    -{stats['avg_loss_pts']} pts")
    print(f"   盈虧比:      {stats['rr_ratio']}")
    print(f"   Profit Factor: {stats['profit_factor']}")

    # ── 時間段 ──
    print(f"\n🕐 時間段統計 (UTC):")
    for sess_name, ss in stats["session_stats"].items():
        print(f"   {sess_name}: {ss['trades']}筆, "
              f"勝率{ss['win_rate']:.1f}%, "
              f"盈虧{ss['pnl']:+.2f}pts")

    # ── 狀態分布 ──
    print(f"\n📋 交易結果分布:")
    for status, count in stats["status_stats"].items():
        print(f"   {status}: {count} 筆")

    # ── 月績效 ──
    if stats["monthly"]:
        print(f"\n📅 月度績效:")
        for month, ms in sorted(stats["monthly"].items()):
            print(f"   {month}: {ms['trades']}筆, "
                  f"勝率{ms['wins']/ms['trades']*100:.0f}%, "
                  f"盈虧{ms['pnl']:+.2f}pts")

    print(f"\n{sep}")


def plot_results(df, trades, stats):
    """繪製 Equity Curve + 交易標記"""
    fig, axes = plt.subplots(3, 1, figsize=(16, 10), sharex=True)

    # ── Panel 1: Equity Curve ──
    ax1 = axes[0]
    if not trades.empty:
        equity = trades.set_index("time")["pnl_pts"].cumsum()
        ax1.fill_between(equity.index, equity.values, 0,
                         alpha=0.3, color="#00d2ff")
        ax1.plot(equity.index, equity.values, color="#00d2ff", lw=2)
        ax1.axhline(y=0, color="#ffffff", lw=0.5, ls="--", alpha=0.5)
        ax1.set_ylabel("累積盈虧 (pts)", fontsize=11)

    # ── Panel 2: 價格 + EMA + 交易標記 ──
    ax2 = axes[1]
    close_data = df["Close"].iloc[-len(df):]
    ax2.plot(df.index, df["Close"], color="#a0a0ff", lw=1, alpha=0.7, label="Close")
    ax2.plot(df.index, df["EMA30"], color="#ffcc00", lw=1.2, alpha=0.8, label="EMA30")
    ax2.plot(df.index, df["EMA10"], color="#00ffcc", lw=0.8, alpha=0.6, label="EMA10")

    if not trades.empty:
        long_mask = trades["direction"] == "LONG"
        short_mask = trades["direction"] == "SHORT"
        long_trades = trades[long_mask]
        short_trades = trades[short_mask]

        for t in long_trades.itertuples():
            color = "#00ff88" if t.pnl_pts > 0 else "#ff4466"
            ax2.scatter(t.time, t.entry, color=color, s=30, zorder=5,
                        marker="^", edgecolors="white", linewidth=0.5)

        for t in short_trades.itertuples():
            color = "#00ff88" if t.pnl_pts > 0 else "#ff4466"
            ax2.scatter(t.time, t.entry, color=color, s=30, zorder=5,
                        marker="v", edgecolors="white", linewidth=0.5)

    ax2.set_ylabel("價格", fontsize=11)
    ax2.legend(loc="upper left", fontsize=9)

    # ── Panel 3: DI+ DI- + DI Gap ──
    ax3 = axes[2]
    ax3.plot(df.index, df["DI+"], color="#00ff88", lw=0.8, alpha=0.8, label="DI+")
    ax3.plot(df.index, df["DI-"], color="#ff4466", lw=0.8, alpha=0.8, label="DI-")
    ax3.axhline(y=DI_THRESHOLD, color="#ffffff", lw=0.5, ls="--", alpha=0.4)
    ax3.set_ylabel("DI", fontsize=11)
    ax3.legend(loc="upper left", fontsize=9)

    # 日期格式
    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d %H:%M"))
    for tick in ax3.get_xticklabels():
        tick.set_rotation(45)
        tick.set_fontsize(8)

    plt.suptitle(f"MNQ Jason's Pattern 回測 — {MINOR_TF} ({LOOKBACK_DAYS}天)",
                 fontsize=14, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    fname = f"jasons_pattern_backtest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    fpath = os.path.join(OUTPUT_DIR, fname)
    plt.savefig(fpath, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\n📷 圖表已儲存: {fpath}")
    return fpath


# ── 主流程 ────────────────────────────────────────

def main():
    print("🚀 MNQ Jason's Pattern 回測引擎啟動")
    print(f"   參數: KDJ={KDJ_PERIOD}, DMI={DMI_PERIOD}, "
          f"DI門檻={DI_THRESHOLD}, DI Gap>{DI_GAP_MIN}")
    print(f"   時間框架: {MINOR_TF} (2分K 約=3分K替代)")

    # 1. 下載數據
    df_minor, df_major = fetch_data()

    # 2. 計算指標
    print("\n🧮 計算指標 (KDJ, DMI, EMA)...")
    df = prepare_data(df_minor, df_major)
    print(f"   有效 K 線: {len(df)}")

    # 3. 掃描信號
    print("\n🔍 掃描 Jason's Pattern...")
    signals = detect_signals(df)
    print(f"   符合條件的信號: {len(signals)} 筆")

    if signals.empty:
        print("⚠️  60天內沒有找到符合所有條件的信號。")
        print("   可能原因: 2分K資料量較少，盤整期較多。")
        print("   建議: 改用5分K試試，或放寬部分條件。")
        return

    print(f"   {'LONG' if (signals['direction']=='LONG').sum() else ''}"
          f"做多: {(signals['direction']=='LONG').sum()}筆, "
          f"做空: {(signals['direction']=='SHORT').sum()}筆")

    # 4. 交易模擬
    print("\n💼 模擬交易 (兩口拆分 + Train Mode)...")
    trades = simulate_trades(df, signals)
    if trades.empty:
        print("⚠️  沒有足夠 K 線資料可模擬交易")
        return

    # 5. 分析
    stats = analyze_performance(df, trades)

    # 6. 輸出
    print_report(stats, trades)

    # 7. 圖表
    chart_path = plot_results(df, trades, stats)

    # 8. 詳細交易明細
    if len(trades) <= 30:
        print("\n📝 交易明細:")
        pd.set_option("display.max_columns", 10)
        pd.set_option("display.width", 120)
        summary = trades[["time", "direction", "entry", "exit",
                          "pnl_pts", "pnl_usd", "status"]].copy()
        summary["time"] = summary["time"].apply(lambda t: t.strftime("%m/%d %H:%M"))
        summary["exit_time"] = trades["exit_time"].apply(
            lambda t: t.strftime("%m/%d %H:%M"))
        summary.columns = ["進場時間", "方向", "進場價", "出場價",
                           "盈虧(pts)", "盈虧($)", "狀態"]
        print(summary.to_string(index=False))

    # 儲存詳盡資料
    json_path = chart_path.replace(".png", ".json")
    output_data = {
        "config": {
            "ticker": TICKER,
            "timeframe": MINOR_TF,
            "lookback_days": LOOKBACK_DAYS,
            "kdj_period": KDJ_PERIOD,
            "dmi_period": DMI_PERIOD,
            "di_threshold": DI_THRESHOLD,
            "di_gap_min": DI_GAP_MIN,
            "sl_pts": SL_PTS,
            "tp1_pts": TP1_PTS,
        },
        "stats": {k: v for k, v in stats.items()
                  if k not in ("session_stats", "status_stats", "monthly")},
        "session_stats": stats["session_stats"],
        "status_stats": stats["status_stats"],
        "trades": trades.to_dict(orient="records") if not trades.empty else [],
    }
    with open(json_path, "w") as f:
        json.dump(output_data, f, indent=2, default=str)
    print(f"📄 詳細數據已儲存: {json_path}")

    print("\n✅ 回測完成！")


if __name__ == "__main__":
    main()
