"""Smoke test du step 1 : vérifie que l'agent répond, sans framework d'évaluation.

Principe : pour chaque cas, on lance l'agent et on vérifie que la réponse
contient un mot-clé attendu (matching déterministe, insensible à la casse).
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.rag_agent import SupportRAGAgent


SMOKE_DATASET_PATH = Path(__file__).resolve().parent / "datasets" / "smoke_eval.csv"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def run_case(case_id: str, question: str, expected_contains: str) -> bool:
    # Une instance d'agent par cas (suffisant pour un smoke test).
    agent = SupportRAGAgent()
    result = agent.answer(question)

    # Matching simple : le mot-clé attendu doit apparaître dans la réponse.
    answer_normalized = result.answer.lower()
    expected_normalized = expected_contains.lower()

    ok = expected_normalized in answer_normalized
    status = "OK" if ok else "FAIL"
    print(f"[{status}] {case_id} -> attendu: '{expected_contains}'")
    return ok


def main() -> int:
    rows = load_rows(SMOKE_DATASET_PATH)
    print(f"Cas charges: {len(rows)}")

    success_count = 0
    for row in rows:
        ok = run_case(row["case_id"], row["question"], row["expected_contains"])
        if ok:
            success_count += 1

    print(f"Resultat: {success_count}/{len(rows)} cas OK")
    if success_count == len(rows):
        print("SMOKE EVAL: SUCCESS")
        return 0

    print("SMOKE EVAL: FAILED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
