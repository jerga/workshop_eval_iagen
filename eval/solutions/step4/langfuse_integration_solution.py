from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv
from langfuse import Langfuse


@dataclass
class LangfuseConfigSolution:
    public_key: str
    secret_key: str
    host: str


def load_langfuse_config_solution() -> LangfuseConfigSolution:
    load_dotenv()
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "").strip()
    secret_key = os.getenv("LANGFUSE_SECRET_KEY", "").strip()
    host = os.getenv("LANGFUSE_HOST", "").strip()

    missing: list[str] = []
    if not public_key:
        missing.append("LANGFUSE_PUBLIC_KEY")
    if not secret_key:
        missing.append("LANGFUSE_SECRET_KEY")
    if not host:
        missing.append("LANGFUSE_HOST")

    if missing:
        raise ValueError("Variables Langfuse manquantes: " + ", ".join(missing))

    return LangfuseConfigSolution(public_key=public_key, secret_key=secret_key, host=host)


class LangfuseIntegrationSolution:
    def __init__(self) -> None:
        config = load_langfuse_config_solution()
        self.client = Langfuse(
            public_key=config.public_key,
            secret_key=config.secret_key,
            host=config.host,
        )

    def ensure_dataset(self, dataset_name: str, description: str) -> Any:
        try:
            return self.client.get_dataset(dataset_name)
        except Exception:
            self.client.create_dataset(name=dataset_name, description=description)
            return self.client.get_dataset(dataset_name)

    def create_dataset_item(
        self,
        dataset_name: str,
        input_text: str,
        expected_output: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        dataset = self.ensure_dataset(dataset_name, "Dataset workshop support IT")
        dataset.create_item(
            input=input_text,
            expected_output=expected_output,
            metadata=metadata or {},
        )

    def log_trace(
        self,
        name: str,
        input_text: str,
        output_text: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.client.trace(
            name=name,
            input=input_text,
            output=output_text,
            metadata=metadata or {},
        )

    def flush(self) -> None:
        self.client.flush()
