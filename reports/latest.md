# SOL/USDC Paper-Trading Report

- Exact Binance Spot market: SOLUSDC (verified TRADING)
- Data fetched: 2026-11-19T07:33:36.407000+00:00
- Interval: 15m; closed candles only
- Latest closed candle: 2026-11-19T07:29:59.999000+00:00
- Latest closed close: 74.7000 USDC
- Current spot ticker (not candle close): 74.6600 USDC

## Indicators

| EMA20 | EMA50 | RSI14 | ATR14 |
|---:|---:|---:|---:|
| 74.3811 | 73.9728 | 61.94 | 0.3100 |

## Signal

**PAPER LONG SETUP**
- Reference close entry: 74.7000
- Illustrative ATR stop: 74.2350
- Illustrative 2R target: 75.6299
- Simulated execution would occur at next candle open.

## 30-day rolling backtest

- Closed trades: 67
- Realized net P&L: -194.28 USDC (1,000 USDC initial equity)
- Win rate: 20.90%
- Maximum marked-to-market drawdown: 20.29%
- Assumed fee: 0.10% each side; slippage: 0.05% each side
- Risk budget: 0.50% equity; stop: 1.5x ATR; target: 2.0R

## Rules and limitations

- Long-only spot; one open position maximum; no leverage or shorting.
- Entry: EMA20 > EMA50, RSI14 52-68, close > EMA20. Exit: stop, 2R target, EMA20 < EMA50, or RSI14 < 45.
- Backtest enters at next candle open; stop is assumed first if stop and target touch in the same candle.
- Fees and slippage are estimates, not account-specific actuals.
- Research baseline only; not yet validated as profitable. No API keys, wallet access, or order placement.
