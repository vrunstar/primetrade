"""
plots.py
Generates all charts for the sentiment vs. trader performance analysis and
saves them as PNGs into the charts/ directory.
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from data_loader import SENTIMENT_ORDER, SENTIMENT_COLORS
from metrics import (
    pnl_winrate_by_sentiment, activity_by_sentiment, top_bottom_accounts,
    buy_sell_bias, fee_impact, top_coins, daily_sentiment_vs_pnl,
    account_level_stats, pnl_by_sentiment_and_coin,
)

CHARTS_DIR = os.path.join(os.path.dirname(__file__), "charts")
plt.rcParams["figure.dpi"] = 150


def _save(fig, name):
    os.makedirs(CHARTS_DIR, exist_ok=True)
    path = os.path.join(CHARTS_DIR, name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"saved {path}")


def plot_pnl_winrate(merged):
    summary, _ = pnl_winrate_by_sentiment(merged)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    axes[0].bar(SENTIMENT_ORDER, summary["mean_pnl"], color=SENTIMENT_COLORS)
    axes[0].set_title("Average Closed PnL per Trade by Market Sentiment", fontweight="bold")
    axes[0].set_ylabel("Avg Closed PnL (USD)")
    axes[0].tick_params(axis="x", rotation=20)
    axes[0].axhline(0, color="black", linewidth=0.8)

    axes[1].bar(SENTIMENT_ORDER, summary["win_rate"] * 100, color=SENTIMENT_COLORS)
    axes[1].set_title("Win Rate by Market Sentiment", fontweight="bold")
    axes[1].set_ylabel("Win Rate (%)")
    axes[1].tick_params(axis="x", rotation=20)
    axes[1].set_ylim(0, 100)
    plt.tight_layout()
    _save(fig, "01_pnl_winrate.png")


def plot_activity(merged):
    activity = activity_by_sentiment(merged)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    axes[0].bar(SENTIMENT_ORDER, activity["trades_per_day"], color=SENTIMENT_COLORS)
    axes[0].set_title("Trading Activity: Trades per Day by Sentiment", fontweight="bold")
    axes[0].set_ylabel("Avg Trades / Day")
    axes[0].tick_params(axis="x", rotation=20)

    axes[1].bar(SENTIMENT_ORDER, activity["volume_per_day_musd"], color=SENTIMENT_COLORS)
    axes[1].set_title("Trading Volume per Day by Sentiment", fontweight="bold")
    axes[1].set_ylabel("Avg Volume / Day (USD Millions)")
    axes[1].tick_params(axis="x", rotation=20)
    plt.tight_layout()
    _save(fig, "02_activity.png")


def plot_top_vs_bottom_pnl(merged):
    _, top_df, bottom_df = top_bottom_accounts(merged)
    top_mean = top_df.groupby("classification")["Closed PnL"].mean().reindex(SENTIMENT_ORDER)
    bottom_mean = bottom_df.groupby("classification")["Closed PnL"].mean().reindex(SENTIMENT_ORDER)

    fig, ax = plt.subplots(figsize=(11, 5.5))
    x = range(len(SENTIMENT_ORDER))
    w = 0.35
    ax.bar([i - w / 2 for i in x], top_mean, width=w, label="Top 8 Traders", color="#27AE60")
    ax.bar([i + w / 2 for i in x], bottom_mean, width=w, label="Bottom 8 Traders", color="#C0392B")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(list(x))
    ax.set_xticklabels(SENTIMENT_ORDER, rotation=20)
    ax.set_ylabel("Avg Closed PnL per Trade (USD)")
    ax.set_title("Top vs Bottom Traders: PnL by Market Sentiment", fontweight="bold")
    ax.legend()
    plt.tight_layout()
    _save(fig, "03_top_vs_bottom_pnl.png")


def plot_buysell_bias(merged):
    _, top_df, bottom_df = top_bottom_accounts(merged)
    top_side = buy_sell_bias(top_df)
    bottom_side = buy_sell_bias(bottom_df)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].bar(SENTIMENT_ORDER, top_side["BUY"], label="Buy %", color="#2ECC71")
    axes[0].bar(SENTIMENT_ORDER, top_side["SELL"], bottom=top_side["BUY"], label="Sell %", color="#E74C3C")
    axes[0].set_title("Top Traders: Buy/Sell Mix", fontweight="bold")
    axes[0].tick_params(axis="x", rotation=25)
    axes[0].legend()
    axes[0].set_ylabel("% of Trades")

    axes[1].bar(SENTIMENT_ORDER, bottom_side["BUY"], label="Buy %", color="#2ECC71")
    axes[1].bar(SENTIMENT_ORDER, bottom_side["SELL"], bottom=bottom_side["BUY"], label="Sell %", color="#E74C3C")
    axes[1].set_title("Bottom Traders: Buy/Sell Mix", fontweight="bold")
    axes[1].tick_params(axis="x", rotation=25)
    axes[1].legend()
    plt.tight_layout()
    _save(fig, "04_buysell_bias.png")


def plot_timeline(merged, sentiment):
    daily = daily_sentiment_vs_pnl(merged, sentiment)
    fig, ax1 = plt.subplots(figsize=(13, 5.5))
    ax2 = ax1.twinx()
    ax1.plot(daily["date"], daily["value"], color="#8E44AD", alpha=0.6, linewidth=1, label="Fear/Greed Index")
    ax2.plot(daily["date"], daily["pnl_7d"], color="#2980B9", linewidth=1.5, label="7d Avg Daily PnL")
    ax2.axhline(0, color="gray", linewidth=0.7, linestyle="--")
    ax1.set_ylabel("Fear & Greed Index Value", color="#8E44AD")
    ax2.set_ylabel("7-Day Avg Daily Closed PnL (USD)", color="#2980B9")
    ax1.set_title("Market Sentiment vs Trader Aggregate PnL Over Time", fontweight="bold")
    fig.legend(loc="upper left", bbox_to_anchor=(0.08, 0.88))
    plt.tight_layout()
    _save(fig, "05_timeline.png")


def plot_top_coins(merged):
    coins = top_coins(merged, 8)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(coins.index[::-1], coins.values[::-1] / 1e6, color="#34495E")
    ax.set_xlabel("Total Volume (USD Millions)")
    ax.set_title("Top 8 Traded Coins by Volume", fontweight="bold")
    plt.tight_layout()
    _save(fig, "06_top_coins.png")


# ---------------------------------------------------------------------
# New charts
# ---------------------------------------------------------------------

def plot_pnl_distribution(merged):
    """Boxplot of closing-trade PnL by sentiment, clipped for readability."""
    closes = merged[merged["Closed PnL"] != 0].copy()
    lo, hi = closes["Closed PnL"].quantile([0.02, 0.98])
    closes["clipped_pnl"] = closes["Closed PnL"].clip(lo, hi)

    fig, ax = plt.subplots(figsize=(11, 5.5))
    data = [closes.loc[closes["classification"] == c, "clipped_pnl"] for c in SENTIMENT_ORDER]
    bp = ax.boxplot(data, patch_artist=True, showfliers=False, widths=0.55)
    ax.set_xticks(range(1, len(SENTIMENT_ORDER) + 1))
    ax.set_xticklabels(SENTIMENT_ORDER)
    for patch, color in zip(bp["boxes"], SENTIMENT_COLORS):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("Closed PnL per Trade (USD, clipped to 2nd-98th pct)")
    ax.set_title("Distribution of Closed PnL by Market Sentiment", fontweight="bold")
    ax.tick_params(axis="x", rotation=20)
    plt.tight_layout()
    _save(fig, "07_pnl_distribution.png")


def plot_trade_size_distribution(merged):
    """Boxplot of trade size (USD) by sentiment."""
    df = merged.copy()
    lo, hi = df["Size USD"].quantile([0.02, 0.98])
    df["clipped_size"] = df["Size USD"].clip(lo, hi)

    fig, ax = plt.subplots(figsize=(11, 5.5))
    data = [df.loc[df["classification"] == c, "clipped_size"] for c in SENTIMENT_ORDER]
    bp = ax.boxplot(data, patch_artist=True, showfliers=False, widths=0.55)
    ax.set_xticks(range(1, len(SENTIMENT_ORDER) + 1))
    ax.set_xticklabels(SENTIMENT_ORDER)
    for patch, color in zip(bp["boxes"], SENTIMENT_COLORS):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax.set_ylabel("Trade Size (USD, clipped to 2nd-98th pct)")
    ax.set_title("Distribution of Trade Size by Market Sentiment", fontweight="bold")
    ax.tick_params(axis="x", rotation=20)
    plt.tight_layout()
    _save(fig, "08_trade_size_distribution.png")


def plot_cumulative_pnl(merged, sentiment):
    """Cumulative aggregate PnL over time, shaded by dominant sentiment class."""
    daily = daily_sentiment_vs_pnl(merged, sentiment)
    daily = daily.merge(
        sentiment.assign(date=pd.to_datetime(sentiment["date"]))[["date", "classification"]],
        on="date", how="left"
    )
    color_map = dict(zip(SENTIMENT_ORDER, SENTIMENT_COLORS))

    fig, ax = plt.subplots(figsize=(13, 5.5))
    ax.plot(daily["date"], daily["cum_pnl"], color="#1B2631", linewidth=1.6, zorder=3)

    # Shade background by sentiment class in contiguous runs
    daily = daily.reset_index(drop=True)
    start_idx = 0
    for i in range(1, len(daily) + 1):
        if i == len(daily) or daily.loc[i, "classification"] != daily.loc[start_idx, "classification"]:
            cls = daily.loc[start_idx, "classification"]
            ax.axvspan(daily.loc[start_idx, "date"], daily.loc[i - 1, "date"],
                       color=color_map.get(cls, "#FFFFFF"), alpha=0.15, zorder=1)
            start_idx = i

    ax.set_ylabel("Cumulative Closed PnL (USD)")
    ax.set_title("Cumulative Trader PnL Over Time, Shaded by Sentiment Regime", fontweight="bold")
    ax.axhline(0, color="gray", linewidth=0.7, linestyle="--")
    plt.tight_layout()
    _save(fig, "09_cumulative_pnl.png")


def plot_account_scatter(merged):
    """Scatter of total volume vs total PnL per account, sized/colored by win rate."""
    stats = account_level_stats(merged)
    fig, ax = plt.subplots(figsize=(10, 6))
    sc = ax.scatter(
        stats["total_volume"] / 1e6, stats["total_pnl"] / 1e3,
        s=stats["n_trades"] / stats["n_trades"].max() * 400 + 30,
        c=stats["win_rate"] * 100, cmap="RdYlGn", edgecolor="black", linewidth=0.4, alpha=0.85
    )
    ax.axhline(0, color="gray", linewidth=0.7, linestyle="--")
    ax.set_xlabel("Total Trading Volume (USD Millions)")
    ax.set_ylabel("Total Closed PnL (USD Thousands)")
    ax.set_title("Account-Level Volume vs. Total PnL\n(bubble size = trade count, color = win rate)", fontweight="bold")
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("Win Rate (%)")
    plt.tight_layout()
    _save(fig, "10_account_scatter.png")


def plot_coin_sentiment_heatmap(merged):
    """Heatmap of average PnL per trade for top coins across sentiment regimes."""
    coins = top_coins(merged, 6).index.tolist()
    pivot = pnl_by_sentiment_and_coin(merged, coins)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    im = ax.imshow(pivot.values, cmap="RdYlGn", aspect="auto",
                    vmin=-np.nanmax(np.abs(pivot.values)), vmax=np.nanmax(np.abs(pivot.values)))
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            val = pivot.values[i, j]
            if not np.isnan(val):
                ax.text(j, i, f"{val:.0f}", ha="center", va="center", fontsize=8.5,
                        color="black")
    ax.set_title("Avg Closed PnL per Trade: Top Coins x Sentiment Regime", fontweight="bold")
    plt.colorbar(im, ax=ax, label="Avg Closed PnL (USD)")
    plt.tight_layout()
    _save(fig, "11_coin_sentiment_heatmap.png")


def plot_extreme_regime_pnl_hist(merged):
    """Overlaid histogram comparing PnL distributions in Extreme Fear vs Extreme Greed."""
    closes = merged[merged["Closed PnL"] != 0]
    ef = closes.loc[closes["classification"] == "Extreme Fear", "Closed PnL"]
    eg = closes.loc[closes["classification"] == "Extreme Greed", "Closed PnL"]
    lo, hi = closes["Closed PnL"].quantile([0.02, 0.98])
    ef_c = ef.clip(lo, hi)
    eg_c = eg.clip(lo, hi)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    bins = np.linspace(lo, hi, 50)
    ax.hist(ef_c, bins=bins, alpha=0.6, label="Extreme Fear", color=SENTIMENT_COLORS[0], density=True)
    ax.hist(eg_c, bins=bins, alpha=0.6, label="Extreme Greed", color=SENTIMENT_COLORS[-1], density=True)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Closed PnL per Trade (USD, clipped to 2nd-98th pct)")
    ax.set_ylabel("Density")
    ax.set_title("PnL Distribution: Extreme Fear vs. Extreme Greed", fontweight="bold")
    ax.legend()
    plt.tight_layout()
    _save(fig, "12_extreme_regime_hist.png")


def generate_all(merged, sentiment):
    plot_pnl_winrate(merged)
    plot_activity(merged)
    plot_top_vs_bottom_pnl(merged)
    plot_buysell_bias(merged)
    plot_timeline(merged, sentiment)
    plot_top_coins(merged)
    plot_pnl_distribution(merged)
    plot_trade_size_distribution(merged)
    plot_cumulative_pnl(merged, sentiment)
    plot_account_scatter(merged)
    plot_coin_sentiment_heatmap(merged)
    plot_extreme_regime_pnl_hist(merged)


if __name__ == "__main__":
    from data_loader import load_merged
    merged, sentiment, trades = load_merged()
    generate_all(merged, sentiment)