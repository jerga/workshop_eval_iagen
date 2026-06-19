from __future__ import annotations

import json
from pathlib import Path


def get_service_status(service_name: str, service_status_file: Path) -> str:
    data = json.loads(service_status_file.read_text(encoding="utf-8"))
    key = service_name.strip().lower()
    status = data.get(key)

    if status is None:
        return (
            f"Service '{service_name}' inconnu. Services disponibles: "
            + ", ".join(sorted(data.keys()))
        )

    return str(status)
