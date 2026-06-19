from __future__ import annotations

import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from eval.step4_production.langfuse_integration import LangfuseIntegration


def main() -> int:
    datasets_dir = Path(__file__).resolve().parent / "datasets"
    source_csv = datasets_dir / "local_baseline.csv"

    # TODO-STEP4-01: completer le suffixe du nom dataset (ex: -v1).
    dataset_name = "it-support-baseline-TODO"

    integration = LangfuseIntegration()
    integration.ensure_dataset(dataset_name, "Dataset baseline workshop support IT")

    with source_csv.open("r", encoding="utf-8", newline="") as handle:
        rows = [dict(row) for row in csv.DictReader(handle)]

    for row in rows:
        integration.create_dataset_item(
            dataset_name=dataset_name,
            input_text=row["input"],
            expected_output=row["expected_output"],
            metadata={"case_id": row["case_id"], "source": "local_baseline.csv"},
        )

    integration.flush()
    print(f"Dataset promu vers Langfuse: {dataset_name} ({len(rows)} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
