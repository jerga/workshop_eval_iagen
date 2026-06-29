"""Step 3 - pipeline v3 : pipeline complet couvrant les 5 familles de scores
(judge, deterministic, grounding, tooling, safety).

Les sections Deterministic / Grounding / Tooling / Safety sont volontairement
vides : elles sont à compléter en exercice.
"""
from __future__ import annotations

from pathlib import Path
import sys

import pytest
from deepeval.dataset import EvaluationDataset
from deepeval import assert_test

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from eval.step3_industrialization.metrics.judge_metrics import (correctness_metric, tone_metric)

# =============================================================================
# Chargement des datasets
# =============================================================================
DATASET_DIR = PROJECT_ROOT / "eval" / "step3_industrialization" / "datasets"

JUDGE_DATASET_PATH = DATASET_DIR / "judge_cases.csv"
JSON_DATASET_PATH = DATASET_DIR / "json_correctness_cases.csv"
GROUNDING_DATASET_PATH = DATASET_DIR / "grounding_faithfulness_cases.csv"
TOOLING_DATASET_PATH = DATASET_DIR / "tooling_correctness_cases.csv"
SAFETY_DATASET_PATH = DATASET_DIR / "role_violation_cases.csv"


def load_judge_dataset() -> EvaluationDataset:
    """Charge le dataset judge depuis CSV avec test cases."""
    dataset = EvaluationDataset()
    dataset.add_test_cases_from_csv_file(
        file_path=str(JUDGE_DATASET_PATH),
        input_col_name="input",
        actual_output_col_name="actual_output",
    )
    return dataset


def load_json_dataset() -> EvaluationDataset:
    """Charge le dataset JSON correctness depuis CSV avec test cases."""
    dataset = EvaluationDataset()
    dataset.add_test_cases_from_csv_file(
        file_path=str(JSON_DATASET_PATH),
        input_col_name="input",
        actual_output_col_name="actual_output",
    )
    return dataset


def load_grounding_dataset() -> EvaluationDataset:
    """Charge le dataset grounding/faithfulness depuis CSV avec test cases."""
    dataset = EvaluationDataset()
    dataset.add_test_cases_from_csv_file(
        file_path=str(GROUNDING_DATASET_PATH),
        input_col_name="input",
        actual_output_col_name="actual_output",
        retrieval_context_col_name="retrieval_context",
        # Le contexte de retrieval peut contenir plusieurs passages séparés par ";".
        retrieval_context_col_delimiter=";",
    )
    return dataset


def load_tooling_dataset() -> EvaluationDataset:
    """Charge le dataset tooling/tool correctness depuis CSV avec test cases."""
    dataset = EvaluationDataset()
    dataset.add_test_cases_from_csv_file(
        file_path=str(TOOLING_DATASET_PATH),
        input_col_name="input",
        actual_output_col_name="actual_output",
        tools_called_col_name="tools_called",
        expected_tools_col_name="expected_tools",
    )
    return dataset


def load_safety_dataset() -> EvaluationDataset:
    """Charge le dataset safety/role violation depuis CSV avec test cases."""
    dataset = EvaluationDataset()
    dataset.add_test_cases_from_csv_file(
        file_path=str(SAFETY_DATASET_PATH),
        input_col_name="input",
        actual_output_col_name="actual_output",
    )
    return dataset


# =============================================================================
# Evaluations LLM-as-a-Judge
# =============================================================================

CORRECTNESS_THRESHOLD = 0.5


@pytest.mark.parametrize("test_case", load_judge_dataset().test_cases)
def test_llm_judge_correctness(test_case):
    """Test LLM-as-a-Judge pour la correction et opérationnalité (Support IT)."""
    assert_test(test_case, [correctness_metric(threshold=CORRECTNESS_THRESHOLD)])


TONE_THRESHOLD = 0.5


@pytest.mark.parametrize("test_case", load_judge_dataset().test_cases)
def test_llm_judge_tone(test_case):
    """Test LLM-as-a-Judge pour le ton professionnel."""
    assert_test(test_case, [tone_metric(threshold=TONE_THRESHOLD)])


# =============================================================================
# Evaluations Deterministic
# =============================================================================


# =============================================================================
# Evaluations Grounding
# =============================================================================


# =============================================================================
# Evaluations Tooling
# =============================================================================


# =============================================================================
# Evaluations Safety
# =============================================================================