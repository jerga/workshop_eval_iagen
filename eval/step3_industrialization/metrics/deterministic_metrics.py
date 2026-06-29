"""Step 3 - Métrique déterministe (Json correctness).
"""
from __future__ import annotations

from pydantic import BaseModel
from eval.common.deepeval_model import build_deepeval_model
from deepeval.metrics import JsonCorrectnessMetric


# TODO: Définir le modèle Pydantic `ITActionPlan` (déduit des `actual_output` du dataset)
#       puis la fonction `json_correctness_metric(threshold: float) -> JsonCorrectnessMetric`.
