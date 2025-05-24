import requests
from typing import List
from langchain.embeddings.base import Embeddings

class LocalServerEmbeddings(Embeddings):
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.model = "text-embedding-nomic-embed-text-v1.5"

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        response = requests.post(f"{self.base_url}/embeddings", json={"input": texts})
        data = response.json()

        return [item["embedding"] for item in data["data"]]

    def embed_query(self, text: str) -> List[float]:
        response = requests.post(f"{self.base_url}/embeddings", json={"input": [text]})
        data = response.json()
        return data["data"][0]["embedding"]

embedding = LocalServerEmbeddings(base_url="http://localhost:1234/v1")