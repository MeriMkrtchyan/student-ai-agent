import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-haiku-4-5-20251001",  # ✅ CORRECT: current cheapest model
    max_tokens=500,
    messages=[{
        "role": "user",
        "content": "Explain photosynthesis in 3 sentences for a 10-year-old."
    }]
)

print(response.content[0].text)
