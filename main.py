"""
main.py
Orchestrates the full pipeline: load data -> compute metrics -> print summary
tables -> generate all charts. Run this as the entry point:

    python main.py
"""

import pandas as pd

from data_loader import load_merged, SENTIMENT_ORDER
from metrics import (
    pnl_winrate_by_sentiment, activity_by_sentiment, top_bottom_accounts,
    buy_sell_bias, fee_impact, top_coins, daily_sentiment_vs_pnl,
)
from plots import generate_all
from report_builder import build_report

pd.set_option("display.width", 140)


def main():
    print("=" * 70)
    print("Loading and merging datasets")
    print("=" * 70)
    merged, sentiment, trades = load_merged()

    print("\n" + "=" * 70)
    print("PnL & Win Rate by Sentiment")
    print("=" * 70)
    summary, closing_trades = pnl_winrate_by_sentiment(merged)
    print(summary)

    print("\n" + "=" * 70)
    print("Trading Activity by Sentiment (normalized per calendar day)")
    print("=" * 70)
    activity = activity_by_sentiment(merged)
    print(activity)

    print("\n" + "=" * 70)
    print("Top vs Bottom Traders")
    print("=" * 70)
    acct_pnl, top_df, bottom_df = top_bottom_accounts(merged)
    print("Top 5 accounts by total PnL:")
    print(acct_pnl.head())
    print("\nBottom 5 accounts by total PnL:")
    print(acct_pnl.tail())

    print("\nTop traders buy/sell bias by sentiment (%):")
    print(buy_sell_bias(top_df))
    print("\nBottom traders buy/sell bias by sentiment (%):")
    print(buy_sell_bias(bottom_df))

    print("\n" + "=" * 70)
    print("Fee Impact by Sentiment")
    print("=" * 70)
    print(fee_impact(merged))

    print("\n" + "=" * 70)
    print("Top Traded Coins")
    print("=" * 70)
    print(top_coins(merged))

    daily = daily_sentiment_vs_pnl(merged, sentiment)
    corr = daily["Closed PnL"].corr(daily["value"])
    print(f"\nCorrelation (daily sentiment value vs daily aggregate PnL): {corr:.4f}")

    print("\n" + "=" * 70)
    print("Generating charts")
    print("=" * 70)
    generate_all(merged, sentiment)

    print("\n" + "=" * 70)
    print("Building PDF report")
    print("=" * 70)
    build_report()

    print("\nDone. Charts saved to ./charts/ and PDF report written.")


if __name__ == "__main__":
    main()