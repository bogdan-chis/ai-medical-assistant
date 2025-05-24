from embeddings.embeddings import LocalServerEmbeddings
import os
from langchain.vectorstores import Chroma

def get_vectorstore(split_documents, persist_directory="chroma/"):
    embedding = LocalServerEmbeddings(base_url="http://localhost:1234/v1")

    if not os.path.exists(persist_directory):
        vectorstore = Chroma.from_documents(
            documents=split_documents,
            embedding=embedding,
            persist_directory=persist_directory,
        )
        vectorstore.persist()
    else:
        vectorstore = Chroma(
            embedding_function=embedding,
            persist_directory=persist_directory
        )

    return vectorstore