# tests/test_backtest.py
import pandas as pd
import pytest

from crypto300.backtest import BacktestConfig, run_backtest


def test_signal_executes_on_next_observation():
    index = pd.date_range("2025-01-01", periods=3, freq="D", tz="UTC")
    close = pd.DataFrame({"BTC": [100.0, 200.0, 200.0]}, index=index)
    targets = pd.DataFrame({"BTC": [0.0, 1.0, 1.0]}, index=index)
    result = run_backtest(close, targets, BacktestConfig(fee_rate=0.0, slippage_rate=0.0))
    assert result.equity.iloc[0] == pytest.approx(300.0)
    assert result.equity.iloc[1] == pytest.approx(300.0)
    assert result.equity.iloc[2] == pytest.approx(300.0)


def test_costs_reduce_equity_when_rebalancing():
    index = pd.date_range("2025-01-01", periods=3, freq="D", tz="UTC")
    close = pd.DataFrame({"BTC": [100.0, 100.0, 100.0]}, index=index)
    targets = pd.DataFrame({"BTC": [1.0, 1.0, 1.0]}, index=index)
    result = run_backtest(close, targets, BacktestConfig(fee_rate=0.01, slippage_rate=0.01))
    assert result.equity.iloc[-1] < 300.0
    assert result.trades == 1
