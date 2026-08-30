# src/crypto300/data.py
"""Market-data normalization and validation helpers."""

from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = ("open", "high", "low", "close", "volume")


def normalize_ohlcv(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a validated daily OHLCV frame with a UTC DatetimeIndex.

    The caller is responsible for supplying data from a trustworthy source.
    Duplicate timestamps are rejected instead of silently choosing a row.
    """
    if not isinstance(frame.index, pd.DatetimeIndex):
        raise TypeError("OHLCV data must use a DatetimeIndex")
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing OHLCV columns: {missing}")
    if frame.empty:
        raise ValueError("OHLCV data cannot be empty")

    result = frame.loc[:, REQUIRED_COLUMNS].copy()
    result.index = pd.to_datetime(result.index, utc=True)
    if result.index.has_duplicates:
        raise ValueError("Duplicate timestamps are not allowed")
    result = result.sort_index()
    if not result.index.is_monotonic_increasing:
        raise ValueError("Timestamps must be increasing")
    if result[REQUIRED_COLUMNS].isna().any().any():
        raise ValueError("OHLCV data contains missing values")
    if (result[["open", "high", "low", "close", "volume"]] < 0).any().any():
        raise ValueError("OHLCV values cannot be negative")
    if (result["high"] < result[["open", "close"]].max(axis=1)).any():
        raise ValueError("High is below open/close")
    if (result["low"] > result[["open", "close"]].min(axis=1)).any():
        raise ValueError("Low is above open/close")
    return result.astype(float)


def close_matrix(markets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Normalize multiple markets and return an aligned close-price matrix."""
    normalized = {symbol: normalize_ohlcv(frame)["close"] for symbol, frame in markets.items()}
    result = pd.concat(normalized, axis=1).dropna(how="any")
    if result.empty:
        raise ValueError("No common timestamps across supplied markets")
    return result
