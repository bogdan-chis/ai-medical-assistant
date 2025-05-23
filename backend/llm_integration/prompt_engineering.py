def format_prompt(question: str) -> str:
    return f"Answer the following question concisely and factually:\n{question}"

def format_context_passage(passage_list: list) -> str:
    return "\n---\n".join(passage_list)