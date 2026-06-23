"""Step 4 (solution) - conversion des traces exportées vers le CSV "judge"."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

DATASETS_DIR = Path(__file__).resolve().parent / "datasets"
INPUT_PATH = DATASETS_DIR / "online_traces.json"
OUTPUT_PATH = DATASETS_DIR / "judge_online_cases.csv"
FIELDNAMES = ["case_id", "input", "actual_output", "trace_id"]

_WHITESPACE_RE = re.compile(r"\s+")


def _normalize_text(text: str) -> str:
    """Met le texte sur une seule ligne en compactant les espaces.

    Les retours à la ligne (\n, \r) et tabulations sont remplacés par un
    espace simple, puis les espaces multiples sont fusionnés. Le quoting CSV
    (gestion des virgules/guillemets) reste assuré par csv.DictWriter.
    """
    return _WHITESPACE_RE.sub(" ", text).strip()


def _as_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return _normalize_text(value)
    return _normalize_text(json.dumps(value, ensure_ascii=False))


def traces_to_rows(traces: list[dict[str, object]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, trace in enumerate(traces, start=1):
        rows.append(
            {
                "case_id": f"online_{index:03d}",
                "input": _as_text(trace.get("input")),
                "actual_output": _as_text(trace.get("output")),
                "trace_id": str(trace.get("trace_id", "")),
            }
        )
    return rows


def convert() -> Path:
    traces = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    rows = traces_to_rows(traces)
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    return OUTPUT_PATH


def main() -> int:
    path = convert()
    print(f"CSV judge écrit -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
