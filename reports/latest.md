# SOL/USDC Paper-Trading Report

- Exact Binance Spot market: SOLUSDC (verified TRADING)
- Data fetched: 2026-11-23T07:50:16.657000+00:00
- Interval: 15m; closed candles only
- Latest closed candle: 2026-11-23T07:44:59.999000+00:00
- Latest closed close: 71.9700 USDC
- Current spot ticker (not candle close): 71.9200 USDC

## Indicators

| EMA20 | EMA50 | RSI14 | ATR14 |
|---:|---:|---:|---:|
| 71.5270 | 70.9975 | 65.43 | 0.3260 |

## Signal

**PAPER LONG SETUP**
- Reference close entry: 71.9700
- Illustrative ATR stop: 71.4810
- Illustrative 2R target: 72.9480
- Simulated execution would occur at next candle open.

## 30-day rolling backtest

- Closed trades: 68
- Realized net P&L: -186.58 USDC (1,000 USDC initial equity)
- Win rate: 22.06%
- Maximum marked-to-market drawdown: 20.16%
- Assumed fee: 0.10% each side; slippage: 0.05% each side
- Risk budget: 0.50% equity; stop: 1.5x ATR; target: 2.0R

## Rules and limitations

- Long-only spot; one open position maximum; no leverage or shorting.
- Entry: EMA20 > EMA50, RSI14 52-68, close > EMA20. Exit: stop, 2R target, EMA20 < EMA50, or RSI14 < 45.
- Backtest enters at next candle open; stop is assumed first if stop and target touch in the same candle.
- Fees and slippage are estimates, not account-specific actuals.
- Research baseline only; not yet validated as profitable. No API keys, wallet access, or order placement.
