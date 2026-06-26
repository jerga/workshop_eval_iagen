from __future__ import annotations

from pydantic import BaseModel

from deepeval.metrics import JsonCorrectnessMetric


class ITActionPlan(BaseModel):
    ticket_id: str
    status: str
    next_step: str


def json_correctness_metric(threshold: float) -> JsonCorrectnessMetric:
    """Construit la métrique Json correctness avec schema attendu configurable."""
    return JsonCorrectnessMetric(
        expected_schema=ITActionPlan,
        threshold=threshold,
        strict_mode=True,
        async_mode=False,
    )
