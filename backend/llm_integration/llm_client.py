### File: backend/llm_integration/llm_client.py
import requests
import os
from dotenv import load_dotenv
from .prompt_engineering import format_prompt

load_dotenv()

LM_API_URL = os.getenv("LM_API_URL", "http://127.0.0.1:1234/v1/chat/completions")

def query_llm_direct(prompt: str, temperature=0.7):
    headers = {"Content-Type": "application/json"}

    # Use prompt engineering utility
    formatted_prompt = format_prompt(prompt)

    messages = [
        {"role": "system", "content": "You are a helpful research assistant. Answer concisely and only based on verified knowledge."},
        {"role": "user", "content": formatted_prompt}
    ]

    payload = {
        "model": "local-model",
        "messages": messages,
        "temperature": temperature
    }

    response = requests.post(LM_API_URL, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()
    if "choices" not in result:
        raise ValueError(f"Unexpected response: {result}")

    return result["choices"][0]["message"]["content"]