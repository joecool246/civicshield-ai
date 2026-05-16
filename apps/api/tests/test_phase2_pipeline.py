import unittest

from app.ai.mock_provider import MockAIProvider
from app.trusted_sources import search_trusted_sources


class Phase2PipelineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.provider = MockAIProvider()

    def test_indiana_ask_uses_trusted_sources(self) -> None:
        question = "What ID do I need to vote in Indiana?"
        sources = search_trusted_sources(question)
        response = self.provider.answer_question(question, sources)

        self.assertEqual(response.status, "verified")
        self.assertGreater(len(response.sources), 0)
        self.assertTrue(any(source.publisher == "Indiana Secretary of State" for source in response.sources))

    def test_other_state_ask_abstains_without_indiana_sources(self) -> None:
        question = "What ID do I need to vote in Oklahoma?"
        sources = search_trusted_sources(question)
        response = self.provider.answer_question(question, sources)

        self.assertEqual(response.status, "unable_to_verify")
        self.assertEqual(response.confidence, "low")
        self.assertEqual(response.sources, [])

    def test_exact_deadline_question_abstains_without_date_source(self) -> None:
        question = "When is the voter registration deadline in Indiana?"
        sources = search_trusted_sources(question)
        response = self.provider.answer_question(question, sources)

        self.assertEqual(response.status, "unable_to_verify")
        self.assertEqual(response.confidence, "low")
        self.assertEqual(response.sources, [])

    def test_check_post_returns_structured_high_risk_output(self) -> None:
        content = "A viral post says Indiana polling places changed on Election Day."
        sources = search_trusted_sources(content)
        response = self.provider.analyze_post(content, sources)

        self.assertEqual(response.claim_text, content)
        self.assertEqual(response.jurisdiction, "Indiana")
        self.assertTrue(response.is_voting_related)
        self.assertEqual(response.risk_level, "high")
        self.assertIn("human review", response.explanation)


if __name__ == "__main__":
    unittest.main()
