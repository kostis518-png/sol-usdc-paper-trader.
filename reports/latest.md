# SOL/USDC Paper-Trading Report

- Exact Binance Spot market: SOLUSDC (verified TRADING; base SOL, quote USDC)
- Data fetched using Binance server time: 2026-11-15T18:20:30.129Z
- Interval: 15m; closed candles only
- Latest closed candle: 2026-11-15T18:00:00.000Z to 2026-11-15T18:14:59.999Z
- Latest closed candle OHLC: 71.42 / 71.64 / 71.16 / 71.22 USDC
- Latest closed candle close: 71.2200 USDC
- Current spot ticker (not candle close): 71.1600 USDC

## Indicators

| EMA20 | EMA50 | RSI14 | ATR14 |
|---:|---:|---:|---:|
| 71.5152 | 71.5604 | 43.84 | 0.4799 |

## Signal

**NO ENTRY — long-only Spot strategy; no short signal is generated.**

Entry conditions: EMA20 > EMA50, RSI14 between 52 and 68, and close > EMA20. All three conditions fail.

Exit conditions: EMA20 < EMA50 or RSI14 < 45. Both are currently true. If a simulated long is already open, the strategy's indicator-exit condition is triggered. The current live paper-position state was not read, so no claim is made that a position was actually closed.

No new entry, stop-loss, take-profit, or position size is issued because there is no qualifying entry.

## 30-day rolling historical replay

- Window: 2026-10-16 18:30 UTC through 2026-11-15 18:14:59 UTC
- Closed Binance Spot candles: 2,879
- Closed trades: 63
- Realized net P&L: -216.15 USDC (1,000 USDC initial simulated equity)
- Win rate: 15.87%
- Maximum marked-to-market drawdown: 21.81%
- Exit counts: 37 stops, 10 take-profits, 16 indicator exits
- Open simulated position at replay end: no
- Assumed fee: 0.10% each side; slippage: 0.05% each side
- Risk budget: 0.50% of simulated cash; stop: 1.5x ATR; target: 2.0R

This is a reproducible replay of the repository's current baseline logic over the stated historical window, not an independently audited or out-of-sample validation. The negative result is a warning that this baseline has performed poorly in this sample; it is not evidence of future performance.

## Rules and limitations

- Long-only spot; one simulated position maximum; no leverage or short selling.
- Entry: EMA20 > EMA50, RSI14 52-68, close > EMA20.
- Exit: stop, 2R target, EMA20 < EMA50, or RSI14 < 45.
- Backtest enters at next candle open; if stop and target are both touched in one candle, stop is assumed first.
- Fees and slippage are estimates, not account-specific actuals.
- Research only. No API keys, wallet access, real orders, or fund transfers.
