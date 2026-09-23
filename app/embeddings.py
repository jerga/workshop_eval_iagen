from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import closing
from pathlib import Path

from openai import OpenAI

from app.config import AppConfig


class OpenAICompatibleEmbeddings:
    def __init__(self, config: AppConfig) -> None:
        self._client = OpenAI(api_key=config.embedding_api_key, base_url=config.embedding_api_base)
        self._model = config.embedding_model

    def embed(self, text: str) -> list[float]:
        response = self._client.embeddings.create(model=self._model, input=text)
        return list(response.data[0].embedding)


class EmbeddingCacheError(RuntimeError):
    pass


class DocumentEmbeddingCache:
    def __init__(self, path: Path, config: AppConfig) -> None:
        self._path = path
        self._identity = (
            config.embedding_provider,
            config.embedding_api_base,
            config.embedding_model,
        )
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with closing(sqlite3.connect(path)) as connection:
                with connection:
                    connection.execute(
                        "CREATE TABLE IF NOT EXISTS embeddings (key TEXT PRIMARY KEY, vector TEXT NOT NULL)"
                    )
        except (OSError, sqlite3.Error) as exc:
            raise EmbeddingCacheError(f"Impossible d'initialiser le cache d'embeddings: {path}") from exc

    def get_or_embed(self, text: str, embeddings: OpenAICompatibleEmbeddings) -> list[float]:
        key = hashlib.sha256(
            json.dumps((*self._identity, text), ensure_ascii=False).encode("utf-8")
        ).hexdigest()
        try:
            with closing(sqlite3.connect(self._path)) as connection:
                row = connection.execute("SELECT vector FROM embeddings WHERE key = ?", (key,)).fetchone()
        except (OSError, sqlite3.Error) as exc:
            raise EmbeddingCacheError(f"Impossible de lire le cache d'embeddings: {self._path}") from exc

        if row is not None:
            try:
                vector = json.loads(row[0])
                if not isinstance(vector, list) or not vector or not all(
                    isinstance(value, (int, float)) for value in vector
                ):
                    raise ValueError("Vecteur invalide")
                return vector
            except (ValueError, TypeError) as exc:
                raise EmbeddingCacheError(f"Vecteur corrompu dans le cache d'embeddings: {self._path}") from exc

        vector = embeddings.embed(text)
        try:
            with closing(sqlite3.connect(self._path)) as connection:
                with connection:
                    connection.execute(
                        "INSERT OR IGNORE INTO embeddings (key, vector) VALUES (?, ?)",
                        (key, json.dumps(vector)),
                    )
        except (OSError, sqlite3.Error) as exc:
            raise EmbeddingCacheError(f"Impossible d'ecrire le cache d'embeddings: {self._path}") from exc
        return vector
