import logging
from typing import Dict, Tuple, Any

from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric, ToxicityMetric, ContextualRelevancyMetric

from backend.config import Settings

# configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JudgeService:
    def __init__(self):
        # Load thresholds and settings
        cfg = Settings()

        # Instantiate only faithfulness and toxicity metrics
        self.metrics: Dict[str, Any] = {
            "faithfulness": FaithfulnessMetric(threshold=cfg.HALLUCI_THRESHOLD),
            "toxicity":    ToxicityMetric(threshold=cfg.TOXICITY_THRESHOLD),
            "contextual_relevancy": ContextualRelevancyMetric(threshold=cfg.RELEVANCY_THRESHOLD)
        }

    def evaluate(
        self,
        query: str,
        context: str,
        generation: str
    ) -> Tuple[float, Dict[str, float]]:
        """
        Evaluate generation on faithfulness and toxicity.
        Returns:
          - primary_score: faithfulness
          - all_scores: dict of metric_name -> score
        """
        all_scores: Dict[str, float] = {}

        # Evaluate each metric
        for name, metric in self.metrics.items():
            tc = LLMTestCase(
                input=query,
                actual_output=generation,
                retrieval_context=[context],
            )
            metric.measure(tc)
            all_scores[name] = metric.score

        # Return faithfulness as primary metric
        primary = all_scores.get("faithfulness", 0.0)
        return primary, all_scores