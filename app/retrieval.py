from __future__ import annotations

import math
from pathlib import Path

from app.embeddings import OpenAICompatibleEmbeddings
from app.models import Document, RetrievedDocument


class SimpleRetriever:
    def __init__(self, knowledge_base_dir: Path, embeddings: OpenAICompatibleEmbeddings | None = None) -> None:
        self._knowledge_base_dir = knowledge_base_dir
        self._embeddings = embeddings
        self._documents = self._load_documents()

    def _load_documents(self) -> list[Document]:
        docs: list[Document] = []
        for path in sorted(self._knowledge_base_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            title = text.splitlines()[0].replace("#", "").strip() if text.strip() else path.stem
            docs.append(
                Document(
                    doc_id=path.stem,
                    title=title,
                    content=text,
                    source_path=str(path),
                )
            )
        return docs

    @staticmethod
    def _tokenize(value: str) -> set[str]:
        cleaned = (
            value.lower()
            .replace("?", " ")
            .replace("!", " ")
            .replace(",", " ")
            .replace(".", " ")
            .replace(";", " ")
            .replace(":", " ")
        )
        return {token for token in cleaned.split() if len(token) > 2}

    def _keyword_score(self, query: str, content: str) -> float:
        query_tokens = self._tokenize(query)
        content_tokens = self._tokenize(content)
        if not query_tokens or not content_tokens:
            return 0.0
        common = len(query_tokens.intersection(content_tokens))
        return common / len(query_tokens)

    @staticmethod
    def _cosine_similarity(v1: list[float], v2: list[float]) -> float:
        if len(v1) != len(v2) or not v1:
            return 0.0
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def search(self, query: str, top_k: int = 3) -> list[RetrievedDocument]:
        if not self._documents:
            return []

        keyword_scored: list[tuple[Document, float]] = []
        for doc in self._documents:
            score = self._keyword_score(query, doc.content)
            keyword_scored.append((doc, score))

        keyword_scored.sort(key=lambda item: item[1], reverse=True)
        candidates = keyword_scored[: max(top_k * 2, 4)]

        if self._embeddings is None:
            return [RetrievedDocument(document=doc, score=score) for doc, score in candidates[:top_k]]

        try:
            query_embedding = self._embeddings.embed(query)
            reranked: list[RetrievedDocument] = []
            for doc, keyword_score in candidates:
                doc_embedding = self._embeddings.embed(doc.content[:1200])
                semantic_score = self._cosine_similarity(query_embedding, doc_embedding)
                final_score = 0.6 * semantic_score + 0.4 * keyword_score
                reranked.append(RetrievedDocument(document=doc, score=final_score))
            reranked.sort(key=lambda item: item.score, reverse=True)
            return reranked[:top_k]
        except Exception:
            return [RetrievedDocument(document=doc, score=score) for doc, score in candidates[:top_k]]
