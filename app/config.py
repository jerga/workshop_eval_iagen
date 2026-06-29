from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class AppConfig:
    llm_api_base: str
    llm_api_key: str
    llm_model: str
    llm_provider: str
    llm_temperature: float
    llm_max_tokens: int
    embedding_api_base: str
    embedding_api_key: str
    embedding_model: str
    embedding_provider: str
    workshop_debug: bool
    app_dir: Path

    @property
    def knowledge_base_dir(self) -> Path:
        return self.app_dir / "data" / "knowledge_base"

    @property
    def service_status_file(self) -> Path:
        return self.app_dir / "data" / "service_status.json"


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Variable d'environnement manquante: {name}")
    return value


def _as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def load_config() -> AppConfig:
    load_dotenv(override=True)

    llm_provider = _required_env("LLM_PROVIDER")
    embedding_provider = _required_env("EMBEDDING_PROVIDER")

    if llm_provider != "openai_compatible":
        raise ValueError("LLM_PROVIDER doit valoir 'openai_compatible'.")

    if embedding_provider != "openai_compatible":
        raise ValueError("EMBEDDING_PROVIDER doit valoir 'openai_compatible'.")

    app_dir = Path(__file__).resolve().parent

    return AppConfig(
        llm_api_base=_required_env("LLM_API_BASE"),
        llm_api_key=_required_env("LLM_API_KEY"),
        llm_model=_required_env("LLM_MODEL"),
        llm_provider=llm_provider,
        llm_temperature=float(os.getenv("LLM_TEMPERATURE", "1")),
        llm_max_tokens=int(os.getenv("LLM_MAX_TOKENS", "1024")),
        embedding_api_base=_required_env("EMBEDDING_API_BASE"),
        embedding_api_key=_required_env("EMBEDDING_API_KEY"),
        embedding_model=_required_env("EMBEDDING_MODEL"),
        embedding_provider=embedding_provider,
        workshop_debug=_as_bool(os.getenv("WORKSHOP_DEBUG", "false")),
        app_dir=app_dir,
    )
