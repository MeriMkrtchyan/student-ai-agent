from dotenv import load_dotenv
load_dotenv()

import os
from anthropic import Anthropic

_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

TOOL_SCHEMAS = [
    {
        "name": "explain_topic",
        "description": "Explain a school topic clearly. Use for questions like explain photosynthesis or what is gravity.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "The topic to explain"},
                "grade_level": {"type": "string", "enum": ["middle school", "high school", "college"]}
            },
            "required": ["topic"]
        }
    },
    {
        "name": "find_examples",
        "description": "Find real-world examples or analogies. Use when student asks for examples.",
        "input_schema": {
            "type": "object",
            "properties": {
                "concept": {"type": "string", "description": "The concept to find examples for"},
                "count": {"type": "integer", "default": 2}
            },
            "required": ["concept"]
        }
    },
    {
        "name": "search_documents",
        "description": "Search uploaded documents. Use ONLY when question refers to uploaded material.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query for documents"}
            },
            "required": ["query"]
        }
    }
]

def explain_topic(topic: str, grade_level: str = "high school") -> str:
    response = _client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=800,
        messages=[{"role": "user", "content": f"Explain '{topic}' for a {grade_level} student. Use analogies."}]
    )
    return response.content[0].text

def find_examples(concept: str, count: int = 2) -> str:
    response = _client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=800,
        messages=[{"role": "user", "content": f"Give {count} real-world examples for '{concept}'."}]
    )
    return response.content[0].text

def search_documents(query: str) -> str:
    return f"Search results for: {query} --- no documents uploaded yet."

AVAILABLE_TOOLS = {
    "explain_topic": explain_topic,
    "find_examples": find_examples,
    "search_documents": search_documents,
}
