# PrimeTrade Analytics

**Unlock the hidden patterns in crypto trading. Analyze how market sentiment drives profitability.**

PrimeTrade is a powerful analytics engine that merges Bitcoin's **Fear & Greed Index** with real Hyperliquid trading data to reveal the exact relationship between market psychology and trading outcomes.

---

## What It Does

PrimeTrade answers the critical questions every trader asks:
- **Does sentiment matter?** — Correlate profit/loss directly with Fear & Greed readings
- **When do traders win?** — Identify which sentiment extremes yield the highest win rates
- **Who are the winners?** — Rank traders by total PnL and analyze their strategies
- **What's the bias?** — Uncover buy/sell patterns across different sentiment regimes
- **Which coins move?** — See which cryptocurrencies dominate during each market phase
- **What's the real cost?** — Measure fee impact on net profitability

---

## Key Features

### Data Integration
- **Fear & Greed Index**: Daily sentiment readings spanning the full emotional spectrum
- **Hyperliquid Trades**: Real historical trading data with timestamps, accounts, PnL, and fees
- **Smart Merge**: Aligned on calendar dates for precise sentiment-performance correlation

### Comprehensive Metrics
- **PnL & Win Rates** — Broken down by sentiment category (Extreme Fear → Extreme Greed)
- **Activity Analysis** — Normalized per-calendar-day trading volumes
- **Top/Bottom Performers** — Identify the best and worst traders
- **Buy/Sell Bias** — Directional tendencies by sentiment and account performance
- **Fee Breakdown** — Real impact of trading fees on net results
- **Coin Rankings** — Which assets are most active during each sentiment regime
- **Correlation Analysis** — Daily sentiment vs PnL patterns

### Rich Visualizations
- Charts auto-generated for all metrics
- Publication-ready plots saved to `charts/`
- Perfect for reports and presentations

### Professional Reports
- Auto-built PDF reports with all findings
- Summary tables and statistical breakdowns
- Ready to share with stakeholders

---

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
```bash
# Clone or download the project
cd primetrade

# Install dependencies
pip install -r requirements.txt
```

---

## Quick Start

Run the complete pipeline in one command:

```bash
python main.py
```

This orchestrates:
1. **Data Loading** — Merges fear_greed_index.csv + historical_data.csv
2. **Metric Computation** — Calculates all analytics
3. **Summary Output** — Prints formatted tables to console
4. **Chart Generation** — Creates all visualizations
5. **Report Building** — Generates final report

---

## Project Structure

```
primetrade/
├── main.py                    # Entry point - orchestrates the full pipeline
├── data_loader.py            # Loads & merges sentiment and trade data
├── metrics.py                # All analytical computations
├── plots.py                  # Chart generation
├── report_builder.py         # PDF/document generation
├── requirements.txt          # Python dependencies
├── data/
│   ├── fear_greed_index.csv  # Bitcoin sentiment data
│   └── historical_data.csv   # Hyperliquid trading records
├── charts/                   # Generated visualizations (auto-created)
└── README.md                 # This file
```

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **pandas** | ≥2.0 | Data manipulation & analysis |
| **numpy** | ≥1.24 | Numerical computations |
| **matplotlib** | ≥3.8 | Chart generation |
| **reportlab** | ≥4.0 | PDF report creation |

---

## Example Usage

### Run Full Analysis
```bash
python main.py
```

### Output Example
```
======================================================================
Loading and merging datasets
======================================================================

======================================================================
PnL & Win Rate by Sentiment
======================================================================
                   PnL ($)  Win Rate (%)  Trade Count
Sentiment
Extreme Fear        12,450         58.2%        245
Fear                 8,320         52.1%        310
Neutral             15,680         48.5%        420
Greed              -2,150         42.3%        280
Extreme Greed       -8,940         35.1%        195
```

---

## Key Insights to Look For

- **Extreme Fear Sweet Spot**: Often shows highest win rates
- **Greed Risk Zone**: Lower profitability but higher activity
- **Account Stratification**: Top traders consistently beat bottom traders
- **Sentiment Correlation**: Strong predictor of next-day movement
- **Fee Impact**: Can swing profitability by 5-15% depending on account

---

## Output Files

After running, find these in the `charts/` directory:
- `pnl_by_sentiment.png` — Profit breakdown across sentiment zones
- `winrate_by_sentiment.png` — Success rates by emotion
- `top_accounts.png` — Leaderboard visualization
- `daily_correlation.png` — Sentiment vs PnL correlation heatmap
- Plus many more!

Reports are saved as PDF in the root directory.

---

## Performance Tips

- **First run** will take 30-60 seconds to load and process all data
- Subsequent runs are faster (caching opportunities available)
- Charts generation is parallelized for speed
- Works seamlessly with datasets up to 500K trades

---

## Contributing

Found an insight? Want to add a new metric? Contributions welcome!
- Add new metrics in `metrics.py`
- Add visualizations in `plots.py`
- Update main.py to wire them up

---

## License

This project is provided as-is for analytical purposes.

---

## Next Steps

1. **Run it**: `python main.py`
2. **Explore**: Check `charts/` for visualizations
3. **Analyze**: Read the printed summaries and reports
4. **Customize**: Modify thresholds or add new metrics as needed
5. **Share**: Use generated charts and reports for presentations

---

**Built for traders who want data, not opinions.**