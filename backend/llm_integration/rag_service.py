from .llm_client import query_llm
from .prompt_engineering import format_prompt, format_context_passage

def run_rag_pipeline(user_query: str, retrieved_chunks: list[str]):
    prompt = format_prompt(user_query)
    context = format_context_passage(retrieved_chunks)
    answer = query_llm(prompt, context)
    
    return {
        "answer": answer,
        "context_used": retrieved_chunks,
        "prompt": prompt
    }
