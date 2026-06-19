from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from eval.common.app_runner import AppRunner
from eval.solutions.step4.langfuse_integration_solution import LangfuseIntegrationSolution


@dataclass
class VariantResultSolution:
    variant_name: str
    score: float
    total: int
    passed: int


class ExperimentRunnerSolution:
    def __init__(self) -> None:
        self.app = AppRunner()
        self.langfuse = LangfuseIntegrationSolution()

    @staticmethod
    def _load_cases(csv_path: Path) -> list[dict[str, str]]:
        with csv_path.open("r", encoding="utf-8", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]

    def _run_variant(
        self,
        variant_name: str,
        dataset_path: Path,
        instruction: str,
    ) -> VariantResultSolution:
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
        return VariantResultSolution(variant_name=variant_name, score=score, total=total, passed=passed)

    def run(self, baseline_csv: Path, variant_csv: Path) -> tuple[VariantResultSolution, VariantResultSolution]:
        baseline_result = self._run_variant("baseline", baseline_csv, "")
        variant_instruction = "Repondez en 2 phrases maximum, avec une action immediate et un ton professionnel."
        variant_result = self._run_variant("variant", variant_csv, variant_instruction)
        self.langfuse.flush()
        return baseline_result, variant_result


def main() -> int:
    datasets_dir = PROJECT_ROOT / "eval" / "step4_production" / "datasets"
    baseline_csv = datasets_dir / "local_baseline.csv"
    variant_csv = datasets_dir / "local_variant.csv"

    runner = ExperimentRunnerSolution()
    baseline_result, variant_result = runner.run(baseline_csv, variant_csv)

    print("=== Step4 Experiment Solution ===")
    print(f"Baseline: {baseline_result.passed}/{baseline_result.total} ({baseline_result.score:.2%})")
    print(f"Variant : {variant_result.passed}/{variant_result.total} ({variant_result.score:.2%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
