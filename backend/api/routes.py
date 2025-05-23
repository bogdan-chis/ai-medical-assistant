from fastapi import APIRouter
from .schemas import RAGRequest
from backend.llm_integration.rag_service import run_rag_pipeline

router = APIRouter()

@router.post("/rag")
def get_rag_response(request: RAGRequest):
    result = run_rag_pipeline(request.query, request.chunks)
    return result