from __future__ import annotations

import os
from typing import Iterable

from dotenv import load_dotenv


REQUIRED_FOR_APP = [
    "LLM_API_BASE",
    "LLM_API_KEY",
    "LLM_MODEL",
    "LLM_PROVIDER",
    "EMBEDDING_API_BASE",
    "EMBEDDING_API_KEY",
    "EMBEDDING_MODEL",
    "EMBEDDING_PROVIDER",
]

OPTIONAL_LATER = [
    "LANGFUSE_PUBLIC_KEY",
    "LANGFUSE_SECRET_KEY",
    "LANGFUSE_BASE_URL",
]


def _missing(keys: Iterable[str]) -> list[str]:
    return [key for key in keys if not os.getenv(key)]


def main() -> int:
    load_dotenv(override=True)

    missing_app = _missing(REQUIRED_FOR_APP)

    print("=== Verification environnement workshop ===")

    if missing_app:
        print("Variables manquantes (application support):")
        for item in missing_app:
            print(f"- {item}")
    else:
        print("Variables application support: OK")

    missing_optional = _missing(OPTIONAL_LATER)
    if missing_optional:
        print("Variables Langfuse : absentes (mais uniquement nécessaire pour TP 4):")
        for item in missing_optional:
            print(f"- {item}")
    else:
        print("Variables Langfuse: OK")

    provider = os.getenv("LLM_PROVIDER", "")
    embedding_provider = os.getenv("EMBEDDING_PROVIDER", "")

    if provider and provider != "openai_compatible":
        print("Erreur: LLM_PROVIDER doit etre 'openai_compatible'.")
        return 1

    if embedding_provider and embedding_provider != "openai_compatible":
        print("Erreur: EMBEDDING_PROVIDER doit etre 'openai_compatible'.")
        return 1

    has_error = bool(missing_app)
    print("Resultat:", "ECHEC" if has_error else "OK")
    return 1 if has_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
