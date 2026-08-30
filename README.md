# $300 Crypto Paper-Trading Research Lab

A research and paper-trading framework for studying how a small hypothetical crypto portfolio might compound under explicit, testable rules.

> **Research only.** This project does not predict prices, guarantee returns, or provide personalized financial advice. Crypto assets are highly volatile and losses can exceed expectations. The default workflow is backtesting and simulation rather than live trading.

## Goals

- Start with a hypothetical `$300` portfolio.
- Compare buy-and-hold, periodic rebalancing, trend-following, and cash-preserving approaches.
- Include fees, slippage, position limits, and drawdown measurements.
- Avoid look-ahead bias and survivorship assumptions.
- Produce deterministic tests before trusting results.
- Separate historical backtesting from forward-looking scenario analysis.
- Support Monte Carlo resampling to show outcome ranges rather than a single forecast.

## Research questions

1. How much does compounding change outcomes when returns are volatile?
2. Which simple rules historically reduced drawdown without destroying too much upside?
3. How sensitive are results to fees, slippage, rebalance frequency, and trend parameters?
4. What range of outcomes is plausible under different return regimes?
5. How often does a strategy lose money despite having a positive long-run historical result?

## Project structure

```text
300DollarInvestmentPlan/
├── README.md
├── pyproject.toml
├── docs/
│   ├── METHODOLOGY.md
│   ├── STRATEGIES.md
│   └── RESULTS.md
├── src/
│   └── crypto300/
│       ├── __init__.py
│       ├── backtest.py
│       ├── data.py
│       ├── metrics.py
│       ├── scenarios.py
│       └── strategies.py
└── tests/
    ├── test_backtest.py
    ├── test_metrics.py
    └── test_strategies.py
```

## Python

Python **3.12+** is required.

Install development dependencies:

```bash
python -m pip install -e '.[dev]'
```

Run the complete test suite:

```bash
python -m pytest
```

Run static checks:

```bash
python -m ruff check .
python -m ruff format --check .
```

## Data

The backtester consumes normalized daily OHLCV data. The framework intentionally keeps the strategy engine independent of a particular exchange or data vendor.

For reproducible research, save a fixed historical dataset and record its source, retrieval date, timezone, and symbol universe. Do **not** silently mix datasets from different vendors.

## Core assumptions

The initial research configuration is deliberately conservative:

- Starting capital: `$300`.
- No leverage.
- No short selling.
- No borrowing.
- Long-only spot positions.
- Fees and slippage are charged on every rebalance.
- Portfolio weights are capped.
- Strategies may hold cash.
- Compounding occurs naturally through reinvestment of portfolio value.

These are research defaults, not recommendations for real-money trading.

## Important interpretation rule

A backtest is not a forecast. Historical performance can be useful for evaluating whether a rule is internally coherent, but it cannot establish what the portfolio will be worth in the future.

The project therefore reports:

- historical CAGR/return;
- volatility;
- maximum drawdown;
- Sharpe-like risk-adjusted return;
- number of trades;
- turnover;
- ending value;
- Monte Carlo percentile ranges;
- sensitivity to costs.

It should **not** report an asserted future value as if it were predictable.

## License

Add the project's preferred license before public distribution.
