from __future__ import annotations

from pathlib import Path

from eval.common.file_utils import read_csv_rows


class DatasetLoader:
    def __init__(self, datasets_dir: Path) -> None:
        self.datasets_dir = datasets_dir

    def load(self, filename: str) -> list[dict[str, str]]:
        return read_csv_rows(self.datasets_dir / filename)
