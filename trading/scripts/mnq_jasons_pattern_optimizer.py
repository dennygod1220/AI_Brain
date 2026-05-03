#!/usr/bin/env python3
"""
MNQ Jason's Pattern 參數優化器 (Phase 2)
==============================================
Grid Search: KDJ 週期 × DI 門檻 × EMA 長度
產出最佳參數組合 + 熱力圖 + 70/30 Train/Test split 驗證

Usage:
  python3 mnq_jasons_pattern_optimizer.py           # 5m, 55天
  python3 mnq_jasons_pattern_optimizer.py --tf 2m   # 2分K
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta, timezone
from itertools import product

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

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

font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
if os.path.exists(font_path):
    from matplotlib import font_manager
    font_manager.fontManager.addfont(font_path)
    plt.rcParams["font.sans-serif"] = ["Noto Sans CJK JP"]
    plt.rcParams["font.family"] = "sans-serif"

# ── 預設 Grid Search 範圍 ──────────────────────────

KDJ_GRID = [9, 14, 21]
DI_THRESH_GRID = [15, 20, 25, 30]
EMA_MID_GRID = [30, 50, 100]
DI_GAP_MIN = 10
DMI_PERIOD = 14
EMA_FAST = 10
EMA_SLOW = 60
SL_PTS = 18
TP1_PTS = 12

# 時間段 (台灣時間)
SESSIONS = {
    "亞洲盤": (22, 5),
    "歐洲盤": (8, 12),
    "美盤": (12, 17),
}

# ── 指標計算 ──────────────────────────────────────


def calc_ema(close, period):
    return close.ewm(span=period, adjust=False).mean()


def calc_kdj(df, period):
    low_min = df["Low"].rolling(window=period).min()
    high_max = df["High"].rolling(window=period).max()
    rsv = ((df["Close"] - low_min) / (high_max - low_min)) * 100
    k = rsv.ewm(span=3, adjust=False).mean()
    d = k.ewm(span=3, adjust=False).mean()
    j = 3 * k - 2 * d
    return k, d, j


def calc_dmi(df, period):
    high, low, close = df["High"], df["Low"], df["Close"]
    prev_close = close.shift(1)
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    up_move = high - high.shift(1)
    down_move = low.shift(1) - low
    dm_plus = pd.Series(np.where(
        (up_move > 0) & (up_move > down_move), up_move, 0
    ), index=df.index)
    dm_minus = pd.Series(np.where(
        (down_move > 0) & (down_move > up_move), down_move, 0
    ), index=df.index)
    tr_s = tr.ewm(span=period, adjust=False).mean()
    dm_plus_s = dm_plus.ewm(span=period, adjust=False).mean()
    dm_minus_s = dm_minus.ewm(span=period, adjust=False).mean()
    di_plus = (dm_plus_s / tr_s) * 100
    di_minus = (dm_minus_s / tr_s) * 100
    return di_plus, di_minus


def get_session(hour_utc):
    for name, (start, end) in SESSIONS.items():
        if start < end:
            if start <= hour_utc < end:
                return name
        else:
            if hour_utc >= start or hour_utc < end:
                return name
    return "其他"


# ── 參數化回測引擎 ──────────────────────────────


def run_backtest(df_minor, df_major, kdj_period, di_threshold, ema_mid):
    """
    接受原始 OHLCV DataFrame + 參數，回傳 stats dict。

    回傳格式:
    {
        "total_trades": int,
        "win_count": int,
        "win_rate": float,
        "avg_win_pts": float,
        "avg_loss_pts": float,
        "profit_factor": float,
        "rr_ratio": float,
        "total_pnl_pts": float,
        "sharpe": float,
        "max_dd_pts": float,
        "session_stats": dict,
        "status_stats": dict,
    }
    """
    df = df_minor.copy()

    # ── 指標 ──
    df["EMA10"] = calc_ema(df["Close"], EMA_FAST)
    df["EMA30"] = calc_ema(df["Close"], ema_mid)
    df["EMA60"] = calc_ema(df["Close"], EMA_SLOW)

    k, d, j = calc_kdj(df, kdj_period)
    df["K"] = k
    df["D"] = d
    df["J"] = j

    di_plus, di_minus = calc_dmi(df, DMI_PERIOD)
    df["DI+"] = di_plus
    df["DI-"] = di_minus
    df["DI_Gap"] = (df["DI+"] - df["DI-"]).abs()

    df["J_prev"] = df["J"].shift(1)
    df["K_prev"] = df["K"].shift(1)
    df["D_prev"] = df["D"].shift(1)

    # 15分K J值 (不管參數，固定 KDJ=9)
    df_major = df_major.copy()
    k_m, d_m, j_m = calc_kdj(df_major, 9)
    df_major["J_15m"] = j_m
    j_15m_aligned = df_major["J_15m"].reindex(df.index, method="ffill")
    j_15m_prev = df_major["J_15m"].shift(1).reindex(df.index, method="ffill")
    df["J_15m"] = j_15m_aligned
    df["J_15m_prev"] = j_15m_prev
    df["J_15m_rising"] = df["J_15m"] > df["J_15m_prev"]
    df["J_15m_falling"] = df["J_15m"] < df["J_15m_prev"]

    # ── 信號檢測 ──
    signals = []
    for i in range(kdj_period + DMI_PERIOD + 5, len(df)):
        row = df.iloc[i]
        if pd.isna(row["J_prev"]) or pd.isna(row["DI+"]) or pd.isna(row["EMA30"]):
            continue

        golden_cross = (
            row["J_prev"] <= row["K_prev"]
            and row["J_prev"] <= row["D_prev"]
            and row["J"] > row["K"]
            and row["J"] > row["D"]
        )
        death_cross = (
            row["J_prev"] >= row["K_prev"]
            and row["J_prev"] >= row["D_prev"]
            and row["J"] < row["K"]
            and row["J"] < row["D"]
        )

        if golden_cross:
            if (row["DI+"] > row["DI-"]
                    and row["DI+"] > di_threshold
                    and row["DI_Gap"] > DI_GAP_MIN
                    and row["J_15m_rising"]
                    and row["Close"] > row["EMA30"]):
                signals.append({
                    "idx": i, "time": row.name, "direction": "LONG",
                    "entry_price": round(row["Close"], 2),
                })
        elif death_cross:
            if (row["DI-"] > row["DI+"]
                    and row["DI-"] > di_threshold
                    and row["DI_Gap"] > DI_GAP_MIN
                    and row["J_15m_falling"]
                    and row["Close"] < row["EMA30"]):
                signals.append({
                    "idx": i, "time": row.name, "direction": "SHORT",
                    "entry_price": round(row["Close"], 2),
                })

    if not signals:
        return {
            "total_trades": 0, "win_count": 0, "loss_count": 0,
            "win_rate": 0, "avg_win_pts": 0, "avg_loss_pts": 0,
            "profit_factor": 0, "rr_ratio": 0, "total_pnl_pts": 0,
            "sharpe": 0, "max_dd_pts": 0, "session_stats": {},
            "status_stats": {},
        }

    # ── 交易模擬 ──
    trades = []
    for sig in signals:
        entry_idx = sig["idx"]
        entry_price = sig["entry_price"]
        direction = sig["direction"]

        if entry_idx + 5 >= len(df):
            continue

        multiplier = 1 if direction == "LONG" else -1
        tp1_hit = False
        sl_hit = False
        train_mode = False
        exit_price = entry_price
        tp1_price = entry_price + (TP1_PTS * multiplier)
        sl_price = entry_price - (SL_PTS * multiplier)

        for j in range(entry_idx + 1, len(df)):
            bar = df.iloc[j]
            high, low = bar["High"], bar["Low"]

            if direction == "LONG":
                if not tp1_hit:
                    if high >= tp1_price:
                        tp1_hit = True
                        trail_sl = bar["EMA10"]
                        sl_price = max(trail_sl, sl_price)
                    elif low <= sl_price:
                        sl_hit = True
                        exit_price = sl_price
                        break
                else:
                    train_mode = True
                    trail_sl = bar["EMA10"]
                    sl_price = max(trail_sl, sl_price)
                    if low <= sl_price:
                        exit_price = sl_price
                        break
            else:
                if not tp1_hit:
                    if low <= tp1_price:
                        tp1_hit = True
                        trail_sl = bar["EMA10"]
                        sl_price = min(trail_sl, sl_price)
                    elif high >= sl_price:
                        sl_hit = True
                        exit_price = sl_price
                        break
                else:
                    train_mode = True
                    trail_sl = bar["EMA10"]
                    sl_price = min(trail_sl, sl_price)
                    if high >= sl_price:
                        exit_price = sl_price
                        break
        else:
            exit_price = df.iloc[-1]["Close"]

        if tp1_hit:
            leg1_pnl = TP1_PTS * 2
            leg2_pnl = (exit_price - entry_price) * multiplier * 2
            total_pnl = leg1_pnl + leg2_pnl
            total_pts = TP1_PTS + (exit_price - entry_price) * multiplier
            status = "TP1+Trail" if train_mode else "TP1_ONLY"
        elif sl_hit:
            total_pnl = (sl_price - entry_price) * multiplier * 4
            total_pts = (sl_price - entry_price) * multiplier * 2
            status = "SL"
        else:
            total_pnl = (exit_price - entry_price) * multiplier * 4
            total_pts = (exit_price - entry_price) * multiplier * 2
            status = "OPEN"

        trades.append({
            "time": sig["time"],
            "direction": direction,
            "pnl_pts": round(total_pts, 2),
            "pnl_usd": round(total_pnl, 2),
            "status": status,
        })

    if not trades:
        return {
            "total_trades": 0, "win_count": 0, "loss_count": 0,
            "win_rate": 0, "avg_win_pts": 0, "avg_loss_pts": 0,
            "profit_factor": 0, "rr_ratio": 0, "total_pnl_pts": 0,
            "sharpe": 0, "max_dd_pts": 0, "session_stats": {},
            "status_stats": {},
        }

    trades_df = pd.DataFrame(trades)

    # ── 績效計算 ──
    total = len(trades_df)
    wins = trades_df[trades_df["pnl_pts"] > 0]
    losses = trades_df[trades_df["pnl_pts"] < 0]
    win_count, loss_count = len(wins), len(losses)
    win_rate = win_count / total * 100 if total else 0

    avg_win = wins["pnl_pts"].mean() if win_count else 0
    avg_loss = abs(losses["pnl_pts"].mean()) if loss_count else 0
    profit_factor = (
        wins["pnl_pts"].sum() / abs(losses["pnl_pts"].sum())
        if loss_count else float("inf")
    )
    rr_ratio = avg_win / avg_loss if avg_loss else 0
    total_pnl = trades_df["pnl_pts"].sum()

    equity = trades_df["pnl_pts"].cumsum()
    running_max = equity.cummax()
    dd = running_max - equity
    max_dd = dd.max()

    returns = trades_df["pnl_pts"]
    sharpe = (returns.mean() / returns.std() * np.sqrt(252)
              ) if returns.std() > 0 else 0

    # 時間段統計
    trades_df["session"] = trades_df["time"].apply(
        lambda t: get_session(t.hour))
    session_stats = {}
    for sess_name in SESSIONS:
        sess_trades = trades_df[trades_df["session"] == sess_name]
        if len(sess_trades) > 0:
            sess_wins = len(sess_trades[sess_trades["pnl_pts"] > 0])
            session_stats[sess_name] = {
                "trades": len(sess_trades),
                "wins": sess_wins,
                "win_rate": round(sess_wins / len(sess_trades) * 100, 1),
                "pnl": round(sess_trades["pnl_pts"].sum(), 2),
            }

    status_stats = trades_df["status"].value_counts().to_dict()

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
        "sharpe": round(sharpe, 3),
        "max_dd_pts": round(max_dd, 2),
        "session_stats": session_stats,
        "status_stats": {k: int(v) for k, v in status_stats.items()},
    }


# ── 數據下載 ──────────────────────────────────────


def fetch_data(tf, lookback):
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=lookback)
    print(f"⏬ 下載 NQ=F {tf} ({lookback}天)...")
    df_minor = yf.download("NQ=F", interval=tf, start=start, end=end,
                           progress=False, multi_level_index=False)
    print(f"⏬ 下載 NQ=F 15m...")
    df_major = yf.download("NQ=F", interval="15m", start=start, end=end,
                           progress=False, multi_level_index=False)
    if df_minor.empty or df_major.empty:
        print("❌ 無法取得數據")
        sys.exit(1)
    print(f"   → {tf}: {len(df_minor)} 根 K 線")
    print(f"   → 15m: {len(df_major)} 根 K 線")
    # 清理 multi-index columns
    df_minor.columns = [c[0] if isinstance(c, tuple) else c for c in df_minor.columns]
    df_major.columns = [c[0] if isinstance(c, tuple) else c for c in df_major.columns]
    return df_minor, df_major


# ── Grid Search ──────────────────────────────────


def grid_search(df_minor, df_major, kdj_grid, di_grid, ema_grid):
    """執行 Grid Search，回傳每組參數的結果清單"""
    total = len(kdj_grid) * len(di_grid) * len(ema_grid)
    results = []

    print(f"\n🔬 Grid Search: {total} 組參數組合")
    print(f"   KDJ週期={kdj_grid}")
    print(f"   DI門檻={di_grid}")
    print(f"   EMA中線={ema_grid}")
    print()

    combo_idx = 0
    for kdj, di, ema in product(kdj_grid, di_grid, ema_grid):
        combo_idx += 1
        label = f"KDJ{kdj}_DI{di}_EMA{ema}"
        print(f"   [{combo_idx:02d}/{total:02d}] {label} ... ", end="", flush=True)

        stats = run_backtest(df_minor, df_major, kdj, di, ema)

        # Composite score: Sharpe × WinRate × sqrt(Trades) — 綜合評估
        # 如果沒交易直接跳過
        trades_n = stats["total_trades"]
        if trades_n == 0:
            print("❌ 0 筆交易")
            results.append({
                "kdj": kdj, "di_thresh": di, "ema_mid": ema,
                "trades": 0, "win_rate": 0, "sharpe": 0,
                "profit_factor": 0, "rr_ratio": 0, "pnl_pts": 0,
                "score": 0,
            })
            continue

        score = (
            stats["sharpe"]
            * (stats["win_rate"] / 100)
            * (min(trades_n, 200) / 200)  # 交易次數獎勵但 capped
        )

        print(f"✅ {stats['total_trades']}筆, "
              f"勝率{stats['win_rate']}%, "
              f"Sharpe {stats['sharpe']}, "
              f"盈虧{stats['total_pnl_pts']:+.0f}pts")

        results.append({
            "kdj": kdj,
            "di_thresh": di,
            "ema_mid": ema,
            "trades": trades_n,
            "win_rate": stats["win_rate"],
            "sharpe": stats["sharpe"],
            "profit_factor": stats["profit_factor"],
            "rr_ratio": stats["rr_ratio"],
            "pnl_pts": stats["total_pnl_pts"],
            "score": round(score, 4),
            "stats": stats,
        })

    return results


# ── Train/Test Split Validation ─────────────────


def train_test_validate(df_minor, df_major, top_combos, train_pct=0.7):
    """
    將數據依時間分割為 train/test，對 top combos 做驗證。
    回傳 validated list: [{combo, train_stats, test_stats, score_diff}]
    """
    split_idx = int(len(df_minor) * train_pct)
    train_minor = df_minor.iloc[:split_idx].copy()
    test_minor = df_minor.iloc[split_idx:].copy()
    # 15m 也要切
    split_major = int(len(df_major) * train_pct)
    train_major = df_major.iloc[:split_major].copy()
    test_major = df_major.iloc[split_major:].copy()

    print(f"\n🧪 Train/Test 驗證 (train={train_pct*100:.0f}%, test={(1-train_pct)*100:.0f}%)")
    print(f"   訓練集: {len(train_minor)} 根K線")
    print(f"   測試集: {len(test_minor)} 根K線\n")

    validated = []
    for combo in top_combos:
        kdj, di, ema = combo["kdj"], combo["di_thresh"], combo["ema_mid"]
        label = f"KDJ{kdj}_DI{di}_EMA{ema}"

        train_stats = run_backtest(train_minor, train_major, kdj, di, ema)
        test_stats = run_backtest(test_minor, test_major, kdj, di, ema)

        train_sharpe = train_stats["sharpe"]
        test_sharpe = test_stats["sharpe"]
        score_diff = abs(train_sharpe - test_sharpe)

        print(f"   {label}: "
              f"Train Sharpe={train_sharpe}, "
              f"Test Sharpe={test_sharpe}, "
              f"Diff={score_diff:.3f}"
              f" | Train: {train_stats['total_trades']}筆 "
              f"{train_stats['total_pnl_pts']:+.0f}pts"
              f" | Test: {test_stats['total_trades']}筆 "
              f"{test_stats['total_pnl_pts']:+.0f}pts"
              )

        validated.append({
            "combo": label,
            "kdj": kdj, "di_thresh": di, "ema_mid": ema,
            "train": {
                "trades": train_stats["total_trades"],
                "win_rate": train_stats["win_rate"],
                "sharpe": train_sharpe,
                "profit_factor": train_stats["profit_factor"],
                "pnl_pts": train_stats["total_pnl_pts"],
            },
            "test": {
                "trades": test_stats["total_trades"],
                "win_rate": test_stats["win_rate"],
                "sharpe": test_sharpe,
                "profit_factor": test_stats["profit_factor"],
                "pnl_pts": test_stats["total_pnl_pts"],
            },
            "score_diff": round(score_diff, 3),
        })

    return validated


# ── 繪圖 ─────────────────────────────────────────


def plot_heatmaps(results, output_dir):
    """對每個 EMA 值畫一張熱力圖 (KDJ × DI_Thresh)"""
    for ema_val in sorted(set(r["ema_mid"] for r in results)):
        subset = [r for r in results if r["ema_mid"] == ema_val and r["trades"] > 0]
        if not subset:
            continue

        kdj_vals = sorted(set(r["kdj"] for r in subset))
        di_vals = sorted(set(r["di_thresh"] for r in subset))

        # Sharpe 熱力圖
        sharpe_grid = np.full((len(di_vals), len(kdj_vals)), np.nan)
        # Score 熱力圖
        score_grid = np.full((len(di_vals), len(kdj_vals)), np.nan)
        # Trade count
        trade_grid = np.full((len(di_vals), len(kdj_vals)), np.nan)

        for r in subset:
            k_idx = kdj_vals.index(r["kdj"])
            d_idx = di_vals.index(r["di_thresh"])
            sharpe_grid[d_idx, k_idx] = r["sharpe"]
            score_grid[d_idx, k_idx] = r["score"]
            trade_grid[d_idx, k_idx] = r["trades"]

        fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

        # Heatmap 1: Sharpe
        ax = axes[0]
        norm = mcolors.TwoSlopeNorm(vmin=-0.5, vcenter=1.0, vmax=3.0)
        im = ax.imshow(sharpe_grid, cmap="RdYlGn", aspect="auto", norm=norm,
                       interpolation="nearest")
        for di_idx in range(len(di_vals)):
            for k_idx in range(len(kdj_vals)):
                val = sharpe_grid[di_idx, k_idx]
                if not np.isnan(val):
                    ax.text(k_idx, di_idx, f"{val:.2f}",
                            ha="center", va="center",
                            color="white" if abs(val - 1.0) > 0.5 else "black",
                            fontsize=11, fontweight="bold")
        ax.set_xticks(range(len(kdj_vals)))
        ax.set_xticklabels([f"KDJ={k}" for k in kdj_vals], fontsize=10)
        ax.set_yticks(range(len(di_vals)))
        ax.set_yticklabels([f"DI≥{d}" for d in di_vals], fontsize=10)
        ax.set_title(f"Sharpe Ratio (EMA={ema_val})", fontsize=13, fontweight="bold")
        plt.colorbar(im, ax=ax, shrink=0.8)

        # Heatmap 2: Score
        ax = axes[1]
        norm2 = mcolors.Normalize(vmin=0, vmax=max(np.nanmax(score_grid), 0.5))
        im2 = ax.imshow(score_grid, cmap="YlOrRd", aspect="auto",
                        norm=norm2, interpolation="nearest")
        for di_idx in range(len(di_vals)):
            for k_idx in range(len(kdj_vals)):
                val = score_grid[di_idx, k_idx]
                if not np.isnan(val):
                    ax.text(k_idx, di_idx, f"{val:.2f}",
                            ha="center", va="center",
                            color="white", fontsize=11, fontweight="bold")
        ax.set_xticks(range(len(kdj_vals)))
        ax.set_xticklabels([f"KDJ={k}" for k in kdj_vals], fontsize=10)
        ax.set_yticks(range(len(di_vals)))
        ax.set_yticklabels([f"DI≥{d}" for d in di_vals], fontsize=10)
        ax.set_title(f"Composite Score (EMA={ema_val})", fontsize=13, fontweight="bold")
        plt.colorbar(im2, ax=ax, shrink=0.8)

        # Heatmap 3: Trade Count
        ax = axes[2]
        norm3 = mcolors.Normalize(vmin=0, vmax=np.nanmax(trade_grid))
        im3 = ax.imshow(trade_grid, cmap="Blues", aspect="auto",
                        norm=norm3, interpolation="nearest")
        for di_idx in range(len(di_vals)):
            for k_idx in range(len(kdj_vals)):
                val = trade_grid[di_idx, k_idx]
                if not np.isnan(val):
                    ax.text(k_idx, di_idx, f"{int(val)}",
                            ha="center", va="center",
                            color="white", fontsize=11, fontweight="bold")
        ax.set_xticks(range(len(kdj_vals)))
        ax.set_xticklabels([f"KDJ={k}" for k in kdj_vals], fontsize=10)
        ax.set_yticks(range(len(di_vals)))
        ax.set_yticklabels([f"DI≥{d}" for d in di_vals], fontsize=10)
        ax.set_title(f"Trade Count (EMA={ema_val})", fontsize=13, fontweight="bold")
        plt.colorbar(im3, ax=ax, shrink=0.8)

        plt.suptitle(f"MNQ Jason's Pattern 參數優化 — EMA{ema_val}",
                     fontsize=15, fontweight="bold", y=1.02)
        plt.tight_layout()

        fname = f"grid_heatmap_EMA{ema_val}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fpath = os.path.join(output_dir, fname)
        plt.savefig(fpath, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"📷 熱力圖: {fpath}")


# ── 主流程 ──────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="MNQ Jason's Pattern 參數優化器")
    parser.add_argument("--tf", default="5m", help="時間框架 (5m/2m)")
    parser.add_argument("--days", type=int, default=55, help="回測天數")
    parser.add_argument("--top-n", type=int, default=5,
                        help="Train/Test 驗證 top N")
    args = parser.parse_args()

    print("=" * 65)
    print("  🔬 MNQ Jason's Pattern 參數優化器 (Phase 2)")
    print(f"  {args.tf} | 最近 {args.days} 天")
    print(f"  Grid: KDJ={KDJ_GRID} × DI≥{DI_THRESH_GRID} × EMA={EMA_MID_GRID}")
    print("=" * 65)

    # 1. 下載數據
    df_minor, df_major = fetch_data(args.tf, args.days)

    # 2. Grid Search
    results = grid_search(df_minor, df_major,
                          KDJ_GRID, DI_THRESH_GRID, EMA_MID_GRID)

    # 3. 排名
    results_sorted = sorted(results, key=lambda r: r["score"], reverse=True)

    print(f"\n{'='*65}")
    print("  🏆 Top 10 參數組合 (by Composite Score)")
    print(f"{'='*65}")
    print(f"  {'Rank':<5} {'KDJ':<8} {'DI≥':<8} {'EMA':<8} {'Trades':<8} "
          f"{'WinRate':<10} {'Sharpe':<10} {'PF':<10} {'PnL':<10} {'Score':<8}")
    print(f"  {'─'*5} {'─'*8} {'─'*8} {'─'*8} {'─'*8} "
          f"{'─'*10} {'─'*10} {'─'*10} {'─'*10} {'─'*8}")
    for rank, r in enumerate(results_sorted[:10], 1):
        winrate = f"{r['win_rate']:.1f}%" if r['trades'] > 0 else "N/A"
        sharpe = f"{r['sharpe']:.2f}" if r['trades'] > 0 else "N/A"
        pf = f"{r['profit_factor']:.2f}" if r['trades'] > 0 else "N/A"
        pnl = f"{r['pnl_pts']:+.0f}" if r['trades'] > 0 else "N/A"
        print(f"  #{rank:<3} KDJ={r['kdj']:<4} ≥{r['di_thresh']:<5} "
              f"{r['ema_mid']:<8} {r['trades']:<8} {winrate:<10} "
              f"{sharpe:<10} {pf:<10} {pnl:<10} {r['score']:<8.3f}")

    # 4. 熱力圖
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "screenshots"
    )
    os.makedirs(output_dir, exist_ok=True)
    plot_heatmaps(results, output_dir)

    # 5. Train/Test Validation
    top_combos = results_sorted[:args.top_n]
    validated = train_test_validate(df_minor, df_major, top_combos)

    print(f"\n{'='*65}")
    print("  📋 Train/Test 驗證總結")
    print(f"{'='*65}")
    print(f"  {'Combo':<20} {'Train S':<10} {'Test S':<10} {'Diff':<10} "
          f"{'Train $':<12} {'Test $':<12}")
    print(f"  {'─'*20} {'─'*10} {'─'*10} {'─'*10} {'─'*12} {'─'*12}")
    for v in validated:
        print(f"  {v['combo']:<20} {v['train']['sharpe']:<10.2f} "
              f"{v['test']['sharpe']:<10.2f} {v['score_diff']:<10.3f} "
              f"{v['train']['pnl_pts']:<+8.0f}pts     "
              f"{v['test']['pnl_pts']:<+8.0f}pts")

    # 6. 最佳組合詳細報表
    best = results_sorted[0]
    best_stats = best.get("stats")
    if best_stats:
        print(f"\n{'='*65}")
        print(f"  ⭐ 最佳參數: KDJ={best['kdj']}, DI≥{best['di_thresh']}, "
              f"EMA={best['ema_mid']}")
        print(f"{'='*65}")
        print(f"  總交易: {best_stats['total_trades']}")
        print(f"  勝率: {best_stats['win_rate']}%")
        print(f"  Sharpe: {best_stats['sharpe']}")
        print(f"  Profit Factor: {best_stats['profit_factor']}")
        print(f"  盈虧比: {best_stats['rr_ratio']}")
        print(f"  總盈虧: {best_stats['total_pnl_pts']:+.0f} pts")
        if best_stats["session_stats"]:
            print(f"\n  時間段:")
            for s_name, s_s in best_stats["session_stats"].items():
                print(f"    {s_name}: {s_s['trades']}筆, "
                      f"勝率{s_s['win_rate']}%, 盈虧{s_s['pnl']:+.0f}pts")

    # 7. 儲存完整結果
    output_data = {
        "config": {
            "timeframe": args.tf,
            "lookback_days": args.days,
            "grid": {
                "kdj_periods": KDJ_GRID,
                "di_thresholds": DI_THRESH_GRID,
                "ema_mid_values": EMA_MID_GRID,
            },
            "defaults": {
                "dmi_period": DMI_PERIOD,
                "di_gap_min": DI_GAP_MIN,
                "sl_pts": SL_PTS,
                "tp1_pts": TP1_PTS,
            },
        },
        "top10": [
            {
                "rank": i + 1,
                "kdj": r["kdj"],
                "di_thresh": r["di_thresh"],
                "ema_mid": r["ema_mid"],
                "trades": r["trades"],
                "win_rate": r["win_rate"],
                "sharpe": r["sharpe"],
                "profit_factor": r["profit_factor"],
                "pnl_pts": r["pnl_pts"],
                "score": r["score"],
            }
            for i, r in enumerate(results_sorted[:10])
        ],
        "all_results": [
            {
                "kdj": r["kdj"],
                "di_thresh": r["di_thresh"],
                "ema_mid": r["ema_mid"],
                "trades": r["trades"],
                "win_rate": r["win_rate"],
                "sharpe": r["sharpe"],
                "profit_factor": r["profit_factor"],
                "pnl_pts": r["pnl_pts"],
                "score": r["score"],
            }
            for r in results_sorted
        ],
        "validation": [
            {
                "combo": v["combo"],
                "train_sharpe": v["train"]["sharpe"],
                "test_sharpe": v["test"]["sharpe"],
                "score_diff": v["score_diff"],
                "train_pnl": v["train"]["pnl_pts"],
                "test_pnl": v["test"]["pnl_pts"],
            }
            for v in validated
        ],
        "best_params": {
            "kdj": best["kdj"],
            "di_thresh": best["di_thresh"],
            "ema_mid": best["ema_mid"],
            "stats": best_stats,
        },
    }

    json_path = os.path.join(output_dir,
        f"grid_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(json_path, "w") as f:
        json.dump(output_data, f, indent=2, default=str)
    print(f"\n📄 完整數據已儲存: {json_path}")
    print("\n✅ 優化完成！")


if __name__ == "__main__":
    main()
