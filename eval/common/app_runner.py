from __future__ import annotations

from app.rag_agent import SupportRAGAgent


class AppRunner:
    def __init__(self) -> None:
        self._agent = SupportRAGAgent()

    def run(self, question: str) -> dict[str, object]:
        result = self._agent.answer(question)
        return {
            "answer": result.answer,
            "retrieved_document_ids": [item.document.doc_id for item in result.retrieved_documents],
            "tool_calls": [
                {
                    "tool_name": call.tool_name,
                    "arguments": call.arguments,
                    "result": call.result,
                }
                for call in result.tool_calls
            ],
            "metadata": result.metadata,
        }
