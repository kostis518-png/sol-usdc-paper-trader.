# SOL/USDC Paper-Trading Report

- Exact Binance Spot market: SOLUSDC (verified TRADING)
- Data fetched: 2026-11-21T07:26:05.164000+00:00
- Interval: 15m; closed candles only
- Latest closed candle: 2026-11-21T07:14:59.999000+00:00
- Latest closed close: 67.7400 USDC
- Current spot ticker (not candle close): 67.8800 USDC

## Indicators

| EMA20 | EMA50 | RSI14 | ATR14 |
|---:|---:|---:|---:|
| 66.8591 | 67.7815 | 56.12 | 0.7388 |

## Signal

**NO ENTRY**
Reason: EMA20 is not above EMA50.

## 30-day rolling backtest

- Closed trades: 64
- Realized net P&L: -190.73 USDC (1,000 USDC initial equity)
- Win rate: 20.31%
- Maximum marked-to-market drawdown: 19.07%
- Assumed fee: 0.10% each side; slippage: 0.05% each side
- Risk budget: 0.50% equity; stop: 1.5x ATR; target: 2.0R

## Rules and limitations

- Long-only spot; one open position maximum; no leverage or shorting.
- Entry: EMA20 > EMA50, RSI14 52-68, close > EMA20. Exit: stop, 2R target, EMA20 < EMA50, or RSI14 < 45.
- Backtest enters at next candle open; stop is assumed first if stop and target touch in the same candle.
- Fees and slippage are estimates, not account-specific actuals.
- Research baseline only; not yet validated as profitable. No API keys, wallet access, or order placement.
