from vectorstore import get_vectorstore
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from prompt_engineering import prompt_text

def run_rag_pipeline(user_query: str, retrieved_chunks: list[str] = None):
    custom_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_text()
    )
    vectorstore = get_vectorstore()

    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",
        model="llama-3.2-1b-instruct",
        temperature=0.7
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": custom_prompt},
        return_source_documents=True
    )
    
    result = qa_chain({"query": user_query})

    return {
        "answer": result["result"],
        "context_used": result["source_documents"]
    }
