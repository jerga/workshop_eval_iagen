"""Step 4 - métriques LLM-as-a-Judge reprises du TP 3.

On ne garde que les 2 métriques GEval utilisées au TP 3 :
- CorrectnessSupportIT : correction / opérationnalité de la réponse
- ToneProfessional     : ton professionnel et courtois

Contrairement au TP 3 (fixtures pytest), on expose ici de simples fonctions
de fabrique : le pipeline du step 4 est un script, pas une suite pytest.
"""
from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from deepeval.metrics import GEval
from deepeval.test_case import SingleTurnParams

from eval.common.deepeval_model import build_deepeval_model

CORRECTNESS_THRESHOLD = 0.5
TONE_THRESHOLD = 0.5


def build_correctness_metric(threshold: float = CORRECTNESS_THRESHOLD) -> GEval:
    """Métrique de correction / opérationnalité (Support IT)."""
    return GEval(
        name="CorrectnessSupportIT",
        criteria=(
            "Vérifie que la réponse est correcte et opérationnelle pour un contexte "
            "de support IT, avec des actions utiles et sans contradiction évidente."
        ),
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
        model=build_deepeval_model(),
        threshold=threshold,
    )


def build_tone_metric(threshold: float = TONE_THRESHOLD) -> GEval:
    """Métrique de ton professionnel et courtois."""
    return GEval(
        name="ToneProfessional",
        criteria=(
            "Vérifie un ton professionnel, courtois et adapté pour un helpdesk IT "
            "interne, avec une formulation claire et constructive."
        ),
        evaluation_params=[SingleTurnParams.ACTUAL_OUTPUT],
        model=build_deepeval_model(),
        threshold=threshold,
    )
