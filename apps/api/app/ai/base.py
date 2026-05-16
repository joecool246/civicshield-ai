from abc import ABC, abstractmethod

from app.models import AskResponse, CheckResponse
from app.trusted_sources import TrustedSource


class AIProvider(ABC):
    name: str

    @abstractmethod
    def answer_question(self, question: str, sources: list[TrustedSource]) -> AskResponse:
        raise NotImplementedError

    @abstractmethod
    def analyze_post(self, content: str, sources: list[TrustedSource]) -> CheckResponse:
        raise NotImplementedError
