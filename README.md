# SOL/USDC Paper Trader

A paper-only research and backtesting tool for Binance Spot SOL/USDC market data.

## Safety

- Public market-data endpoints only.
- No Binance API keys, wallet connections, or order-placement code.
- All entries, exits, stop-losses, and take-profits are simulated.
- Historical backtests are not predictions or guarantees.

## Initial strategy

The initial research baseline uses EMA 20/EMA 50 trend alignment, RSI(14) momentum confirmation, and ATR(14)-based risk levels. Signals are evaluated only after a candle closes. Backtests must include configurable fees and slippage and avoid look-ahead bias.

## Project status

This repository is being built as a paper-only system. No live trading functionality is included.