"""
metrics.py
Computes summary tables used across the analysis: PnL/win-rate by sentiment,
activity normalized by calendar days, top/bottom trader segmentation, buy/sell
bias, fee impact, coin concentration, and daily aggregate PnL vs sentiment value.
"""

import pandas as pd
from data_loader import SENTIMENT_ORDER


def pnl_winrate_by_sentiment(merged):
    summary = merged.groupby("classification")["Closed PnL"].agg(
        trades="count", mean_pnl="mean", median_pnl="median", total_pnl="sum"
    ).reindex(SENTIMENT_ORDER)

    closing_trades = merged[merged["Closed PnL"] != 0]
    win_rate = closing_trades.groupby("classification").apply(
        lambda x: (x["Closed PnL"] > 0).mean()
    ).reindex(SENTIMENT_ORDER)

    summary["win_rate"] = win_rate
    return summary, closing_trades


def activity_by_sentiment(merged):
    days_per_class = merged.groupby("classification")["date"].nunique().reindex(SENTIMENT_ORDER)
    activity = merged.groupby("classification").agg(
        trades=("Trade ID", "count"), volume_usd=("Size USD", "sum")
    ).reindex(SENTIMENT_ORDER)
    activity["calendar_days"] = days_per_class
    activity["trades_per_day"] = activity["trades"] / days_per_class
    activity["volume_per_day_musd"] = activity["volume_usd"] / days_per_class / 1e6
    return activity


def top_bottom_accounts(merged, n=8):
    acct_pnl = merged.groupby("Account")["Closed PnL"].sum().sort_values(ascending=False)
    top_accounts = acct_pnl.head(n).index
    bottom_accounts = acct_pnl.tail(n).index
    top_df = merged[merged["Account"].isin(top_accounts)]
    bottom_df = merged[merged["Account"].isin(bottom_accounts)]
    return acct_pnl, top_df, bottom_df


def buy_sell_bias(df):
    return (pd.crosstab(df["classification"], df["Side"], normalize="index") * 100).reindex(SENTIMENT_ORDER)


def fee_impact(merged):
    fees = merged.groupby("classification").agg(
        total_fee=("Fee", "sum"), avg_fee=("Fee", "mean"), total_pnl=("Closed PnL", "sum")
    ).reindex(SENTIMENT_ORDER)
    fees["fee_as_pct_of_pnl"] = (fees["total_fee"] / fees["total_pnl"] * 100).round(2)
    return fees


def top_coins(merged, n=8):
    return merged.groupby("Coin")["Size USD"].sum().sort_values(ascending=False).head(n)


def daily_sentiment_vs_pnl(merged, sentiment):
    daily = merged.groupby("date")["Closed PnL"].sum().reset_index()
    daily = daily.merge(sentiment[["date", "value"]], on="date", how="left").sort_values("date")
    daily["date"] = pd.to_datetime(daily["date"])
    daily["pnl_7d"] = daily["Closed PnL"].rolling(7, min_periods=1).mean()
    daily["cum_pnl"] = daily["Closed PnL"].cumsum()
    return daily


def account_level_stats(merged):
    """Per-account aggregate stats for scatter/bubble analysis."""
    closes = merged[merged["Closed PnL"] != 0]
    stats = merged.groupby("Account").agg(
        total_volume=("Size USD", "sum"),
        total_pnl=("Closed PnL", "sum"),
        n_trades=("Trade ID", "count"),
    )
    win_rate = closes.groupby("Account").apply(lambda x: (x["Closed PnL"] > 0).mean())
    stats["win_rate"] = win_rate
    return stats.dropna()


def pnl_by_sentiment_and_coin(merged, coins):
    subset = merged[merged["Coin"].isin(coins)]
    pivot = subset.groupby(["classification", "Coin"])["Closed PnL"].mean().unstack()
    return pivot.reindex(SENTIMENT_ORDER)[coins]


if __name__ == "__main__":
    from data_loader import load_merged
    merged, sentiment, trades = load_merged()
    summary, closes = pnl_winrate_by_sentiment(merged)
    print(summary)
