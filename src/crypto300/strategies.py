# src/crypto300/strategies.py
"""Simple, explicit portfolio-weight strategies for research."""

from __future__ import annotations

import pandas as pd


def buy_and_hold(close: pd.DataFrame, weights: dict[str, float]) -> pd.DataFrame:
    """Return fixed target weights after the initial allocation."""
    _validate_weights(close, weights)
    result = pd.DataFrame(0.0, index=close.index, columns=close.columns)
    result.loc[:, list(weights)] = pd.Series(weights)
    return result


def periodic_rebalance(
    close: pd.DataFrame,
    weights: dict[str, float],
    frequency_days: int = 30,
) -> pd.DataFrame:
    """Return target weights on scheduled rebalance dates, forward-filled."""
    _validate_weights(close, weights)
    if frequency_days < 1:
        raise ValueError("frequency_days must be positive")
    result = pd.DataFrame(0.0, index=close.index, columns=close.columns)
    target = pd.Series(weights, dtype=float)
    for position in range(0, len(close), frequency_days):
        result.iloc[position:, result.columns.get_indexer(target.index)] = target.values
    return result


def trend_following(
    close: pd.DataFrame,
    risky_weights: dict[str, float],
    lookback_days: int = 100,
) -> pd.DataFrame:
    """Hold risky assets only when each asset is above its simple moving average.

    Unallocated capital remains cash. Signals are generated from close prices;
    the backtester executes them on the following observation.
    """
    _validate_weights(close, risky_weights)
    if lookback_days < 2:
        raise ValueError("lookback_days must be at least 2")
    sma = close.rolling(lookback_days, min_periods=lookback_days).mean()
    signals = close > sma
    return signals.mul(pd.Series(risky_weights), axis=1).fillna(0.0)


def _validate_weights(close: pd.DataFrame, weights: dict[str, float]) -> None:
    if not weights:
        raise ValueError("At least one asset weight is required")
    unknown = set(weights) - set(close.columns)
    if unknown:
        raise ValueError(f"Unknown assets: {sorted(unknown)}")
    if any(weight < 0 for weight in weights.values()):
        raise ValueError("Weights cannot be negative")
    if sum(weights.values()) > 1.0 + 1e-12:
        raise ValueError("Weights cannot exceed 100%")
