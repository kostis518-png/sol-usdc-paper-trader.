# SOL/USDC 90-Day Validation — 2026-11-19

## Method

- Binance Spot SOLUSDC, 15-minute candles only
- 8,640 closed candles covering approximately 90 days
- 70% chronological development segment and final 30% holdout segment
- 1,000 USDC starting equity per independently evaluated segment
- 0.10% fee and 0.05% adverse slippage per side
- 0.50% of available cash risk budget per position; one position at a time
- Long-only, no leverage
- Entries at next candle open; stop-first if stop and target are touched in the same candle
- No parameter selection based on the holdout segment

## Results

| Variant | Full-sample trades | Full-sample net realized P&L | Full-sample max drawdown | Holdout trades | Holdout net realized P&L | Holdout max drawdown |
|---|---:|---:|---:|---:|---:|---:|
| EMA20/50, RSI 52–68 | 267 | -564.53 USDC | 56.45% | 62 | -184.37 USDC | 18.44% |
| EMA20/50, RSI 55–65 + cooldown | 208 | -472.31 USDC | 47.90% | 51 | -143.84 USDC | 15.32% |
| EMA30/100, RSI 55–65 + cooldown | 158 | -377.05 USDC | 38.90% | 29 | -51.58 USDC | 6.18% |

The development segment ended with an open position in each tested variant. Its reported P&L is realized P&L only and excludes the unrealized value of that position. The holdout segments ended flat.

## Decision

**Reject all three variants for live deployment.** Every full-sample and holdout result is materially negative after modeled costs. The slower EMA30/100 filter reduces drawdown and losses, but does not establish positive expectancy.

Do not connect trading credentials, enable order placement, or use leverage. Continue paper-only research.

## Next research gates

1. Fix end-of-window accounting in the production backtester: report realized P&L, unrealized P&L, and equity including any open position separately.
2. Add a complete trade ledger and compare against buy-and-hold and a no-trade benchmark.
3. Run walk-forward tests over several non-overlapping 90-day windows and different market regimes.
4. Test whether a volatility/trend regime filter improves holdout expectancy without excessive parameter tuning.
5. Require positive net expectancy, adequate trade count, and controlled drawdown across multiple holdout windows before considering any live use.

## Reproducibility note

This is an independent verification simulation using Binance public market data and the repository's entry/exit rules and stated cost assumptions. Small numerical differences from the scheduled report can arise from the server-time cutoff and end-of-window treatment. This report is diagnostic and does not replace the production report.
