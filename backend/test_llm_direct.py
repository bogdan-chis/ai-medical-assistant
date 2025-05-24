from llm_integration.llm_client import query_llm_direct
from llm_integration.prompt_engineering import format_context_passage
from vectorstore.vector_store import get_vectorstore
from data.document_splitter import create_split_documents

def main():
    question = "What are the key challenges in applying AI to medical diagnosis?"

    # Step 1: Load vectorstore
    vectorstore = get_vectorstore(create_split_documents())

    # Step 2: Retrieve relevant chunks
    retrieved_docs = vectorstore.as_retriever().get_relevant_documents(question)

    # Step 3: Format the context
    context = format_context_passage([doc.page_content for doc in retrieved_docs])

    # Step 4: Query the LLM
    answer = query_llm_direct(question, context)

    print("🔎 Question:", question)
    print("📚 Retrieved context:", context[:300] + "..." if len(context) > 300 else context)
    print("💬 Answer:", answer)

if __name__ == "__main__":
    main()
