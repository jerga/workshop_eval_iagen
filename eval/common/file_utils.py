from __future__ import annotations

import csv
from pathlib import Path


def project_root_from(file_path: str) -> Path:
    return Path(file_path).resolve().parents[2]


def read_csv_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]
