"""Solution Step 3 - Métriques paramétrisées pour le TP3.

Fixtures pytest paramétrées qui acceptent un seuil (threshold)
configurable pour adapter l'évaluation des métriques GEval
selon les besoins du test.
"""
from __future__ import annotations

import pytest

from eval.common.deepeval_model import build_deepeval_model
from deepeval.metrics import GEval
from deepeval.test_case import SingleTurnParams


@pytest.fixture(scope="module")
def correctness_metric(threshold: float) -> GEval:
    """Métrique GEval pour évaluer la correction et l'opérationnalité de la réponse IT."""
    model = build_deepeval_model()

    return GEval(
        name="CorrectnessSupportIT",
        criteria=(
            "Verifie que la reponse est correcte et operationnelle pour un contexte "
            "de support IT, avec des actions utiles et sans contradiction evidente."
        ),
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
        model=model,
        threshold=threshold,
    )


@pytest.fixture(scope="module")
def tone_metric(threshold: float) -> GEval:
    """Métrique GEval pour évaluer le ton professionnel et courtois."""
    model = build_deepeval_model()

    return GEval(
        name="ToneProfessional",
        criteria=(
            "Verifie un ton professionnel, courtois et appropriate pour un helpdesk IT "
            "interne, avec une formulation claire et constructive."
        ),
        evaluation_params=[SingleTurnParams.ACTUAL_OUTPUT],
        model=model,
        threshold=threshold,
    )