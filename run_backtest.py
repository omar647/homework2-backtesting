"""Run the full backtest for a chosen ticker and produce metrics + charts.

Usage:
    python run_backtest.py --ticker AAPL --years 5
    python run_backtest.py --ticker QQQ
"""

from __future__ import annotations

import argparse
import os

import matplotlib
matplotlib.use("Agg")  # headless: save charts without a display

from src.backtest import run_backtest
from src.data import get_daily_ohlcv
from src.indicators import add_indicators
from src.metrics import metrics_table
from src.plotting import plot_drawdowns, plot_equity_curves, plot_price_signals
from src.strategies import STRATEGIES

CHARTS_DIR = os.path.join(os.path.dirname(__file__), "charts")


def main() -> None:
    ap = argparse.ArgumentParser(description="Technical-indicator strategy backtester")
    ap.add_argument("--ticker", default="AAPL", help="Ticker symbol (e.g. AAPL, MSFT, SPY, QQQ, NVDA)")
    ap.add_argument("--years", type=int, default=5, help="Years of history (>=5)")
    ap.add_argument("--capital", type=float, default=100_000, help="Initial capital")
    args = ap.parse_args()

    ticker = args.ticker.upper()
    os.makedirs(CHARTS_DIR, exist_ok=True)

    print(f"Downloading {args.years}y of daily data for {ticker}…")
    df = get_daily_ohlcv(ticker, years=args.years)
    df = add_indicators(df)
    print(f"  {len(df)} bars from {df.index[0].date()} to {df.index[-1].date()}")

    # Run every strategy.
    results = {}
    for name, strat in STRATEGIES.items():
        signal = strat(df)
        results[name] = run_backtest(df, signal, initial_capital=args.capital)

    # Metrics table.
    table = metrics_table(results)
    print("\n=== Performance Comparison ===")
    print(table.to_string())

    # Charts.
    plot_equity_curves(results, save=os.path.join(CHARTS_DIR, f"{ticker}_equity.png"))
    plot_drawdowns(results, save=os.path.join(CHARTS_DIR, f"{ticker}_drawdown.png"))
    for name in ("Trend Following", "Mean Reversion", "Custom Strategy"):
        fname = name.lower().replace(" ", "_")
        plot_price_signals(df, results[name], f"{ticker} — {name}",
                           save=os.path.join(CHARTS_DIR, f"{ticker}_{fname}.png"))
    print(f"\nCharts saved to {CHARTS_DIR}/")

    # Save the metrics table for the report.
    table.to_csv(os.path.join(CHARTS_DIR, f"{ticker}_metrics.csv"))
    print("Done.")


if __name__ == "__main__":
    main()
