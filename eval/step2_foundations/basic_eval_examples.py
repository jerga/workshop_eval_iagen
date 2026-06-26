"""Step 2 : deux familles d'évaluation avec DeepEval.

- LLM-as-a-Judge (GEval) : un LLM note la réponse selon un critère libre.
- Grounding (FaithfulnessMetric) : vérifie que la réponse reste fidèle au
  contexte de retrieval (détection d'hallucination).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
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
    # On renvoie aussi le contexte de retrieval : indispensable pour la faithfulness.
    return result.answer, [item.document.content for item in result.retrieved_documents]


def llm_judge_section() -> list[bool]:
    print("\n=== SECTION LLM-AS-A-JUDGE ===")
    model = build_deepeval_model()

    question = "Le VPN est indisponible, que dois-je faire ?"

    answer, _ = get_agent_answer_and_context(question)

    # TODO-01: rendre le prompt du juge plus précis pour qu'il évalue les instructions importantes du prompt système de l'agent
    tone_score = GEval(
        name="ProfessionalTone",
        model=model,
        criteria="La réponse doit garder un ton professionnel...",
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
        threshold=0.5,
    )

    # TODO-02: ajuster la consigne pour vérifier explicitement formule d'intro et formule de conclusion.
    formula_score = GEval(
        name="AnswerStructure",
        model=model,
        criteria=(
            "La réponse doit contenir ..."
        ),
        evaluation_params=[SingleTurnParams.ACTUAL_OUTPUT],
        threshold=0.5,
    )

    case_tone = LLMTestCase(input=question, actual_output=answer)
    case_formula = LLMTestCase(input=question, actual_output=answer)

    tone_result = evaluate(test_cases=[case_tone], metrics=[tone_score], display_config=DisplayConfig(print_results=True))
    formula_result = evaluate(test_cases=[case_formula], metrics=[formula_score], display_config=DisplayConfig(print_results=True))

    tone_ok = bool(tone_result.test_results[0].success)
    formula_ok = bool(formula_result.test_results[0].success)
    return [tone_ok, formula_ok]


def grounding_faithfulness_section() -> list[bool]:
    print("\n=== SECTION GROUNDING / FAITHFULNESS ===")
    model = build_deepeval_model()

    question = "Comment diagnostiquer un incident VPN ?"

    answer, retrieval_context = get_agent_answer_and_context(question)

    # TODO-03: ajuster le seuil de faithfulness selon votre tolerance au risque d'hallucination.
    # threshold = seuil de réussite : le cas passe si le score >= threshold.
    faithfulness_score = FaithfulnessMetric(threshold=0, model=model)

    case = LLMTestCase(input=question, actual_output=answer, retrieval_context=retrieval_context)
    result = evaluate(test_cases=[case], metrics=[faithfulness_score], display_config=DisplayConfig(print_results=True))
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
