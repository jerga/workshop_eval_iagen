from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from eval.common.app_runner import AppRunner
from eval.step4_production.langfuse_integration import LangfuseIntegration


@dataclass
class VariantResult:
    variant_name: str
    score: float
    total: int
    passed: int


class ExperimentRunner:
    def __init__(self) -> None:
        self.app = AppRunner()
        self.langfuse = LangfuseIntegration()

    @staticmethod
    def _load_cases(csv_path: Path) -> list[dict[str, str]]:
        with csv_path.open("r", encoding="utf-8", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]

    def _run_variant(
        self,
        variant_name: str,
        dataset_path: Path,
        instruction: str,
    ) -> VariantResult:
        rows = self._load_cases(dataset_path)
        passed = 0

        for row in rows:
            question = row["input"]
            expected_contains = row["expected_contains"].lower()

            composed_input = question
            if instruction:
                composed_input = f"{question}\n\nInstruction de variante: {instruction}"

            output = self.app.run(composed_input)
            answer_text = str(output["answer"]).lower()
            ok = expected_contains in answer_text
            if ok:
                passed += 1

            self.langfuse.log_trace(
                name="step4_variant_eval",
                input_text=composed_input,
                output_text=str(output["answer"]),
                metadata={
                    "variant": variant_name,
                    "case_id": row["case_id"],
                    "expected_contains": expected_contains,
                    "passed": ok,
                },
            )

        total = len(rows)
        score = (passed / total) if total else 0.0
        return VariantResult(variant_name=variant_name, score=score, total=total, passed=passed)

    def run(self, baseline_csv: Path, variant_csv: Path) -> tuple[VariantResult, VariantResult]:
        baseline_result = self._run_variant(
            variant_name="baseline",
            dataset_path=baseline_csv,
            instruction="",
        )

        # TODO-STEP4-03: completer l'instruction de la variante.
        variant_instruction = ""
        variant_result = self._run_variant(
            variant_name="variant",
            dataset_path=variant_csv,
            instruction=variant_instruction,
        )

        self.langfuse.flush()
        return baseline_result, variant_result
