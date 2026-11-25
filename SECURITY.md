# Wallet and transaction security model

## Current release boundary

- Operating mode defaults to `PAPER`; unknown mode values also fail closed to `PAPER`.
- No wallet signing or transaction broadcasting is wired into the application.
- The security gate in `security_gate.py` is policy code only. It is not a transaction executor.
- The only permitted signing policy is user-initiated Solana Devnet signing after a successful simulation and explicit Phantom approval.
- Every broadcast policy additionally requires a separate execution confirmation.
- Strategy signals and background jobs cannot satisfy the user-initiation requirement.
- Mainnet broadcasting is blocked even when the opt-in environment flag is set: execution is deliberately unimplemented in this release.

## Configuration

The safe default requires no configuration. Optional development settings:

```env
TRADING_MODE=PAPER
MAINNET_BROADCAST_ENABLED=false
```

Do not set Mainnet enabled. Do not add wallet secrets, seed phrases, private keys, or exchange credentials to environment files or GitHub.

## Required future transaction sequence

1. User explicitly initiates a transaction.
2. Construct a transaction for Devnet only.
3. Validate token accounts, destination, amounts, network and limits.
4. Simulate and reject any simulation error.
5. Display network, token, amount, destination, estimated fees, slippage and minimum output.
6. Request explicit Phantom signing approval.
7. Show the signed transaction details and request a separate execution confirmation.
8. Only then may a separately reviewed Devnet broadcaster be implemented.

Mainnet requires a separate security review, project-owner configuration, and fresh confirmation for every transaction. No strategy signal may ever directly initiate a real transaction.
