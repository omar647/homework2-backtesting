# 📊 Technical Indicators & Strategy Backtesting (Alpaca)

**Homework 2** — Build a backtesting platform on Alpaca historical data and
compare algorithmic trading strategies on a **risk-adjusted** basis.

## What it does

- Pulls **5+ years of daily OHLCV** for any ticker from Alpaca.
- Computes **11 technical indicators** across all four categories.
- Runs **3 strategies** + a Buy & Hold benchmark through a reusable, long-only
  backtesting engine (\$100k, no leverage, no shorting).
- Reports **Total Return, CAGR, Volatility, Sharpe, Sortino, Max Drawdown, Win Rate**.
- Produces **price-signal, equity-curve, and drawdown** charts.

## Project structure

```
homework2-backtesting/
├── run_backtest.py          # CLI: run all strategies + save charts for a ticker
├── backtest_report.ipynb    # final report notebook (charts + discussion)
├── requirements.txt
├── .env.example             # copy to .env, add Alpaca paper keys
├── .gitignore
├── charts/                  # generated PNG charts + metrics.csv
├── report/report.md         # written final report (export to PDF)
└── src/
    ├── config.py            # load API keys from environment
    ├── data.py              # Alpaca daily OHLCV download
    ├── indicators.py        # 11 indicators (SMA, EMA, MACD, ADX, RSI, …)
    ├── strategies.py        # Trend Following, Mean Reversion, Custom
    ├── backtest.py          # long-only backtesting engine
    ├── metrics.py           # performance metrics + comparison table
    └── plotting.py          # price/equity/drawdown charts
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env          # add your Alpaca PAPER keys
```

## Run

**CLI** (downloads data, prints the metrics table, saves charts to `charts/`):
```bash
python run_backtest.py --ticker AAPL --years 5
python run_backtest.py --ticker QQQ
```

**Notebook** (the final report, with charts inline):
```bash
jupyter notebook backtest_report.ipynb
```

## Indicators

| Category | Indicators |
|---|---|
| Trend | SMA, EMA, MACD, ADX |
| Momentum | RSI, Stochastic Oscillator, Williams %R |
| Volatility | Bollinger Bands, ATR |
| Volume | OBV, Chaikin Money Flow (CMF) |

## Strategies

| # | Name | Category mix | Entry | Exit |
|---|---|---|---|---|
| 1 | Trend Following | Trend | MACD > signal **and** ADX > 25 | MACD < signal |
| 2 | Mean Reversion | Momentum + Volatility | RSI < 30 **and** price < lower band | RSI > 70 **and** price > upper band |
| 3 | Custom | Trend + Momentum + Volume | EMA50 > EMA200 **and** RSI > 50 **and** CMF > 0 | EMA50 < EMA200 **or** RSI < 45 |

## Backtesting assumptions

Initial capital \$100,000 · long-only · no leverage · no shorting · signals act
on the next bar (no look-ahead) · gross of fees/slippage/taxes.

## Demo video

A walkthrough of the code, the strategies, the performance table, and the charts.

[![Watch the demo](https://img.youtube.com/vi/ucJv0GhX1Mc/hqdefault.jpg)](https://youtu.be/ucJv0GhX1Mc)

## Deliverables checklist

- [x] Alpaca data retrieval · [x] 6+ indicators (11) · [x] Strategy 1/2/3
- [x] Backtesting engine · [x] Performance metrics · [x] Visualizations
- [x] Final report (`report/report.md` + notebook) · [ ] Demo video (add link)

## Tech stack

`alpaca-py` · `pandas` · `numpy` · `matplotlib` · `python-dotenv`
