"""Read-only OpenAI backend scaffold for the SOL/USDC project.

No wallet signing, private keys, exchange credentials, or order placement.
"""
import os
from typing import Annotated

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field

app = FastAPI(title="SOL/USDC AI Assistant API", version="0.1.0")

origins = [
    item.strip()
    for item in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    if item.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

class AnalyzeRequest(BaseModel):
    question: Annotated[str, Field(min_length=1, max_length=4000)]

class AnalyzeResponse(BaseModel):
    answer: str
    mode: str = "read-only"

@app.get("/health")
def health():
    return {"status": "ok", "mode": "read-only"}

@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")
    if not api_key or not model:
        raise HTTPException(
            status_code=503,
            detail="Server configuration incomplete: set OPENAI_API_KEY and OPENAI_MODEL.",
        )

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=model,
            instructions=(
                "You are a cautious SOL/USDC market research assistant. "
                "Explain uncertainty, distinguish verified data from assumptions, "
                "and never claim to have placed trades. This service is read-only: "
                "never request seed phrases, private keys, API secrets, or wallet "
                "signatures. Do not instruct the user to enable automatic trading."
            ),
            input=request.question,
        )
        return AnalyzeResponse(answer=response.output_text)
    except Exception:
        # Do not return provider errors that might expose configuration details.
        raise HTTPException(status_code=502, detail="AI analysis request failed.")
