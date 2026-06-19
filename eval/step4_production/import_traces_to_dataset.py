from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from eval.step4_production.langfuse_integration import LangfuseIntegration


def main() -> int:
    traces_path = Path(__file__).resolve().parent / "traces" / "sample_production_traces.jsonl"
    dataset_name = "it-support-from-traces-v1"

    integration = LangfuseIntegration()
    integration.ensure_dataset(dataset_name, "Dataset derive de traces support IT")

    count = 0
    for line in traces_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue

        record = json.loads(line)
        input_text = str(record.get("question", ""))

        # TODO-STEP4-02: completer la strategie d'extraction expected_output.
        expected_output = ""

        integration.create_dataset_item(
            dataset_name=dataset_name,
            input_text=input_text,
            expected_output=expected_output,
            metadata={
                "trace_id": record.get("trace_id"),
                "source": "sample_production_traces.jsonl",
                "retrieved_document_ids": record.get("retrieved_document_ids", []),
            },
        )
        count += 1

    integration.flush()
    print(f"Traces importees vers dataset Langfuse: {dataset_name} ({count} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
