from __future__ import annotations

import pytest

from eval.common.deepeval_model import build_deepeval_model
from deepeval.metrics import GEval
from deepeval.test_case import SingleTurnParams


@pytest.fixture(scope="module")
def correctness_metric() -> GEval:
    """ Metrique GEval pour evaluer la correction et l'opérationnalité de la réponse IT.
        Fixture scope="module" : la métrique est construite une seule fois et réutilisée
        par tous les tests du module.
    """
    model = build_deepeval_model()

    return GEval(
        name="CorrectnessSupportIT",
        criteria=(
            "Vérifie que la réponse est correcte et opérationnelle pour un contexte "
            "de support IT, avec des actions utiles et sans contradiction évidente."
        ),
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
        model=model,
        threshold=0.5,
    )
