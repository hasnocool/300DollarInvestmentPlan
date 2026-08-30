# src/crypto300/metrics.py
"""Performance and risk metrics."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd


def total_return(equity: pd.Series) -> float:
    _require_equity(equity)
    return float(equity.iloc[-1] / equity.iloc[0] - 1.0)


def cagr(equity: pd.Series, periods_per_year: int = 365) -> float:
    _require_equity(equity)
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive")
    periods = len(equity) - 1
    if periods <= 0:
        return 0.0
    return float((equity.iloc[-1] / equity.iloc[0]) ** (periods_per_year / periods) - 1.0)


def volatility(equity: pd.Series, periods_per_year: int = 365) -> float:
    _require_equity(equity)
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive")
    returns = equity.pct_change().dropna()
    return float(returns.std(ddof=1) * math.sqrt(periods_per_year)) if len(returns) > 1 else 0.0


def max_drawdown(equity: pd.Series) -> float:
    _require_equity(equity)
    drawdown = equity / equity.cummax() - 1.0
    return float(drawdown.min())


def sharpe_like(equity: pd.Series, periods_per_year: int = 365, risk_free: float = 0.0) -> float:
    _require_equity(equity)
    returns = equity.pct_change().dropna()
    if len(returns) < 2:
        return 0.0
    rf_period = (1.0 + risk_free) ** (1.0 / periods_per_year) - 1.0
    excess = returns - rf_period
    std = excess.std(ddof=1)
    return float(excess.mean() / std * math.sqrt(periods_per_year)) if std > 0 else 0.0


def summarize(equity: pd.Series, trades: int, turnover: pd.Series) -> dict[str, float]:
    return {
        "start_value": float(equity.iloc[0]),
        "end_value": float(equity.iloc[-1]),
        "total_return": total_return(equity),
        "cagr": cagr(equity),
        "annualized_volatility": volatility(equity),
        "max_drawdown": max_drawdown(equity),
        "sharpe_like": sharpe_like(equity),
        "trades": float(trades),
        "turnover": float(turnover.sum()),
    }


def _require_equity(equity: pd.Series) -> None:
    if equity.empty:
        raise ValueError("Equity series cannot be empty")
    if not np.isfinite(equity.to_numpy(dtype=float)).all():
        raise ValueError("Equity contains non-finite values")
    if (equity <= 0).any():
        raise ValueError("Equity must remain positive")
