# backend/llm_integration/rag_service.py

import os
import logging
from typing import List, Optional, Tuple, Any, Dict

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from backend.vectorstore.vector_store import get_vectorstore
from backend.data.document_splitter import create_split_documents
from backend.llm_integration.prompt_engineering import (
    prompt_text,
    format_context_passage,
    format_prompt,
)
from backend.llm_integration.judge_service import JudgeService
from backend.config import Settings

# configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_rag_pipeline(
    user_query: str,
    retrieved_chunks: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    1) Retrieve (or accept) context passages.
    2) Format them and the question via prompt-engineering helpers.
    3) Call the RAG LLM to generate an answer.
    4) Evaluate faithfulness via JudgeService, retry once if below threshold.
    5) Return answer, context_used (List[str]), metrics, regenerated flag, and scores.
    """
    logger.info("Starting RAG pipeline for query: %s", user_query)
    cfg = Settings()

    # 1) System prompt
    system_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_text()
    )
    logger.debug("Loaded system prompt template.")

    # 2) LLM factory
    def _make_llm():
        logger.debug("Creating ChatOpenAI with model %s", cfg.LLM_MAIN_MODEL)
        return ChatOpenAI(
            base_url=cfg.LLM_API_BASE_URL,
            api_key=cfg.LLM_API_KEY,
            model=cfg.LLM_MAIN_MODEL,
            temperature=0.5,
            max_tokens=200,
        )

    # 3) Generate function
    if not retrieved_chunks:
        logger.info("No pre-provided chunks; building/retrieving vectorstore.")
        persist_dir = "chroma/"
        if os.path.exists(persist_dir) and os.listdir(persist_dir):
            vectorstore = get_vectorstore()
            logger.debug("Loaded existing Chroma vectorstore.")
        else:
            split_docs = create_split_documents()
            vectorstore = get_vectorstore(split_docs)
            logger.debug("Created new Chroma vectorstore with split docs.")

        llm = _make_llm()
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            chain_type_kwargs={
                "prompt": system_prompt,
                "document_variable_name": "context",
            },
            return_source_documents=True
        )

        def _generate() -> Tuple[str, List[str], str]:
            logger.info("Running QA chain...")
            out = qa_chain({"query": user_query})
            answer = out["result"]
            docs = out["source_documents"]
            contexts = [d.page_content for d in docs]
            logger.debug("Retrieved %d source documents.", len(contexts))
            context_str = format_context_passage(contexts)
            logger.debug("Formatted context passage: %s", context_str)
            return answer, contexts, context_str

    else:
        logger.info("Using provided retrieved_chunks of length %d.", len(retrieved_chunks))
        def _generate() -> Tuple[str, List[str], str]:
            contexts = retrieved_chunks
            context_str = format_context_passage(contexts)
            logger.debug("Formatted context passage for provided chunks.")
            llm = _make_llm()
            user_msg = format_prompt(f"{context_str}\n\nQuestion: {user_query}")
            logger.debug("Formatted user message: %s", user_msg)
            answer = llm.call_as_llm(messages=[
                {"role": "system", "content": prompt_text()},
                {"role": "user",   "content": user_msg},
            ])
            logger.info("Generated answer using direct LLM call.")
            return answer, contexts, context_str

    # 4) Setup JudgeService
    judge = JudgeService()
    logger.info("Initialized JudgeService.")

    # 5) First pass
    answer, contexts, context_str = _generate()
    logger.info("First pass answer: %s", answer)
    try:
        first_score, first_metrics = judge.evaluate(
            query=user_query,
            context=context_str,
            generation=answer
        )
        logger.info("First pass faithfulness score: %.2f", first_score)
    except Exception:
        logger.exception("JudgeService evaluation failed on first pass.")
        return {
            "answer":       answer,
            "context_used": contexts,
            "metrics":      {},
            "regenerated":  False,
            "warning":      "Evaluation unavailable, returning raw answer"
        }

    # 6) Retry if below threshold
    if first_score < cfg.HALLUCI_THRESHOLD:
        logger.warning(
            "Faithfulness %.2f below threshold %.2f, retrying...",
            first_score, cfg.HALLUCI_THRESHOLD
        )
        try:
            answer2, contexts2, context_str2 = _generate()
            retry_score, retry_metrics = judge.evaluate(
                query=user_query,
                context=context_str2,
                generation=answer2
            )
            logger.info("Retry faithfulness score: %.2f", retry_score)
            return {
                "answer":       answer2,
                "context_used": contexts2,
                "metrics":      retry_metrics,
                "regenerated":  True,
                "first_score":  first_score,
                "retry_score":  retry_score
            }
        except Exception:
            logger.exception("JudgeService retry failed, returning first answer.")
            return {
                "answer":       answer,
                "context_used": contexts,
                "metrics":      {"faithfulness": first_score},
                "regenerated":  False,
                "first_score":  first_score,
                "warning":      "Retry evaluation failed, returned first answer"
            }

    # 7) Success on first pass
    logger.info("Faithfulness above threshold, returning first answer.")
    return {
        "answer":       answer,
        "context_used": contexts,
        "metrics":      first_metrics,
        "regenerated":  False,
        "score":        first_score
    }