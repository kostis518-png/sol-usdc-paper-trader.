# Read-only AI backend

This is a separate backend scaffold. The existing `paper_trader.py` and its scheduled report workflow are unchanged.

## Run in GitHub Codespaces

Open a Codespace on branch `feature/phantom-openai-readonly`, then in the terminal:

```bash
cd api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` in the Codespace and set:
- `OPENAI_API_KEY`: the replacement key, stored only in this ignored local file for development.
- `OPENAI_MODEL`: a model name enabled for your API project.
- `CORS_ORIGINS`: the exact frontend origin when a frontend is added.

Start the server:

```bash
set -a && source .env && set +a
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Open the forwarded port 8000 and visit `/health`. The analysis endpoint is `POST /api/analyze` with JSON `{"question":"Summarize the SOL/USDC research rules."}`.

## Security boundary

- Never commit `.env`, API keys, wallet secrets, or recovery phrases.
- Never place an OpenAI API key in browser code.
- This scaffold has no Phantom connection, wallet signing, exchange credentials, or live order endpoints.
- Do not expose this development server publicly as a production service. Before deployment, add authentication, rate limits, request logging with secret redaction, and a strict production CORS allowlist.
- Phantom connection and user-approved transaction previews will be implemented as a separate frontend step. Every transaction must be reviewed and signed by the user in Phantom.
