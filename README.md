# SOL/USDC Paper Trader + Phantom Wallet Dashboard

A paper-only quantitative research project for the exact Binance Spot SOL/USDC market (symbol: `SOLUSDC`), with a mobile-first Phantom wallet monitoring interface.

## Safety

- Paper trading is the default. No exchange trading credentials or order placement.
- The web dashboard uses the official Phantom Connect React SDK and reads public wallet balances on Solana Devnet only.
- The current dashboard does not request signatures, construct transactions, or broadcast transactions.
- `security_gate.py` defines fail-closed policy checks for a future user-approved signing flow. It is not a transaction executor.
- Mainnet transaction execution is disabled and unimplemented.
- Never enter a seed phrase, private key, or recovery phrase into this project.

See [SECURITY.md](SECURITY.md) for the approval model.

## Existing strategy baseline

- Candle interval: 15 minutes; closed candles only.
- Indicators: EMA20, EMA50, Wilder RSI14, and Wilder ATR14.
- Entry: EMA20 > EMA50, RSI14 between 52 and 68, and close > EMA20.
- Exit: ATR stop at 1.5x ATR, target at 2R, EMA20 < EMA50, or RSI14 < 45.
- Position sizing: risk budget 0.5% of simulated cash; one position at a time.
- Backtest execution: next candle open; if stop and target are both touched in one candle, assume stop first.
- Cost assumptions: 0.10% fee and 0.05% slippage per side.

**Research status:** existing 30-day and 90-day validation reports show negative results after modeled costs. The strategy is not validated as profitable and must remain paper-only.

## Run the Python paper trader

Requires Python 3.10+; no third-party packages.

```bash
python paper_trader.py --days 30 --output reports/latest.md
```

Run security policy tests:

```bash
python -m unittest discover -s tests -v
```

## Run the web dashboard

Requires Node.js 20+ and npm.

```bash
cd web
npm install
npm run dev
```

Open the Vite URL shown in the terminal. For Android, open the forwarded HTTPS port from your Codespace. Phantom mobile connection works through the official Phantom Connect SDK flow; wallet connection still requires the user to approve it in Phantom.

### Dashboard scope in this release

- Phantom connection/disconnection UI using `@phantom/react-sdk`.
- Devnet SOL and USDC balance reads.
- Binance public SOLUSDC ticker only; no quote-pair substitution.
- Explicit PAPER MODE and REAL TRADING DISABLED statuses.
- No wallet signing or transaction broadcast functionality.

The dashboard uses the Solana Devnet USDC mint. It does not display Mainnet wallet balances.

## GitHub Actions

- `.github/workflows/daily-report.yml`: existing daily paper report.
- `.github/workflows/security-tests.yml`: Python security-gate tests on Python 3.10, 3.11 and 3.12.

## Limitations / next milestones

- The frontend has not yet been built or run in a live browser in this environment.
- Phantom connection and mobile deeplink behavior require end-to-end testing on Android with the Phantom app installed.
- The strategy engine still needs end-of-window position accounting, a trade ledger, volume confirmation, 1h analysis, and multi-window walk-forward validation.
- Transaction construction, simulation, token account inspection, and user-approved Devnet signing are not implemented yet.
- Mainnet remains disabled and unimplemented.
