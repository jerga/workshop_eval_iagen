"""Step 4 (solution) - export des traces Langfuse vers un JSON local."""
from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langfuse import Langfuse

TRACE_NAME = "support-rag-agent"
EXPORT_LIMIT = 3
OUTPUT_PATH = Path(__file__).resolve().parent / "datasets" / "online_traces.json"


def build_client() -> Langfuse:
    load_dotenv(override=True)
    return Langfuse(
        public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
        secret_key=os.environ["LANGFUSE_SECRET_KEY"],
        host=os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com"),
    )


def export_traces() -> list[dict[str, object]]:
    client = build_client()
    response = client.api.trace.list(name=TRACE_NAME, limit=EXPORT_LIMIT)

    traces = [
        {
            "trace_id": item.id,
            "timestamp": str(item.timestamp),
            "input": item.input,
            "output": item.output,
        }
        for item in response.data
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
