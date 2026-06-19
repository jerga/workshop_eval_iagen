from __future__ import annotations
from pathlib import Path
import sys
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[3]
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
    dataset.add_test_cases_from_csv_file(
        file_path=str(DATASET_PATH),
        input_col_name="input",
        actual_output_col_name="actual_output",
    )
    return dataset


@pytest.fixture(scope="module")
def correctness_metric():
    """Metrique GEval pour evaluer la correction et l'opérationnalité de la réponse IT."""
    model = build_deepeval_model()

    return GEval(
        name="CorrectnessSupportIT",
        criteria=(
            "Vérifie que la réponse est correcte et opérationnelle pour un contexte "
            "de support IT, avec des actions utiles et sans contradiction."
        ),
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
        model=model,
        threshold=0.5,
    )


@pytest.mark.parametrize("test_case", load_judge_dataset().test_cases)
def test_llm_judge_correctness(test_case, correctness_metric):
    """Test LLM-as-a-Judge pour la correction et opérationnalité (Support IT)."""
    assert_test(test_case, [correctness_metric])

