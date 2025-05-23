### File: backend/test_llm_direct.py
from llm_integration.llm_client import query_llm_direct

def main():
    prompt = "What are the key challenges in applying AI to medical diagnosis?"
    answer = query_llm_direct(prompt)

    print("🔎 Prompt:", prompt)
    print("💬 Answer:", answer)

if __name__ == "__main__":
    main()
