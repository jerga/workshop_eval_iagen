from __future__ import annotations

import math
from pathlib import Path

from app.embeddings import DocumentEmbeddingCache, EmbeddingCacheError, OpenAICompatibleEmbeddings
from app.models import Document, RetrievedDocument


MIN_COMBINED_SCORE = 0.55
STOP_WORDS = {
    "au", "aux", "avec", "ce", "ces", "comment", "dans", "de", "des", "du",
    "en", "est", "et", "faire", "je", "la", "le", "les", "ma", "mes", "mon",
    "ne", "pas", "pour", "que", "qui", "se", "si", "sur", "un", "une", "vous",
}


class SimpleRetriever:
    def __init__(
        self,
        knowledge_base_dir: Path,
        embeddings: OpenAICompatibleEmbeddings | None = None,
        cache: DocumentEmbeddingCache | None = None,
    ) -> None:
        self._knowledge_base_dir = knowledge_base_dir
        self._embeddings = embeddings
        self._documents = self._load_documents()
        self._document_embeddings: dict[str, list[float]] | None = None
        if embeddings is not None:
            try:
                self._document_embeddings = {
                    doc.doc_id: cache.get_or_embed(doc.content[:1200], embeddings)
                    if cache is not None else embeddings.embed(doc.content[:1200])
                    for doc in self._documents
                }
            except EmbeddingCacheError:
                raise
            except Exception:
                self._document_embeddings = None

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
        return {token for token in cleaned.split() if len(token) > 2 and token not in STOP_WORDS}

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

        if self._embeddings is None or self._document_embeddings is None:
            return [RetrievedDocument(document=doc, score=score) for doc, score in keyword_scored if score > 0][:top_k]

        try:
            query_embedding = self._embeddings.embed(query)
            reranked: list[RetrievedDocument] = []
            for doc, keyword_score in keyword_scored:
                doc_embedding = self._document_embeddings[doc.doc_id]
                semantic_score = self._cosine_similarity(query_embedding, doc_embedding)
                final_score = 0.6 * semantic_score + 0.4 * keyword_score
                reranked.append(RetrievedDocument(document=doc, score=final_score))
            reranked.sort(key=lambda item: item.score, reverse=True)
            return [item for item in reranked if item.score >= MIN_COMBINED_SCORE][:top_k]
        except Exception:
            return [RetrievedDocument(document=doc, score=score) for doc, score in keyword_scored if score > 0][:top_k]
