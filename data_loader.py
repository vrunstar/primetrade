"""
data_loader.py
Loads the Bitcoin Fear & Greed sentiment dataset and the Hyperliquid historical
trade dataset, cleans timestamps, and merges them on calendar date.
"""

import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SENTIMENT_ORDER = ["Extreme Fear", "Fear", "Neutral", "Greed", "Extreme Greed"]
SENTIMENT_COLORS = ["#8B0000", "#E74C3C", "#95A5A6", "#27AE60", "#145A32"]


def load_sentiment(path=None):
    """Load the Fear & Greed Index CSV and parse the date column."""
    path = path or os.path.join(DATA_DIR, "fear_greed_index.csv")
    sentiment = pd.read_csv(path)
    sentiment["date"] = pd.to_datetime(sentiment["date"]).dt.date
    return sentiment


def load_trades(path=None):
    """Load the Hyperliquid historical trade CSV and parse timestamps."""
    path = path or os.path.join(DATA_DIR, "historical_data.csv")
    trades = pd.read_csv(path)
    trades["Timestamp IST"] = pd.to_datetime(
        trades["Timestamp IST"], format="%d-%m-%Y %H:%M", errors="coerce"
    )
    trades["date"] = trades["Timestamp IST"].dt.date
    return trades


def load_merged(sentiment_path=None, trades_path=None, verbose=True):
    """Load both datasets and merge trades with the daily sentiment label."""
    sentiment = load_sentiment(sentiment_path)
    trades = load_trades(trades_path)

    merged = trades.merge(sentiment[["date", "classification"]], on="date", how="left")
    unmatched = merged["classification"].isna().sum()
    merged = merged.dropna(subset=["classification"])

    if verbose:
        print(f"Sentiment rows: {len(sentiment):,} | range: {sentiment['date'].min()} to {sentiment['date'].max()}")
        print(f"Trade rows: {len(trades):,} | range: {trades['date'].min()} to {trades['date'].max()}")
        print(f"Unique accounts: {trades['Account'].nunique()} | Unique coins: {trades['Coin'].nunique()}")
        print(f"Unmatched rows dropped after merge: {unmatched} ({unmatched / len(trades) * 100:.3f}%)")

    return merged, sentiment, trades


if __name__ == "__main__":
    merged, sentiment, trades = load_merged()
    print("\nMerged shape:", merged.shape)
    print(merged["classification"].value_counts().reindex(SENTIMENT_ORDER))
