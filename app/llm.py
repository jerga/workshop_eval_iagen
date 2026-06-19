from __future__ import annotations

from openai import OpenAI

from app.config import AppConfig


class OpenAICompatibleLLM:
    def __init__(self, config: AppConfig) -> None:
        self._client = OpenAI(api_key=config.llm_api_key, base_url=config.llm_api_base)
        self._model = config.llm_model
        self._temperature = config.llm_temperature
        self._max_tokens = config.llm_max_tokens

    def chat(self, messages: list[dict[str, str]]) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
        )
        content = response.choices[0].message.content
        return (content or "").strip()
