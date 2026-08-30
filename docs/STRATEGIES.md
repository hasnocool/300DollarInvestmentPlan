# Strategy Suite

The initial suite intentionally uses simple rules so that results can be audited.

## 1. Buy and hold

A fixed allocation is established and left alone. This is the control group.

Example research allocation:

- BTC: 60%
- ETH: 20%
- Cash: 20%

The percentages are **test parameters**, not a recommendation.

## 2. Periodic rebalance

A target allocation is restored on a fixed schedule such as 30 days. This tests whether systematic rebalancing changes risk-adjusted results relative to buy-and-hold.

## 3. Trend-following

An asset receives its configured risky weight only while its close is above its simple moving average. Otherwise the allocation is cash.

The initial implementation uses a configurable lookback such as 100 days. The parameter must be tested across a range rather than optimized on the entire history.

## 4. Cash-preserving comparison

Because a $300 portfolio is small, a useful control is a strategy that can hold substantial cash. This helps distinguish returns caused by taking more market risk from returns caused by the trading rule itself.

## 5. Required comparisons

Every report should compare strategies on identical data and cost assumptions:

| Strategy | Return | CAGR | Volatility | Max drawdown | Turnover | Trades |
|---|---:|---:|---:|---:|---:|---:|
| Buy & hold | | | | | | |
| Periodic rebalance | | | | | | |
| Trend following | | | | | | |

Do not choose the winner using return alone.

## Future strategy modules

Planned research extensions:

- volatility targeting;
- drawdown-aware exposure caps;
- regime detection;
- moving-average crossovers;
- momentum ranking;
- block-bootstrap validation;
- walk-forward parameter selection;
- out-of-sample evaluation;
- portfolio-level risk budgeting.

No strategy should be promoted to live use merely because it wins one historical backtest.
