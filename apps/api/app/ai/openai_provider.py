import os

from app.ai.mock_provider import MockAIProvider
from app.models import AskResponse, CheckResponse
from app.trusted_sources import TrustedSource


class OpenAIProviderPlaceholder(MockAIProvider):
    name = "openai-placeholder"

    def __init__(self) -> None:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is required to enable the OpenAI provider.")

    def answer_question(self, question: str, sources: list[TrustedSource]) -> AskResponse:
        response = super().answer_question(question, sources)
        response.note = (
            "OpenAI provider placeholder is enabled, but CivicShield still uses safe mock generation "
            "until a real source-grounded prompt and validation layer are implemented. "
            + response.note
        )
        return response

    def analyze_post(self, content: str, sources: list[TrustedSource]) -> CheckResponse:
        response = super().analyze_post(content, sources)
        response.explanation = (
            "OpenAI provider placeholder is enabled, but CivicShield still returns deterministic structured output. "
            + response.explanation
        )
        return response
