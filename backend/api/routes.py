# backend/api/routes.py

from fastapi import APIRouter
from .schemas import RAGRequest, RAGResponse
from backend.llm_integration.rag_service import run_rag_pipeline

router = APIRouter()

@router.post("/rag", response_model=RAGResponse)
def get_rag_response(request: RAGRequest):
    """
    Run the RAG + Judge pipeline and return:
     - answer
     - context_used
     - metrics
     - regenerated flag & scores
    """
    result = run_rag_pipeline(request.query, request.chunks)
    return result
