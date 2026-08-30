# src/crypto300/scenarios.py
"""Monte Carlo resampling for uncertainty ranges, not price prediction."""

from __future__ import annotations

import numpy as np


def bootstrap_paths(
    starting_value: float,
    historical_returns: np.ndarray,
    periods: int,
    simulations: int = 10_000,
    seed: int = 42,
) -> np.ndarray:
    """Bootstrap historical returns into simulated equity paths.

    Sampling is with replacement and preserves the empirical distribution but
    not temporal correlations. Results should be interpreted as scenario
    ranges, not probabilities that a particular future price will occur.
    """
    if starting_value <= 0:
        raise ValueError("starting_value must be positive")
    if periods < 1 or simulations < 1:
        raise ValueError("periods and simulations must be positive")
    returns = np.asarray(historical_returns, dtype=float)
    if returns.size < 2 or not np.isfinite(returns).all():
        raise ValueError("historical_returns must contain at least two finite values")
    if (returns <= -1.0).any():
        raise ValueError("Returns must be greater than -100%")

    rng = np.random.default_rng(seed)
    sampled = rng.choice(returns, size=(simulations, periods), replace=True)
    paths = starting_value * np.cumprod(1.0 + sampled, axis=1)
    return np.column_stack([np.full(simulations, starting_value), paths])


def terminal_percentiles(paths: np.ndarray, percentiles=(5, 25, 50, 75, 95)) -> dict[int, float]:
    """Summarize terminal simulated values by percentile."""
    values = np.asarray(paths[:, -1], dtype=float)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("paths must be a non-empty 2D array")
    return {int(p): float(np.percentile(values, p)) for p in percentiles}
