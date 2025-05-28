def format_prompt(question: str) -> str:
    return f"Answer the following question concisely and factually:\n{question}"

def format_context_passage(passage_list: list) -> str:
    return "\n---\n".join(passage_list)

def prompt_text():
    return """
        You are a certified medical assistant. Respond strictly based on the provided context.

        INSTRUCTIONS:
        - Only answer if the context supports it directly.
        - KEEP IT SHORT: Respond in **no more than two sentences**.
        - If the input is general (e.g., "hi", "how are you"), reply politely but do NOT give medical advice.
        - If the context does NOT answer the question, say: "I cannot help you with that."

        Context:
        {context}

        Question:
        {question}

        Answer:
        """.strip()

