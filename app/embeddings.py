from __future__ import annotations

from openai import OpenAI

from app.config import AppConfig


class OpenAICompatibleEmbeddings:
    def __init__(self, config: AppConfig) -> None:
        self._client = OpenAI(api_key=config.embedding_api_key, base_url=config.embedding_api_base)
        self._model = config.embedding_model

    def embed(self, text: str) -> list[float]:
        response = self._client.embeddings.create(model=self._model, input=text)
        return list(response.data[0].embedding)
