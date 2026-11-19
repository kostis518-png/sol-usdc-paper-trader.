# SOL/USDC Strategy Review — 2026-11-19

## Scope

- Market: Binance Spot SOLUSDC only
- Timeframe: 15-minute candles
- Sample: 2,880 closed candles, approximately 30 days
- Starting simulated equity: 1,000 USDC
- Entry execution: next candle open with 0.05% adverse slippage
- Exit execution: stop/target/indicator price with 0.05% adverse slippage
- Fees: 0.10% per side
- Risk budget: 0.50% of available equity per trade
- Long-only, one position maximum, no leverage
- Stop-first assumption when stop and target are both touched in one candle
- Out-of-sample split: first 70% for development, final 30% for holdout evaluation

This is a research diagnostic, not a claim of profitability. The variants below were evaluated on the same historical sample; the small holdout contains relatively few trades and is not statistically conclusive.

## Results

| Variant | Full-sample closed trades | Full-sample net realized P&L | Full-sample max drawdown | Holdout trades | Holdout net realized P&L | Holdout max drawdown |
|---|---:|---:|---:|---:|---:|---:|
| Baseline EMA20/50, RSI 52–68 | 66 | -188.67 USDC | 19.54% | 21 | -34.53 USDC | 4.72% |
| Baseline + one-bar re-entry cooldown | 62 | -187.59 USDC | 19.28% | 19 | -24.35 USDC | 3.91% |
| EMA20/50, RSI 55–65 + cooldown | 57 | -166.21 USDC | 17.96% | 18 | -19.85 USDC | 4.44% |
| EMA30/100, RSI 55–65 + cooldown | 29 | -51.37 USDC | 6.16% | 13 | -4.85 USDC | 2.99% |

## Interpretation

1. None of the tested variants was profitable after the modeled fees and slippage.
2. The slower EMA30/100 filter reduced trade frequency and drawdown materially in this sample, but remained net negative.
3. A one-bar cooldown after an exit reduced repeated entries and improved the baseline holdout loss, but did not produce a positive expectancy.
4. The holdout is only about nine days and contains 13–21 trades per variant. It is too small to validate a robust edge.
5. Do not deploy this strategy with real funds, leverage, or automated order execution.

## Engineering and research actions before any live consideration

- Keep the existing baseline unchanged until a replacement passes validation.
- Add explicit end-of-test open-position valuation/closure to the official report so realized and unrealized P&L are not confused.
- Add a trade ledger with entry/exit timestamps, fills, fees, slippage, exit reason, and per-trade R multiple.
- Add walk-forward testing over multiple non-overlapping market regimes, not just one 30-day window.
- Test parameter stability and include a benchmark such as buy-and-hold over the same dates.
- Add a no-trade gate when the strategy has negative out-of-sample expectancy or drawdown exceeds a defined limit.
- Keep the system paper-only. No API keys, wallet connections, or order placement.

## Data and reproducibility note

The figures are from a separate verification simulation over Binance public SOLUSDC 15-minute candles using the strategy rules and stated cost assumptions. Small differences from `reports/latest.md` can occur because the daily workflow fetches at a different server-time boundary and handles any open position at the end of the sample differently. The review is therefore a diagnostic comparison, not a replacement for the official daily report.
