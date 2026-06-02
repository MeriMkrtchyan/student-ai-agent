# Student AI Assistant Agent

An AI agent that answers school-topic questions and searches uploaded documents using tool-calling with the Anthropic Claude API.

Built with Python, FastAPI, and ChromaDB. All tools are free-tier or open-source.

## Features

- Tool-calling agent -- Claude decides which of 3 tools to use: explain_topic, find_examples, search_documents
- Document upload -- Accepts PDF and TXT files, chunks and embeds them for semantic search
- RAG pipeline -- Retrieval-Augmented Generation using local ChromaDB (no cloud vector DB costs)
- Conversation memory -- Multi-turn chat with persistent history
- 100% local embeddings -- Uses all-MiniLM-L6-v2 (no paid embedding API)

## Quick Start

```bash
# 1. Clone & enter
git clone &lt;your-repo-url&gt;
cd student-ai-agent

# 2. Virtual env
python3 -m venv venv && source venv/bin/activate

# 3. Install
pip install -r requirements.txt

# 4. API key
cp .env.example .env
# Edit .env: paste your key from console.anthropic.com

# 5. Run
uvicorn main:app --reload

# 6. Open http://localhost:8000# Student AI Assistant Agent
