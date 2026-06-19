from __future__ import annotations

from deepeval.metrics import ToolCorrectnessMetric
from deepeval.test_case import ToolCallParams


def tool_correctness_metric(
    threshold: float,
    should_exact_match: bool = True,
    should_consider_ordering: bool = False,
) -> ToolCorrectnessMetric:
    """Construit la metrique Tool correctness pour valider les outils appeles."""
    return ToolCorrectnessMetric(
        threshold=threshold,
        should_exact_match=should_exact_match,
        should_consider_ordering=should_consider_ordering,
        evaluation_params=[ToolCallParams.NAME, ToolCallParams.INPUT_PARAMETERS],
        async_mode=False,
    )
