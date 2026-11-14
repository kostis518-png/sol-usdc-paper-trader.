# SOL/USDC Paper Trader

A paper-only research and backtesting tool for the exact Binance Spot SOL/USDC market (symbol: SOLUSDC).

## Safety

- Public Binance Spot market-data endpoints only.
- No API keys, wallet connections, private account data, or order placement.
- Long-only spot simulation; no leverage and no short selling.
- All entries and exits are simulated. No funds are moved.
- Historical backtests are not predictions or guarantees.

## Strategy baseline

- Candle interval: 15 minutes; evaluate closed candles only.
- Indicators: EMA20, EMA50, Wilder RSI14, and Wilder ATR14.
- Entry: EMA20 > EMA50, RSI14 between 52 and 68, and close > EMA20.
- Exit: ATR stop at 1.5x ATR, target at 2R, EMA20 < EMA50, or RSI14 < 45.
- Position sizing: risk budget 0.5% of simulated cash; one position at a time.
- Backtest execution: next candle open; if stop and target are both touched in one candle, assume stop first.
- Cost assumptions: 0.10% fee and 0.05% slippage per side. Adjust these to match actual account conditions before relying on results.

This is an initial research baseline, not a proven profitable strategy. Evaluate it across multiple market regimes and compare out-of-sample performance before considering any real-money use.

## Run locally

Requires Python 3.10+; no third-party packages.

```bash
python paper_trader.py --days 30 --output reports/latest.md
```

## Daily report automation

GitHub Actions runs daily at 06:15 UTC and can also be started manually from the Actions tab. Each run generates and commits `reports/latest.md`.

Workflow: `.github/workflows/daily-report.yml`

## Market-data integrity

The runner verifies that Binance reports SOLUSDC with base asset SOL, quote asset USDC, and status TRADING. It fails closed if the exact pair is unavailable; it never substitutes another quote asset or venue. The currently forming candle is excluded using Binance server time.
