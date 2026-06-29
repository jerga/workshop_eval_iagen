"""Step 4 (solution) - éval Judge en ligne + remontée des scores Langfuse."""
from __future__ import annotations

import csv
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from deepeval.test_case import LLMTestCase
from langfuse import Langfuse

from eval.solutions.step4.judge_metrics_solution import (
    build_correctness_metric,
    build_tone_metric,
)

DATASET_PATH = Path(__file__).resolve().parent / "datasets" / "judge_online_cases.csv"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def build_langfuse_client() -> Langfuse | None:
    load_dotenv(override=True)
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    if not public_key or not secret_key:
        return None
    return Langfuse(
        public_key=public_key,
        secret_key=secret_key,
        host=os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com"),
    )


def run() -> int:
    rows = load_rows(DATASET_PATH)
    correctness_score = build_correctness_metric()
    tone_score = build_tone_metric()
    client = build_langfuse_client()

    pushed = 0
    print(f"=== Éval Judge en ligne ({len(rows)} cas) ===")

    for row in rows:
        test_case = LLMTestCase(
            input=row["input"],
            actual_output=row["actual_output"],
        )
        trace_id = (row.get("trace_id") or "").strip()
        print(f"\n[{row.get('case_id', '?')}] trace_id={trace_id or '(aucun)'}")

        for metric in (correctness_score, tone_score):
            metric.measure(test_case)
            score = float(metric.score or 0.0)
            reason = metric.reason or ""
            print(f"  - {metric.name}: {score:.2f}")

            if client and trace_id:
                client.create_score(
                    trace_id=trace_id,
                    name=metric.name,
                    value=score,
                    data_type="NUMERIC",
                    comment=reason,
                )
                pushed += 1

    if client:
        client.flush()

    if pushed:
        print(f"\n{pushed} score(s) remonté(s) dans Langfuse.")
    else:
        print("\nAucun score remonté (clés Langfuse absentes ou trace_id vides).")
    return 0


def main() -> int:
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
