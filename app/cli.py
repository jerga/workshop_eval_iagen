from __future__ import annotations

import argparse
import json
import logging
import os

from dotenv import load_dotenv
from langfuse import get_client

from app.rag_agent import SupportRAGAgent


def _setup_langfuse() -> None:
    """Configure Langfuse uniquement si les cles sont presentes.

    Sans compte ni cles, le tracing est desactive proprement : l'application
    fonctionne normalement et aucune trace n'est envoyee.
    """
    load_dotenv()
    has_keys = bool(
        os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY")
    )
    if has_keys:
        base_url = os.getenv("LANGFUSE_BASE_URL")
        if base_url and not os.getenv("LANGFUSE_HOST"):
            os.environ["LANGFUSE_HOST"] = base_url
    else:
        os.environ.setdefault("LANGFUSE_TRACING_ENABLED", "false")
        logging.getLogger("langfuse").setLevel(logging.ERROR)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Assistant support IT (RAG CLI)")
    parser.add_argument("question", nargs="?", help="Question support IT")
    parser.add_argument(
        "--show-internal",
        action="store_true",
        help="Affiche les metadonnees internes (utile pour debug/evaluation)",
    )
    return parser


def main() -> int:
    _setup_langfuse()
    parser = build_parser()
    args = parser.parse_args()

    agent = SupportRAGAgent()

    try:
        if args.question:
            result = agent.answer(args.question)
            print(result.answer)
            if args.show_internal:
                print("\n--- METADONNEES INTERNES ---")
                print(json.dumps(result.metadata, ensure_ascii=False, indent=2))
            return 0

        print("Mode interactif. Tapez 'exit' pour quitter.")
        while True:
            user_input = input("\nVotre question support IT > ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit"}:
                print("Au revoir.")
                return 0

            result = agent.answer(user_input)
            print("\n" + result.answer)
    finally:
        # En script court, on force l'envoi des traces avant de quitter.
        # Sans cles Langfuse, flush() est un no-op.
        get_client().flush()


if __name__ == "__main__":
    raise SystemExit(main())
