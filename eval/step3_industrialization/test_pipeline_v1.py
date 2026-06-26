"""Step 3 - pipeline v1 : premier test pytest + DeepEval, juge "correctness" seul.

Le dataset CSV est transformé en test cases ; chaque cas devient un test
paramétré. assert_test échoue si la valeur du score passe sous le seuil.
"""
from __future__ import annotations
from pathlib import Path
import sys
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from eval.common.deepeval_model import build_deepeval_model
from deepeval.dataset import EvaluationDataset
from deepeval.metrics import GEval
from deepeval.test_case import SingleTurnParams
from deepeval import assert_test

DATASET_PATH = (PROJECT_ROOT / "eval" / "step3_industrialization" / "datasets" / "judge_cases.csv")


def load_judge_dataset() -> EvaluationDataset:
    """Charge le dataset judge depuis CSV avec test cases."""
    dataset = EvaluationDataset()
    # TODO: Charger les test cases depuis le CSV judge_cases.csv, DATASET_PATH est déjà défini.

    return dataset


@pytest.mark.parametrize("test_case", load_judge_dataset().test_cases)
def test_llm_judge_correctness(test_case):
    """Test LLM-as-a-Judge pour la correction et opérationnalité (Support IT)."""
    model = build_deepeval_model()
    correctness_score = GEval(
        name="CorrectnessSupportIT",
        criteria=(
            "Vérifie que la réponse est correcte et opérationnelle pour un contexte "
            "de support IT, avec des actions utiles et sans contradiction."
        ),
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
        model=model,
        # TODO: Definir un threshold adapté au niveau d'exigence souhaité.
    )
    assert_test(test_case, [correctness_score])

