from __future__ import annotations

from eval.common.deepeval_model import build_deepeval_model
from deepeval.metrics import FaithfulnessMetric


def faithfulness_metric(
    threshold: float,
    truths_extraction_limit: int = 4,
) -> FaithfulnessMetric:
    """Construit la metrique Faithfulness pour vérifier l'ancrage au contexte RAG."""
    model = build_deepeval_model()
    return FaithfulnessMetric(
        model=model,
        threshold=threshold,
        truths_extraction_limit=truths_extraction_limit,
        penalize_ambiguous_claims=True,
    )
