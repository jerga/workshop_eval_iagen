from __future__ import annotations

import re

from app.config import load_config
from app.embeddings import OpenAICompatibleEmbeddings
from app.llm import OpenAICompatibleLLM
from app.models import AgentResult, ToolCall
from app.prompts import SYSTEM_PROMPT, build_user_prompt
from app.retrieval import SimpleRetriever
from app.tools import get_service_status


class SupportRAGAgent:
    def __init__(self) -> None:
        self.config = load_config()
        self.embeddings = OpenAICompatibleEmbeddings(self.config)
        self.retriever = SimpleRetriever(self.config.knowledge_base_dir, embeddings=self.embeddings)
        self.llm = OpenAICompatibleLLM(self.config)

    @staticmethod
    def _detect_service_name(question: str) -> str | None:
        normalized = question.lower()
        known_services = ["vpn", "email", "wifi"]

        for name in known_services:
            if name in normalized:
                return name

        patterns = [
            r"statut\s+du\s+service\s+([a-z0-9_-]+)",
            r"status\s+of\s+([a-z0-9_-]+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, normalized)
            if match:
                return match.group(1)

        return None

    def answer(self, question: str) -> AgentResult:
        retrieved = self.retriever.search(question, top_k=3)

        tool_calls: list[ToolCall] = []
        service_name = self._detect_service_name(question)
        if service_name is not None:
            tool_result = get_service_status(service_name, self.config.service_status_file)
            tool_calls.append(
                ToolCall(
                    tool_name="get_service_status",
                    arguments={"service_name": service_name},
                    result=tool_result,
                )
            )

        prompt = build_user_prompt(question, retrieved, tool_calls)
        final_answer = self.llm.chat(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ]
        )

        metadata = {
            "question": question,
            "retrieved_document_ids": [item.document.doc_id for item in retrieved],
            "tool_call_count": len(tool_calls),
            "model": self.config.llm_model,
        }

        return AgentResult(
            answer=final_answer,
            retrieved_documents=retrieved,
            tool_calls=tool_calls,
            metadata=metadata,
        )
