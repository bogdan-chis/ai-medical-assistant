from pydantic import BaseModel
from typing import List

class RAGRequest(BaseModel):
    query: str
    chunks: List[str] = []