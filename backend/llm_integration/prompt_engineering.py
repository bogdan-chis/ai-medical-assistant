def format_prompt(question: str) -> str:
    return f"Answer the following question concisely and factually:\n{question}"

def format_context_passage(passage_list: list) -> str:
    return "\n---\n".join(passage_list)

def prompt_text():
    return """

            You are a doctor specialized in various fields of medicine.

            You will respond concisely, in no more than 3 sentences to the user's question and in a friendly manner.

            You will answer based on the context provided below.

            If the user's question is not related to the context, you will say "I cannot help you with that".

            Answer:
            """.strip()