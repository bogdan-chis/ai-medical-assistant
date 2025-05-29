# ### File: backend/llm_integration/llm_client.py
# import requests
# import os
# from dotenv import load_dotenv
# from .prompt_engineering import format_prompt, format_context_passage, prompt_text

# load_dotenv()

# LM_API_URL = os.getenv("LM_API_URL", "http://127.0.0.1:1234/v1/chat/completions")


# def query_llm_direct(prompt: str, context: str, temperature=0.7):
#     headers = {"Content-Type": "application/json"}

#     formatted_prompt = format_prompt(prompt)

#     messages = [
#         {"role": "system", "content": prompt_text()},
#         {"role": "user", "content": f"{context}\n\n{formatted_prompt}"}
#     ]

#     payload = {
#         "model": "llama-3.2-1b-instruct",  # or whatever model you’re using
#         "messages": messages,
#         "temperature": temperature
#     }

#     print("📤 Sending request to LM Studio...")

#     response = requests.post(LM_API_URL, headers=headers, json=payload)
#     response.raise_for_status()

#     result = response.json()

#     print("📥 Raw response:", result)

#     if "choices" not in result:
#         raise ValueError(f"Unexpected response format: {result}")

#     return result["choices"][0]["message"]["content"]
