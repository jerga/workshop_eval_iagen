from __future__ import annotations

import argparse
import json

from app.rag_agent import SupportRAGAgent


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
    parser = build_parser()
    args = parser.parse_args()

    agent = SupportRAGAgent()

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


if __name__ == "__main__":
    raise SystemExit(main())
