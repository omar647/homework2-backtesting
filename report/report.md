# Final Report — Technical Indicators & Strategy Backtesting

**Ticker analyzed:** AAPL  ·  **Period:** ~5 years of daily bars (2021-06 → 2026-07)
**Initial capital:** $100,000  ·  **Constraints:** long-only, no leverage, no shorting

> Charts referenced below are in `../charts/` (equity, drawdown, and per-strategy
> price/signal plots) and are also embedded in `../backtest_report.ipynb`.
> To produce a PDF, open the notebook and *File → Save and Export As → PDF* (or
> print this Markdown to PDF).

---

## 1. Strategy Descriptions & Rules

### Buy & Hold (benchmark)
Fully invested for the entire period. Establishes the return and drawdown any
active strategy must beat on a risk-adjusted basis.

### Strategy 1 — Trend Following (Trend category)
Follows established trends using MACD for direction and ADX for trend strength.
- **Entry:** `MACD > MACD signal` **and** `ADX > 25`
- **Exit:** `MACD < MACD signal`

### Strategy 2 — Mean Reversion (Momentum + Volatility)
Buys oversold dips and sells overbought spikes.
- **Entry:** `RSI < 30` **and** `Close < lower Bollinger Band`
- **Exit:** `RSI > 70` **and** `Close > upper Bollinger Band`

### Strategy 3 — Custom (Trend + Momentum + Volume)
Stays long only in a confirmed uptrend with positive momentum and buying pressure
— three indicators from three different categories.
- **Entry:** `EMA50 > EMA200` **and** `RSI > 50` **and** `CMF > 0`
- **Exit:** `EMA50 < EMA200` **or** `RSI < 45`

---

## 2. Performance Comparison (AAPL, 5y)

| Strategy | Total Return | CAGR | Volatility | Sharpe | Sortino | Max Drawdown | Win Rate | Trades |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Buy & Hold | 118.44% | 16.94% | 27.56% | 0.71 | 1.02 | −33.32% | 100.00% | 1 |
| Trend Following | 10.83% | 2.08% | 14.08% | 0.22 | 0.18 | −25.01% | 45.95% | 37 |
| Mean Reversion | 64.70% | 10.51% | 18.85% | 0.62 | 0.58 | −22.79% | 100.00% | 5 |
| Custom Strategy | 27.38% | 4.97% | 15.26% | 0.39 | 0.39 | −21.49% | 33.33% | 24 |

*(Figures regenerate whenever the backtest is re-run; they are gross of fees,
slippage, and taxes.)*

---

## 3. Discussion of Results

**Which strategy performs best on a risk-adjusted basis?**

On AAPL over this window, **Buy & Hold has the highest Sharpe (0.71) and Sortino
(1.02)** — but it also carries the **deepest drawdown (−33%)** and is exposed to
the market 100% of the time. Among the *active* strategies, **Mean Reversion is
the standout**: it captures 65% total return with a Sharpe of 0.62 — close to
Buy & Hold — while cutting the worst drawdown to −22.8% and spending most of the
period in cash (only 5 trades). That is a materially better risk profile for
nearly the same risk-adjusted efficiency.

**Trend Following underperforms here.** MACD/ADX crossovers trade often (37
trades) and get repeatedly whipsawed in AAPL's choppy-but-upward tape, so it
sacrifices most of the upside (10.8% total) for only a modest drawdown benefit —
the classic cost of a lagging trend system in a market that mean-reverts around
its trend.

**The Custom strategy behaves as designed** — the EMA-regime + RSI + CMF filter
keeps it out during weak/accumulation-poor phases, giving it the **shallowest
drawdown of all (−21.5%)**, at the cost of return (27%). It is the most
*defensive* strategy.

**Takeaway.** In a strongly trending single name like AAPL, it is hard to beat
Buy & Hold on raw Sharpe, but active strategies add value by **reducing drawdown**.
For an investor who cares about downside, **Mean Reversion offers the best
return-per-unit-of-drawdown**, and **Custom offers the smoothest ride**. Results
are ticker- and regime-dependent: re-running on `QQQ`, `NVDA`, or `SPY` (change
`TICKER` in the notebook or `--ticker` on the CLI) shows how the ranking shifts
in more or less trending markets.
