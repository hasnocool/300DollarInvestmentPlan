# Methodology

## Scope

This repository is a reproducible research framework for a hypothetical $300 crypto portfolio. It is designed to answer **what would have happened under explicit rules**, not what will happen next.

## Data contract

Every market series must contain:

- UTC timestamp;
- open, high, low, close, volume;
- unique timestamps;
- non-negative prices and volume;
- internally consistent high/low values.

The project should retain the original source and retrieval metadata alongside any dataset used for published results.

## Look-ahead prevention

Signals are calculated from information through day `t`. The backtester applies the target allocation beginning at `t+1`. This deliberately sacrifices some apparent backtest performance in exchange for a clearer causal ordering.

Do not calculate a signal using future bars, future fundamentals, or a later revised dataset.

## Costs

Every allocation change incurs configurable fees and slippage. A strategy that only works before costs should be treated as fragile.

## Compounding

The simulation reinvests portfolio gains and losses. There is no external contribution in the base experiment. Thus the starting value remains $300 and portfolio size changes solely through simulated performance.

## Risk reporting

Each experiment should report:

- terminal value;
- total return;
- CAGR;
- annualized volatility;
- maximum drawdown;
- Sharpe-like ratio;
- number of rebalance events;
- turnover;
- sensitivity to fees and slippage.

Maximum drawdown is especially important for a small account because a large loss can require a disproportionately large subsequent gain to recover.

## Validation design

Tests use synthetic deterministic data to verify mathematical behavior independently of market history. This prevents a broken implementation from being hidden behind plausible-looking charts.

Before publishing a backtest:

1. Run the unit suite.
2. Run formatting/lint checks.
3. Pin or record the data snapshot.
4. Inspect the first and last trades manually.
5. Confirm that signals cannot use future rows.
6. Compare the strategy against a simple hand-calculated fixture.
7. Re-run with costs disabled and verify the expected difference.
8. Run parameter sensitivity instead of selecting one favorable parameter set.

## Monte Carlo

Bootstrap simulation resamples historical daily returns with replacement. It is useful for producing a distribution of hypothetical outcomes. It does **not** establish a confidence interval for the actual future market and does not preserve all time-series dependencies.

For stronger research, later versions should add block bootstrap, regime-conditioned simulations, and walk-forward validation.

## Forecasting policy

The system must never turn a historical CAGR into a promised future account value. Forward scenarios should be labeled explicitly as assumptions such as `bear`, `base`, and `bull`, and should be shown as ranges.
