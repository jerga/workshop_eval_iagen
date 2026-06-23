"""Step 4 (solution) - métriques LLM-as-a-Judge reprises du TP 3."""
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
    return GEval(
        name="ToneProfessional",
        criteria=(
            "Évalue le ton de manière très exigeante, comme un manager qualité d'un "
            "helpdesk IT premium. Retire des points pour CHACUN de ces éléments : "
            "absence de formule d'accueil personnalisée, absence d'empathie explicite "
            "face au problème de l'utilisateur, ton trop neutre ou robotique, jargon "
            "non explicité, absence de formule de clôture proposant un suivi, "
            "tournures impersonnelles ou directives sèches. Un score élevé doit être "
            "réservé à une réponse chaleureuse, empathique ET parfaitement professionnelle. "
            "Une réponse seulement correcte et polie ne doit pas dépasser la moyenne."
        ),
        evaluation_params=[SingleTurnParams.ACTUAL_OUTPUT],
        model=build_deepeval_model(),
        threshold=threshold,
    )
