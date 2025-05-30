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
    4) Evaluate faithfulness & toxicity via JudgeService.
       Retry once if faithfulness < threshold OR toxicity > threshold.
    5) Return answer, context_used (List[str]), metrics, regenerated flag, and score.
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

    # 3) Build the generation function
    if not retrieved_chunks:
        logger.info("No provided chunks; retrieving via vectorstore.")
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
            logger.info("Running RetrievalQA chain...")
            out = qa_chain({"query": user_query})
            answer = out["result"]
            docs = out["source_documents"]
            contexts = [d.page_content for d in docs]
            logger.debug("Retrieved %d documents.", len(contexts))
            context_str = format_context_passage(contexts)
            return answer, contexts, context_str

    else:
        logger.info("Using provided chunks (len=%d).", len(retrieved_chunks))
        def _generate() -> Tuple[str, List[str], str]:
            contexts = retrieved_chunks
            context_str = format_context_passage(contexts)
            logger.debug("Formatted provided context passages.")
            llm = _make_llm()
            user_msg = format_prompt(f"{context_str}\n\nQuestion: {user_query}")
            logger.debug("Formatted prompt for LLM call.")
            answer = llm.call_as_llm(messages=[
                {"role": "system", "content": prompt_text()},
                {"role": "user",   "content": user_msg},
            ])
            return answer, contexts, context_str

    # 4) Initialize JudgeService
    judge = JudgeService()
    logger.info("Initialized JudgeService for faithfulness & toxicity.")

    def _evaluate(answer: str, contexts: List[str], context_str: str) -> Tuple[float, Dict[str, float]]:
        """Helper to evaluate metrics and return faithfulness and metrics dict."""
        try:
            faith_score, metrics = judge.evaluate(
                query=user_query,
                context=context_str,
                generation=answer
            )
            tox_score = metrics.get("toxicity", 0.0)
            return faith_score, tox_score, metrics
        except Exception:
            logger.exception("JudgeService evaluation failed.")
            return 0.0, 0.0, {}

    # 5) First generation + evaluation
    answer, contexts, context_str = _generate()
    faith_score, tox_score, metrics = _evaluate(answer, contexts, context_str)
    logger.info("First-pass faithfulness=%.3f, toxicity=%.3f", faith_score, tox_score)

    # 6) Retry if faithfulness below or toxicity above thresholds
    if faith_score < cfg.HALLUCI_THRESHOLD or tox_score > cfg.TOXICITY_THRESHOLD:
        reason = []
        if faith_score < cfg.HALLUCI_THRESHOLD:
            reason.append("faithfulness")
        if tox_score > cfg.TOXICITY_THRESHOLD:
            reason.append("toxicity")
        logger.warning(
            "Metrics %s failed thresholds; retrying.", 
            ",".join(reason)
        )
        answer2, contexts2, context_str2 = _generate()
        faith_score2, tox_score2, metrics2 = _evaluate(answer2, contexts2, context_str2)
        logger.info("Retry-pass faithfulness=%.3f, toxicity=%.3f", faith_score2, tox_score2)
        return {
            "answer":       answer2,
            "context_used": contexts2,
            "metrics":      metrics2,
            "regenerated":  True,
            "score":        faith_score2,
            "first_score":  faith_score,
            "first_toxicity": tox_score
        }

    # 7) Success on first pass
    logger.info(
        "Metrics within thresholds; returning first-pass result.")
    return {
        "answer":       answer,
        "context_used": contexts,
        "metrics":      metrics,
        "regenerated":  False,
        "score":        faith_score
    }
