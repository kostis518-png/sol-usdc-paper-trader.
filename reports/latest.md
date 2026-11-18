# SOL/USDC Paper-Trading Report

- Exact Binance Spot market: SOLUSDC (verified TRADING)
- Data fetched: 2026-11-18T07:31:24.091000+00:00
- Interval: 15m; closed candles only
- Latest closed candle: 2026-11-18T07:29:59.999000+00:00
- Latest closed close: 75.0800 USDC
- Current spot ticker (not candle close): 74.9900 USDC

## Indicators

| EMA20 | EMA50 | RSI14 | ATR14 |
|---:|---:|---:|---:|
| 74.8581 | 74.3810 | 56.46 | 0.3513 |

## Signal

**PAPER LONG SETUP**
- Reference close entry: 75.0800
- Illustrative ATR stop: 74.5530
- Illustrative 2R target: 76.1340
- Simulated execution would occur at next candle open.

## 30-day rolling backtest

- Closed trades: 69
- Realized net P&L: -212.26 USDC (1,000 USDC initial equity)
- Win rate: 18.84%
- Maximum marked-to-market drawdown: 21.48%
- Assumed fee: 0.10% each side; slippage: 0.05% each side
- Risk budget: 0.50% equity; stop: 1.5x ATR; target: 2.0R

## Rules and limitations

- Long-only spot; one open position maximum; no leverage or shorting.
- Entry: EMA20 > EMA50, RSI14 52-68, close > EMA20. Exit: stop, 2R target, EMA20 < EMA50, or RSI14 < 45.
- Backtest enters at next candle open; stop is assumed first if stop and target touch in the same candle.
- Fees and slippage are estimates, not account-specific actuals.
- Research baseline only; not yet validated as profitable. No API keys, wallet access, or order placement.
