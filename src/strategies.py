"""Three long-only trading strategies.

Each returns a target-position Series (1 = long / in market, 0 = flat),
computed from indicator columns produced by ``indicators.add_indicators``.
"""

from __future__ import annotations

import pandas as pd


def _position_from_signals(entry: pd.Series, exit_: pd.Series) -> pd.Series:
    """Build a 0/1 position that turns on at ``entry`` and off at ``exit_``.

    Holds the position between an entry and the next exit (forward-filled).
    """
    raw = pd.Series(index=entry.index, dtype="float64")
    raw[entry] = 1.0
    raw[exit_] = 0.0
    return raw.ffill().fillna(0.0)


def trend_following(df: pd.DataFrame) -> pd.Series:
    """Strategy 1 — Trend Following (MACD + ADX).

    Buy when MACD > signal AND ADX > 25; sell when MACD < signal.
    """
    entry = (df["macd"] > df["macd_signal"]) & (df["adx"] > 25)
    exit_ = df["macd"] < df["macd_signal"]
    return _position_from_signals(entry, exit_)


def mean_reversion(df: pd.DataFrame) -> pd.Series:
    """Strategy 2 — Mean Reversion (RSI + Bollinger Bands).

    Buy when RSI < 30 AND price below lower band;
    sell when RSI > 70 AND price above upper band.
    """
    entry = (df["rsi"] < 30) & (df["close"] < df["bb_lower"])
    exit_ = (df["rsi"] > 70) & (df["close"] > df["bb_upper"])
    return _position_from_signals(entry, exit_)


def custom(df: pd.DataFrame) -> pd.Series:
    """Strategy 3 — Custom (Trend + Momentum + Volume).

    Combines three indicators from three categories:
      * Trend    : EMA50 > EMA200 (uptrend regime)
      * Momentum : RSI > 50 (positive momentum)
      * Volume   : CMF > 0 (buying pressure / accumulation)

    Buy when all three hold; exit when the trend breaks (EMA50 < EMA200)
    or momentum fades (RSI < 45).
    """
    entry = (df["ema50"] > df["ema200"]) & (df["rsi"] > 50) & (df["cmf"] > 0)
    exit_ = (df["ema50"] < df["ema200"]) | (df["rsi"] < 45)
    return _position_from_signals(entry, exit_)


def buy_and_hold(df: pd.DataFrame) -> pd.Series:
    """Benchmark — always in the market."""
    return pd.Series(1.0, index=df.index)


STRATEGIES = {
    "Buy & Hold": buy_and_hold,
    "Trend Following": trend_following,
    "Mean Reversion": mean_reversion,
    "Custom Strategy": custom,
}
