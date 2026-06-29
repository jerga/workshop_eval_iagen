from __future__ import annotations

from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from eval.solutions.step3.metrics.judge_metrics_solution import (
    correctness_metric,
    tone_metric,
)
from deepeval.dataset import EvaluationDataset
from deepeval import assert_test

DATASET_PATH = (
    PROJECT_ROOT / "eval" / "step3_industrialization" / "datasets" / "judge_cases.csv"
)


def load_judge_dataset() -> EvaluationDataset:
    """Charge le dataset judge depuis CSV avec test cases."""
    dataset = EvaluationDataset()
    dataset.add_test_cases_from_csv_file(
        file_path=str(DATASET_PATH),
        input_col_name="input",
        actual_output_col_name="actual_output",
    )
    return dataset

CORRECTNESS_THRESHOLD = 0.5

@pytest.mark.parametrize("test_case", load_judge_dataset().test_cases)
def test_llm_judge_correctness(test_case):
    """Test LLM-as-a-Judge pour la correction et operationnalite (Support IT)."""
    assert_test(test_case, [correctness_metric(threshold=CORRECTNESS_THRESHOLD)])

TONE_THRESHOLD = 0.5

@pytest.mark.parametrize("test_case", load_judge_dataset().test_cases)
def test_llm_judge_tone(test_case):
    """Test LLM-as-a-Judge pour le ton professionnel."""
    assert_test(test_case, [tone_metric(threshold=TONE_THRESHOLD)])
