def format_prompt(question: str) -> str:
    return f"Answer the following question concisely and factually:\n{question}"

def format_context_passage(passage_list: list) -> str:
    return "\n---\n".join(passage_list)

def prompt_text():
    return """
        Below are examples of how to reason and cite relevant context. Follow their style exactly.
        Example 1:
        Context:
        [1] “Aspirin reduces fever by inhibiting prostaglandin synthesis.”
        [2] “Ibuprofen is also an NSAID used to treat fever.”
        Q: Which mechanism makes aspirin reduce fever?
        A:
        1. Context [1] states aspirin inhibits prostaglandin synthesis.
        2. Context [2] names ibuprofen as another NSAID but says nothing about mechanism.
        Final answer: Aspirin reduces fever by inhibiting prostaglandin synthesis.

        Example 2:
        Context:
        [1] “The standard adult dose of acetaminophen is 500–1000 mg every 4–6 hours.”
        [2] “No more than 4 grams per day to avoid liver toxicity.”
        Q: What is the maximum daily dose of acetaminophen?
        A:
        1. Context [1] gives per-dose limits.
        2. Context [2] directly states the daily limit is 4 g.
        Final answer: The maximum daily dose is 4 grams.

        Now your turn.

        Context:
        {context}

        Question:
        {question}

        Answer (show reasoning steps, cite context IDs, then final answer):
        1.
        2.
        
        Final answer:
        """.strip()

