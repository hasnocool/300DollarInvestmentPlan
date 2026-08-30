# tests/test_scenarios.py
import numpy as np
import pytest

from crypto300.scenarios import bootstrap_paths, terminal_percentiles


def test_bootstrap_is_deterministic_with_seed():
    returns = np.array([0.01, -0.02, 0.03, 0.0])
    first = bootstrap_paths(300.0, returns, periods=10, simulations=100, seed=7)
    second = bootstrap_paths(300.0, returns, periods=10, simulations=100, seed=7)
    assert np.array_equal(first, second)
    assert first.shape == (100, 11)
    assert (first[:, 0] == 300.0).all()


def test_terminal_percentiles():
    paths = np.array([[100.0, 110.0], [100.0, 120.0], [100.0, 130.0]])
    result = terminal_percentiles(paths, percentiles=(0, 50, 100))
    assert result == {0: 110.0, 50: 120.0, 100: 130.0}


def test_returns_below_minus_one_rejected():
    with pytest.raises(ValueError):
        bootstrap_paths(300.0, np.array([0.01, -1.0]), periods=5)
