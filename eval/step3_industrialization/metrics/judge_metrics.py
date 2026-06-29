"""Step 3 - Métriques LLM-as-a-Judge pour évaluation pytest.
"""
from __future__ import annotations

from eval.common.deepeval_model import build_deepeval_model
from deepeval.metrics import GEval
from deepeval.test_case import SingleTurnParams


def correctness_metric(threshold: float) -> GEval:
    """Métrique GEval pour évaluer la correction et l'opérationnalité de la réponse IT."""
    model = build_deepeval_model()

    return GEval(
        name="CorrectnessSupportIT",
        criteria=(
            "Vérifie que la réponse est correcte et opérationnelle pour un contexte "
            "de support IT, avec des actions utiles et sans contradiction évidente."
        ),
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
        model=model,
        threshold=threshold,
    )


def tone_metric(threshold: float) -> GEval:
    """Métrique GEval pour évaluer le ton professionnel."""
    model = build_deepeval_model()
    return GEval(
        name="ToneProfessional",
        criteria=(
            "Évalue le ton de manière très exigeante, comme un manager qualité d'un "
            "helpdesk IT premium. Retire des points pour CHACUN de ces éléments : "
            "absence de formule d'accueil personnalisée, absence d'empathie explicite "
            "face au problème de l'utilisateur, ton trop neutre ou robotique, jargon "
            "excédentaire déroutant pour l'utilisateur, absence d'offre d'escalade "
            "si utile."
        ),
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
        model=model,
        threshold=threshold,
    )
