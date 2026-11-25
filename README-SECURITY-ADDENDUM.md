# Security foundation implementation

This branch adds a fail-closed operating-mode and transaction approval policy.

- `security_gate.py`: PAPER/DEVNET/MAINNET mode model and signing/broadcast gates.
- `tests/test_security_gate.py`: tests for default PAPER mode, user initiation, simulation, Phantom approval, separate execution confirmation and Mainnet blocking.
- `.github/workflows/security-tests.yml`: Python 3.10–3.12 CI test matrix.
- `SECURITY.md`: transaction sequence and security boundaries.

Run locally:

```bash
python -m unittest discover -s tests -v
```

This is the first security milestone, not the complete Phantom integration. No wallet connection, signing, swap, or broadcast code is added by this change.
