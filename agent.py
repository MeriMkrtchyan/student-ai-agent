import os
from typing import List, Dict, Any
from anthropic import Anthropic
from tools import TOOL_SCHEMAS, AVAILABLE_TOOLS

_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a helpful AI student assistant.
You have three tools: explain_topic, find_examples, search_documents.
Use the right tool for the job. If no tool is needed, answer directly."""

def run_agent(user_message: str, conversation_history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    messages = list(conversation_history) if conversation_history else []
    messages.append({"role": "user", "content": user_message})
    
    tools_used = []
    max_iterations = 5
    
    for iteration in range(max_iterations):
        response = _client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOL_SCHEMAS,
            messages=messages
        )
        
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    tools_used.append(tool_name)
                    
                    result = AVAILABLE_TOOLS[tool_name](**tool_input)
                    
                    messages.append({
                        "role": "user",
                        "content": [{"type": "tool_result", "tool_use_id": block.id, "content": str(result)}]
                    })
        else:
            final_answer = response.content[0].text
            updated_history = list(conversation_history) if conversation_history else []
            updated_history.append({"role": "user", "content": user_message})
            updated_history.append({"role": "assistant", "content": final_answer})
            
            return {"answer": final_answer, "history": updated_history, "tools_used": tools_used}
    
    return {"answer": "Thinking limit reached.", "history": messages, "tools_used": tools_used}
