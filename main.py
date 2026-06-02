from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from anthropic import Anthropic
from agent import run_agent
from document_processor import extract_text_from_pdf, extract_text_from_txt
from database import add_document

app = FastAPI(title="Student AI Assistant")
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class AskRequest(BaseModel):
    question: str
    history: List[Dict[str, Any]] = []

@app.get("/")
async def root():
    return {"message": "Student AI Assistant is running. Use POST /ask or POST /upload"}

@app.get("/health")
async def health():
    return {"status": "ok", "model": "claude-haiku-4-5-20251001"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename")
    
    content = await file.read()
    
    if file.filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(content)
    elif file.filename.lower().endswith(".txt"):
        text = extract_text_from_txt(content)
    else:
        raise HTTPException(status_code=400, detail="Only PDF and TXT supported")
    
    num_chunks = add_document(file.filename, text)
    return {"status": "success", "filename": file.filename, "chunks_stored": num_chunks}

@app.post("/ask")
async def ask(req: AskRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    result = run_agent(req.question, req.history)
    return {"answer": result["answer"], "history": result["history"], "tools_used": result["tools_used"]}
