from __future__ import annotations

from datetime import datetime, timezone


def build_trace_record(question: str, app_output: dict[str, object]) -> dict[str, object]:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "question": question,
        "answer": app_output.get("answer", ""),
        "retrieved_document_ids": app_output.get("retrieved_document_ids", []),
        "tool_calls": app_output.get("tool_calls", []),
        "metadata": app_output.get("metadata", {}),
    }
