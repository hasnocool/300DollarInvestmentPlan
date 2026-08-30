# tests/test_data.py
import pandas as pd
import pytest

from crypto300.data import normalize_ohlcv


def _frame():
    index = pd.date_range("2025-01-01", periods=2, freq="D")
    return pd.DataFrame(
        {
            "open": [100, 101],
            "high": [102, 103],
            "low": [99, 100],
            "close": [101, 102],
            "volume": [1000, 1100],
        },
        index=index,
    )


def test_normalize_ohlcv_sorts_and_converts_timezone():
    result = normalize_ohlcv(_frame().iloc[::-1])
    assert result.index.is_monotonic_increasing
    assert str(result.index.tz) == "UTC"


def test_normalize_ohlcv_rejects_missing_columns():
    frame = _frame().drop(columns="volume")
    with pytest.raises(ValueError, match="Missing OHLCV"):
        normalize_ohlcv(frame)


def test_normalize_ohlcv_rejects_invalid_candle():
    frame = _frame()
    frame.loc[frame.index[0], "high"] = 90
    with pytest.raises(ValueError, match="High"):
        normalize_ohlcv(frame)
