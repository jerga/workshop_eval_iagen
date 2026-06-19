from __future__ import annotations

import json
import re

from app.config import load_config
from app.llm import OpenAICompatibleLLM

try:
    # DeepEval reste visible pour la pedagogie, meme si le fallback est utilise.
    from deepeval.metrics import AnswerRelevancyMetric  # type: ignore

    DEEPEVAL_AVAILABLE = True
except Exception:
    DEEPEVAL_AVAILABLE = False


def _parse_json_object(raw_text: str) -> dict[str, object]:
    text = raw_text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json\n", "", 1).strip()

    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{[\s\S]*\}", raw_text)
    if not match:
        raise ValueError("Reponse JSON attendue du juge LLM.")
    return json.loads(match.group(0))


class DeepEvalClient:
    def __init__(self) -> None:
        self._llm = OpenAICompatibleLLM(load_config())

    def llm_judge(self, question: str, expected_answer: str, candidate_answer: str) -> dict[str, float]:
        prompt = f"""
Vous etes juge de qualite pour support IT.
Question: {question}
Reference: {expected_answer}
Reponse candidate: {candidate_answer}

Retournez STRICTEMENT un JSON:
{{
  "accuracy": 0.0,
  "completeness": 0.0,
  "clarity": 0.0,
  "tone_professional_and_vous": 0.0
}}
""".strip()

        raw = self._llm.chat(
            [
                {"role": "system", "content": "Retournez uniquement du JSON valide."},
                {"role": "user", "content": prompt},
            ]
        )
        parsed = _parse_json_object(raw)
        return {
            "accuracy": float(parsed.get("accuracy", 0.0)),
            "completeness": float(parsed.get("completeness", 0.0)),
            "clarity": float(parsed.get("clarity", 0.0)),
            "tone_professional_and_vous": float(parsed.get("tone_professional_and_vous", 0.0)),
        }

    def grounding_scores(self, answer: str, expected_answer: str, retrieved_document_ids: list[str]) -> dict[str, float]:
        answer_text = answer.lower()
        expected_text = expected_answer.lower()

        answer_correctness = 1.0 if any(token in answer_text for token in expected_text.split()[:4]) else 0.5
        faithfulness = 1.0 if bool(retrieved_document_ids) else 0.3
        contextual_relevancy = 1.0 if any(token in answer_text for token in ["vpn", "wifi", "mfa", "email"]) else 0.4

        if DEEPEVAL_AVAILABLE:
            # Point d'ancrage pedagogique DeepEval visible.
            try:
                _ = AnswerRelevancyMetric(threshold=0.5)
            except Exception:
                pass

        return {
            "answer_correctness": answer_correctness,
            "faithfulness": faithfulness,
            "contextual_relevancy": contextual_relevancy,
        }
