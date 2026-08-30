# tests/test_metrics.py
import pandas as pd
import pytest

from crypto300.metrics import cagr, max_drawdown, sharpe_like, total_return


def test_total_return():
    equity = pd.Series([100.0, 110.0, 121.0])
    assert total_return(equity) == pytest.approx(0.21)


def test_max_drawdown():
    equity = pd.Series([100.0, 120.0, 90.0, 110.0])
    assert max_drawdown(equity) == pytest.approx(-0.25)


def test_cagr():
    equity = pd.Series([100.0, 110.0])
    assert cagr(equity, periods_per_year=1) == pytest.approx(0.10)


def test_sharpe_zero_for_constant_returns():
    equity = pd.Series([100.0, 101.0, 102.01, 103.0301])
    assert sharpe_like(equity) == pytest.approx(0.0)
