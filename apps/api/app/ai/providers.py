import os

from app.ai.base import AIProvider
from app.ai.mock_provider import MockAIProvider
from app.ai.openai_provider import OpenAIProviderPlaceholder


def get_ai_provider() -> AIProvider:
    provider = os.getenv("CIVICSHIELD_AI_PROVIDER", "mock").lower()
    if provider == "openai" and os.getenv("OPENAI_API_KEY"):
        return OpenAIProviderPlaceholder()
    return MockAIProvider()
