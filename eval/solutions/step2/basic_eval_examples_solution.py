from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from eval.common.deepeval_model import build_deepeval_model
from app.rag_agent import SupportRAGAgent

from deepeval import evaluate
from deepeval.evaluate.configs import DisplayConfig
from deepeval.metrics import FaithfulnessMetric, GEval
from deepeval.test_case import LLMTestCase
from deepeval.test_case import SingleTurnParams


def get_agent_answer_and_context(question: str) -> tuple[str, list[str]]:
    agent = SupportRAGAgent()
    result = agent.answer(question)
    return result.answer, [item.document.content for item in result.retrieved_documents]


def llm_judge_section() -> list[bool]:
    print("\n=== SECTION LLM-AS-A-JUDGE ===")
    model = build_deepeval_model()

    question = "Le VPN est indisponible, que dois-je faire ?"

    answer, _ = get_agent_answer_and_context(question)

    # TODO-01 (solution): prompt juge precis pour le ton professionnel en contexte IT.
    tone_metric = GEval(
        name="ProfessionalTone",
        model=model,
        criteria=(
            "La réponse doit être professionnelle, orientée action, concise, "
            "avec un vouvoiement systématique, sans ton familier ni promesse excessive."
        ),
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
        threshold=0.75,
    )

    # TODO-02 (solution): consigne explicite sur formule d'intro et formule de conclusion.
    formula_metric = GEval(
        name="AnswerStructure",
        model=model,
        criteria=(
            "La réponse doit commencer par une formule d'introduction polie (ex: Bonjour) "
            "et terminer par une formule de clôture professionnelle (ex: Cordialement)."
        ),
        evaluation_params=[SingleTurnParams.ACTUAL_OUTPUT],
        threshold=0.8,
    )

    case_tone = LLMTestCase(input=question, actual_output=answer)
    case_formula = LLMTestCase(input=question, actual_output=answer)

    tone_result = evaluate(test_cases=[case_tone], metrics=[tone_metric], display_config=DisplayConfig(print_results=True))
    formula_result = evaluate(test_cases=[case_formula], metrics=[formula_metric], display_config=DisplayConfig(print_results=True))

    tone_ok = bool(tone_result.test_results[0].success)
    formula_ok = bool(formula_result.test_results[0].success)
    return [tone_ok, formula_ok]


def grounding_faithfulness_section() -> list[bool]:
    print("\n=== SECTION GROUNDING / FAITHFULNESS ===")
    model = build_deepeval_model()

    question = "Comment diagnostiquer un incident VPN ?"

    answer, retrieval_context = get_agent_answer_and_context(question)

    # TODO-03 (solution): seuil de faithfulness calibre sur la tolerance au risque d'hallucination.
    faithfulness_metric = FaithfulnessMetric(threshold=0.8, model=model)

    case = LLMTestCase(input=question, actual_output=answer, retrieval_context=retrieval_context)
    result = evaluate(test_cases=[case], metrics=[faithfulness_metric], display_config=DisplayConfig(print_results=True))
    return [bool(result.test_results[0].success)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Step 2 foundations: judge, grounding.")
    parser.add_argument(
        "--section",
        choices=["all", "judge", "grounding"],
        default="all",
        help="Execute une seule section ou tout le script.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    results: list[bool] = []
    if args.section in {"all", "judge"}:
        results.extend(llm_judge_section())
    if args.section in {"all", "grounding"}:
        results.extend(grounding_faithfulness_section())

    passed = sum(1 for item in results if item)
    total = len(results)
    print(f"\nSummary: {passed}/{total} checks OK")
    print("Note: des FAIL sont attendus en workshop pour montrer la valeur de l'evaluation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
