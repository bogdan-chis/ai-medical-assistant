from backend.embeddings.embeddings import LocalServerEmbeddings
import os
from langchain.vectorstores import Chroma
from backend.data.document_splitter import create_split_documents

def get_vectorstore(split_documents=None, persist_directory="chroma/"):
    embedding = LocalServerEmbeddings(base_url="http://localhost:1234/v1")

    # Check if DB already exists and has data
    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        return Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding
        )

    if split_documents is None:
        raise ValueError("No documents provided and vector store does not exist.")

    vectorstore = Chroma.from_documents(
        documents=split_documents,
        embedding=embedding,
        persist_directory=persist_directory
    )
    vectorstore.persist()
    return vectorstore