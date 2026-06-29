from __future__ import annotations

from eval.common.deepeval_model import build_deepeval_model
from deepeval.metrics import RoleViolationMetric


def role_violation_metric(threshold: float, role: str) -> RoleViolationMetric:
    """Construit la métrique Role violation avec role cible configurable."""
    model = build_deepeval_model()
    return RoleViolationMetric(
        model=model,
        threshold=threshold,
        role=role,
    )
