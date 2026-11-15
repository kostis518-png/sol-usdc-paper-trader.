# SOL/USDC Paper-Trading Report

- Exact Binance Spot market: SOLUSDC (verified TRADING)
- Data fetched: 2026-11-15T07:19:32.944000+00:00
- Interval: 15m; closed candles only
- Latest closed candle: 2026-11-15T07:14:59.999000+00:00
- Latest closed close: 70.2900 USDC
- Current spot ticker (not candle close): 70.4500 USDC

## Indicators

| EMA20 | EMA50 | RSI14 | ATR14 |
|---:|---:|---:|---:|
| 70.6640 | 71.0800 | 45.53 | 0.6254 |

## Signal

**NO ENTRY**
Reason: EMA20 is not above EMA50; RSI14 is outside 52-68; close is not above EMA20.

## 30-day rolling backtest

- Closed trades: 61
- Realized net P&L: -208.54 USDC (1,000 USDC initial equity)
- Win rate: 16.39%
- Maximum marked-to-market drawdown: 21.55%
- Assumed fee: 0.10% each side; slippage: 0.05% each side
- Risk budget: 0.50% equity; stop: 1.5x ATR; target: 2.0R

## Rules and limitations

- Long-only spot; one open position maximum; no leverage or shorting.
- Entry: EMA20 > EMA50, RSI14 52-68, close > EMA20. Exit: stop, 2R target, EMA20 < EMA50, or RSI14 < 45.
- Backtest enters at next candle open; stop is assumed first if stop and target touch in the same candle.
- Fees and slippage are estimates, not account-specific actuals.
- Research baseline only; not yet validated as profitable. No API keys, wallet access, or order placement.
