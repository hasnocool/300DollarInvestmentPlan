# src/crypto300/backtest.py
"""Deterministic long-only portfolio backtester.

Trades are applied using the next period's close, so a signal computed from
period t cannot trade at period t's close. This is a simple guard against
look-ahead bias.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class BacktestConfig:
    initial_capital: float = 300.0
    fee_rate: float = 0.001
    slippage_rate: float = 0.0005

    @property
    def round_trip_cost(self) -> float:
        return self.fee_rate + self.slippage_rate


@dataclass(frozen=True)
class BacktestResult:
    equity: pd.Series
    weights: pd.DataFrame
    turnover: pd.Series
    trades: int


def run_backtest(close: pd.DataFrame, target_weights: pd.DataFrame, config: BacktestConfig) -> BacktestResult:
    """Run a close-to-close portfolio simulation with fees and slippage.

    `target_weights.loc[t]` is calculated using information available through
    t and is therefore executed at t+1. The final signal has no execution.
    Cash is the residual weight. Negative weights are rejected.
    """
    if config.initial_capital <= 0:
        raise ValueError("initial_capital must be positive")
    if config.fee_rate < 0 or config.slippage_rate < 0:
        raise ValueError("Costs cannot be negative")
    close = close.astype(float).sort_index()
    target_weights = target_weights.reindex(index=close.index, columns=close.columns).fillna(0.0)
    if (target_weights < 0).any().any():
        raise ValueError("Negative target weights are not supported")
    if (target_weights.sum(axis=1) > 1.0 + 1e-9).any():
        raise ValueError("Target weights cannot exceed 100%")
    if len(close) < 2:
        raise ValueError("At least two observations are required")

    returns = close.pct_change().fillna(0.0)
    executed = target_weights.shift(1).fillna(0.0)
    previous = pd.Series(0.0, index=close.columns)
    equity = pd.Series(index=close.index, dtype=float)
    turnover = pd.Series(0.0, index=close.index, dtype=float)
    value = config.initial_capital
    trades = 0

    for timestamp in close.index:
        desired = executed.loc[timestamp].clip(lower=0.0)
        gross = float((desired * returns.loc[timestamp]).sum())
        traded_weight = float((desired - previous).abs().sum())
        cost = traded_weight * config.round_trip_cost
        value *= max(0.0, 1.0 + gross - cost)
        equity.loc[timestamp] = value
        turnover.loc[timestamp] = traded_weight
        trades += int(traded_weight > 1e-12)
        previous = desired

    return BacktestResult(equity=equity, weights=executed, turnover=turnover, trades=trades)
