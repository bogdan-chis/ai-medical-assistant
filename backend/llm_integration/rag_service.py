import os
from backend.vectorstore.vector_store import get_vectorstore
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from backend.llm_integration.prompt_engineering import prompt_text
from backend.data.document_splitter import create_split_documents

def run_rag_pipeline(user_query: str, retrieved_chunks: list[str] = None):
    custom_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_text()
    )

    persist_directory = "chroma/"
    
    # Load documents only if database doesn't exist
    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        vectorstore = get_vectorstore()
    else:
        split_docs = create_split_documents()
        vectorstore = get_vectorstore(split_docs)

    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",
        model="llama-3.2-1b-instruct",
        temperature=0.7
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={
            "prompt": custom_prompt,
            "document_variable_name": "context"
        },
        return_source_documents=True
    )
    
    result = qa_chain({"query": user_query})

    return {
        "answer": result["result"],
        "context_used": result["source_documents"]
    }
