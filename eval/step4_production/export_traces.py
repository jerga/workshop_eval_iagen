"""Step 4 - export des traces Langfuse vers un fichier local (JSON).

Cas d'usage : récupérer en local quelques vraies traces de production
(notre "dataset en ligne") pour les évaluer ensuite hors-ligne.

Le code est volontairement minimal : on liste les dernières observations
racines de l'agent (une par trace) et on garde l'essentiel (id, entrée, sortie).
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv
from langfuse import Langfuse

TRACE_NAME = "support-rag-agent"
EXPORT_LIMIT = 3
LOOKBACK = timedelta(days=7)
OUTPUT_PATH = Path(__file__).resolve().parent / "datasets" / "online_traces.json"


def build_client() -> Langfuse:
    """Client Langfuse configuré depuis le .env (LANGFUSE_BASE_URL)."""
    load_dotenv(override=True)
    return Langfuse(
        public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
        secret_key=os.environ["LANGFUSE_SECRET_KEY"],
        base_url=os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com"),
    )


def export_traces() -> list[dict[str, object]]:
    client = build_client()
    now = datetime.now(timezone.utc)
    # Résultats triés par start_time décroissant : les N plus récents.
    response = client.api.observations.get_many(
        name=TRACE_NAME,
        fields="core,basic,io",
        from_start_time=now - LOOKBACK,
        to_start_time=now,
        limit=EXPORT_LIMIT,
    )

    traces = [
        {
            "trace_id": item.trace_id,
            "timestamp": str(item.start_time),
            "input": item.input,
            "output": item.output,
        }
        for item in response.data
        if item.parent_observation_id is None
    ]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(traces, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return traces


def main() -> int:
    traces = export_traces()
    print(f"{len(traces)} trace(s) exportée(s) -> {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
