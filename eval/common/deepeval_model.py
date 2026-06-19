from __future__ import annotations

from app.config import AppConfig, load_config

try:
    from deepeval.models import DeepEvalBaseLLM
    from openai import OpenAI

    DEEPEVAL_MODEL_AVAILABLE = True
except Exception:
    DEEPEVAL_MODEL_AVAILABLE = False
    DeepEvalBaseLLM = object  # type: ignore[assignment]
    OpenAI = None  # type: ignore[assignment]


class OpenAICompatibleDeepEvalLLM(DeepEvalBaseLLM):  # type: ignore[misc]
    """DeepEval LLM wrapper backed by workshop LLM_* environment variables."""

    def __init__(self, config: AppConfig) -> None:
        self._config = config
        super().__init__(model=config.llm_model)

    def load_model(self) -> OpenAI:
        return OpenAI(api_key=self._config.llm_api_key, base_url=self._config.llm_api_base)

    def generate(self, prompt: str, schema=None) -> str:  # noqa: ANN001
        response = self.model.chat.completions.create(
            model=self._config.llm_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self._config.llm_temperature,
            max_tokens=self._config.llm_max_tokens,
        )
        content = response.choices[0].message.content
        return (content or "").strip()

    async def a_generate(self, prompt: str, schema=None) -> str:  # noqa: ANN001
        return self.generate(prompt, schema=schema)

    def get_model_name(self) -> str:
        return self._config.llm_model


def build_deepeval_model() -> OpenAICompatibleDeepEvalLLM | None:
    if not DEEPEVAL_MODEL_AVAILABLE:
        return None

    try:
        return OpenAICompatibleDeepEvalLLM(load_config())
    except Exception:
        return None
