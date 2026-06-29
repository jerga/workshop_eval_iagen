"""Step 3 - Métrique outillage (Tool correctness).
"""
from __future__ import annotations
from eval.common.deepeval_model import build_deepeval_model
from deepeval.metrics import ToolCorrectnessMetric
from deepeval.test_case import ToolCallParams


# TODO: Définir la fonction `tool_correctness_metric(threshold: float, should_exact_match: bool = True,
#       should_consider_ordering: bool = False) -> ToolCorrectnessMetric`.
