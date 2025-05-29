# backend/api/schemas.py

from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class RAGRequest(BaseModel):
    query: str
    chunks: List[str] = []

class RAGResponse(BaseModel):
    # The generated answer
    answer: str
    # The list of context passages actually used
    context_used: List[str]
    # The DeepEval metrics (e.g. faithfulness) -> raw scores
    metrics: Dict[str, float]
    # Whether we triggered a regenerate (due to low faithfulness)
    regenerated: bool
    # The faithfulness score from the first run (if regenerated)
    first_score: Optional[float] = None
    # The faithfulness score after retry (if regenerated)
    retry_score: Optional[float] = None
    # The faithfulness score (if not regenerated)
    score: Optional[float] = None
