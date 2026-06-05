# Student AI Assistant Agent

An AI agent that answers school-topic questions and searches uploaded documents using tool-calling with the Anthropic Claude API.

Built with Python, FastAPI, and ChromaDB. All tools are free-tier or open-source.

## Features

- Tool-calling agent -- Claude decides which of 3 tools to use: explain_topic, find_examples, search_documents
- Document upload -- Accepts PDF and TXT files, chunks and embeds them for semantic search
- RAG pipeline -- Retrieval-Augmented Generation using local ChromaDB (no cloud vector DB costs)
- Conversation memory -- Multi-turn chat with persistent history
- 100% local embeddings -- Uses all-MiniLM-L6-v2 (no paid embedding API)

## Tech Stack
FastAPI
Python
ChromaDB
Anthropic Claude API
Uvicorn

## Live Demo

https://student-ai-agent-fhur.onrender.com

## How to Run Locally
git clone https://github.com/your-username/student-ai-agent.git
cd student-ai-agent

python -m venv venv
source venv/bin/activate  # (Linux/Mac)
pip install -r requirements.txt

uvicorn main:app --reload
Environment Variables

Create a .env file:

ANTHROPIC_API_KEY=your_key_here

## Project Structure
main.py
agent.py
database.py
document_processor.py
static/
requirements.txt

## API Endpoints
GET / → Frontend
GET /health → Health check
POST /upload → Upload documents
POST /ask → Ask questions
