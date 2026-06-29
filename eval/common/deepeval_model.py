from __future__ import annotations

import os
import threading
import time

from app.config import AppConfig, load_config

try:
    from deepeval.models import DeepEvalBaseLLM
    from openai import OpenAI

    DEEPEVAL_MODEL_AVAILABLE = True
except Exception:
    DEEPEVAL_MODEL_AVAILABLE = False
    DeepEvalBaseLLM = object  # type: ignore[assignment]
    OpenAI = None  # type: ignore[assignment]


def _load_min_interval_s() -> float:
    """Intervalle minimal (en secondes) entre deux appels au LLM juge.

    Throttling désactivé par défaut. Activable via la variable d'environnement
    `DEEPEVAL_LLM_MIN_INTERVAL_S` (ex: `1` pour plafonner à ~1 appel/seconde).
    Une valeur vide, nulle, négative ou invalide désactive le throttling.
    """
    raw = os.getenv("DEEPEVAL_LLM_MIN_INTERVAL_S", "").strip()
    if not raw:
        return 0.0
    try:
        return max(0.0, float(raw))
    except ValueError:
        return 0.0


_MIN_INTERVAL_S = _load_min_interval_s()


class OpenAICompatibleDeepEvalLLM(DeepEvalBaseLLM):  # type: ignore[misc]
    """DeepEval LLM wrapper backed by workshop LLM_* environment variables."""

    # Etat partagé par toutes les instances (une par métrique) pour borner le
    # débit global d'appels LLM lorsque le throttling est activé.
    _rate_lock = threading.Lock()
    _last_call_ts = 0.0

    def __init__(self, config: AppConfig) -> None:
        self._config = config
        super().__init__(model=config.llm_model)

    def _throttle(self) -> None:
        """Espace les appels LLM pour respecter `DEEPEVAL_LLM_MIN_INTERVAL_S`.

        No-op si le throttling est désactivé (intervalle <= 0).
        """
        if _MIN_INTERVAL_S <= 0:
            return
        with OpenAICompatibleDeepEvalLLM._rate_lock:
            elapsed = time.monotonic() - OpenAICompatibleDeepEvalLLM._last_call_ts
            wait = _MIN_INTERVAL_S - elapsed
            if wait > 0:
                time.sleep(wait)
            OpenAICompatibleDeepEvalLLM._last_call_ts = time.monotonic()

    def load_model(self) -> OpenAI:
        return OpenAI(api_key=self._config.llm_api_key, base_url=self._config.llm_api_base)

    def generate(self, prompt: str, schema=None) -> str:  # noqa: ANN001
        self._throttle()
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
