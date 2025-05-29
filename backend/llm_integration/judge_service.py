# backend/llm_integration/judge_service.py

from typing import Dict, Tuple
import importlib

from deepeval.test_case import LLMTestCase
from deepeval.metrics.faithfulness.faithfulness import FaithfulnessMetric
from backend.config import Settings


class JudgeService:
    def __init__(self):
        # Load your hallucinaton threshold from .env via Pydantic
        cfg = Settings()

        # Instantiate a single FaithfulnessMetric.
        # By *not* passing in any model or API keys here, it will use
        # whatever the CLI has already configured via `deepeval set-local-model`.
        self.metric = FaithfulnessMetric(threshold=cfg.HALLUCI_THRESHOLD)

    def evaluate(self, query: str, context: str, generation: str) -> Tuple[float, Dict[str, float]]:
        # Wrap into a DeepEval test case
        tc = LLMTestCase(
            input=query,
            actual_output=generation,
            retrieval_context=[context],
        )

        # Run the metric (talks to your local LLM as per the CLI config)
        self.metric.measure(tc)
        score = self.metric.score

        # Return both the single primary score and the dict
        return score, {"faithfulness": score}
