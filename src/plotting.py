"""Charts: price + indicators + signals, equity curves, and drawdowns."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from .backtest import BacktestResult
from .metrics import drawdown_series


def plot_price_signals(df: pd.DataFrame, result: BacktestResult, title: str, save: str | None = None):
    """Price with SMA/Bollinger and buy/sell markers for one strategy."""
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(df.index, df["close"], label="Close", color="black", linewidth=1)
    ax.plot(df.index, df["sma50"], label="SMA 50", color="#1f77b4", alpha=0.8)
    ax.plot(df.index, df["bb_upper"], color="#999", linestyle="--", alpha=0.5, label="Bollinger")
    ax.plot(df.index, df["bb_lower"], color="#999", linestyle="--", alpha=0.5)

    pos = result.position
    entries = pos[(pos == 1) & (pos.shift(1) == 0)].index
    exits = pos[(pos == 0) & (pos.shift(1) == 1)].index
    ax.scatter(entries, df["close"].reindex(entries), marker="^", color="green", s=90, label="Buy", zorder=5)
    ax.scatter(exits, df["close"].reindex(exits), marker="v", color="red", s=90, label="Sell", zorder=5)

    ax.set_title(title)
    ax.set_ylabel("Price ($)")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    if save:
        fig.savefig(save, dpi=120, bbox_inches="tight")
    return fig


def plot_equity_curves(results: dict[str, BacktestResult], save: str | None = None):
    """Compare equity curves of all strategies (and Buy & Hold)."""
    fig, ax = plt.subplots(figsize=(14, 7))
    for name, res in results.items():
        ax.plot(res.equity.index, res.equity, label=name, linewidth=1.5)
    ax.set_title("Equity Curve — Strategy Comparison")
    ax.set_ylabel("Portfolio value ($)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    if save:
        fig.savefig(save, dpi=120, bbox_inches="tight")
    return fig


def plot_drawdowns(results: dict[str, BacktestResult], save: str | None = None):
    """Compare drawdowns across strategies."""
    fig, ax = plt.subplots(figsize=(14, 7))
    for name, res in results.items():
        dd = drawdown_series(res.equity) * 100
        ax.plot(dd.index, dd, label=name, linewidth=1.2)
    ax.set_title("Drawdown — Strategy Comparison")
    ax.set_ylabel("Drawdown (%)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    if save:
        fig.savefig(save, dpi=120, bbox_inches="tight")
    return fig
