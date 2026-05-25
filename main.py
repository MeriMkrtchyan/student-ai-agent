from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from anthropic import Anthropic
from agent import run_agent

app = FastAPI(title="Student AI Assistant")
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class AskRequest(BaseModel):
    question: str
    history: List[Dict[str, Any]] = []

@app.get("/health")
async def health():
    return {"status": "ok", "model": "claude-haiku-4-5-20251001"}

@app.post("/ask")
async def ask(req: AskRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    result = run_agent(req.question, req.history)
    return {"answer": result["answer"], "history": result["history"], "tools_used": result["tools_used"]}
