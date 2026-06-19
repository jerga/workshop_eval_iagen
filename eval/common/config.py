from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EvalThresholds:
    llm_judge_min_score: float = 0.7
    grounding_min_score: float = 0.7


@dataclass
class EvalRuntimeConfig:
    thresholds: EvalThresholds = field(default_factory=EvalThresholds)
