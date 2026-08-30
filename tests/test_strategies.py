# tests/test_strategies.py
import pandas as pd
import pytest

from crypto300.strategies import buy_and_hold, periodic_rebalance, trend_following


@pytest.fixture
def close():
    index = pd.date_range("2025-01-01", periods=6, freq="D", tz="UTC")
    return pd.DataFrame({"BTC": [100, 101, 102, 103, 104, 105], "ETH": [100, 99, 101, 98, 103, 100]}, index=index)


def test_buy_and_hold(close):
    result = buy_and_hold(close, {"BTC": 0.7, "ETH": 0.2})
    assert (result["BTC"] == 0.7).all()
    assert (result["ETH"] == 0.2).all()


def test_periodic_rebalance_forward_fills(close):
    result = periodic_rebalance(close, {"BTC": 0.6}, frequency_days=3)
    assert (result.iloc[:3]["BTC"] == 0.6).all()
    assert (result.iloc[3:]["BTC"] == 0.6).all()


def test_trend_following_stays_cash_before_sma(close):
    result = trend_following(close, {"BTC": 0.8}, lookback_days=3)
    assert result.iloc[0]["BTC"] == 0.0
    assert result.iloc[1]["BTC"] == 0.0


def test_weights_cannot_exceed_one(close):
    with pytest.raises(ValueError):
        buy_and_hold(close, {"BTC": 0.8, "ETH": 0.3})
