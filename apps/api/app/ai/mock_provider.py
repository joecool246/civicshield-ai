import re

from app.ai.base import AIProvider
from app.models import AskResponse, CheckResponse
from app.trusted_sources import TrustedSource, mentions_indiana, mentions_other_state

VOTING_TERMS = ("registration", "register", "vote", "voting", "polling", "ballot", "id")
EXACT_DATE_TERMS = ("deadline", "deadlines", "date", "dates", "when")
HIGH_RISK_TERMS = (
    "deadline",
    "polling place",
    "polls closed",
    "eligibility",
    "eligible",
    "election day",
    "robocall",
    "deepfake",
    "synthetic audio",
    "synthetic video",
    "threat",
    "intimidation",
    "viral",
)


def _has_term(text: str, terms: tuple[str, ...]) -> bool:
    return any(re.search(rf"\b{re.escape(term)}\b", text) for term in terms)


class MockAIProvider(AIProvider):
    name = "mock"

    def answer_question(self, question: str, sources: list[TrustedSource]) -> AskResponse:
        lowered = question.lower()

        if any(term in lowered for term in ["who should i vote", "endorse", "best candidate"]):
            return AskResponse(
                answer=(
                    "CivicShield does not endorse candidates or provide voting recommendations. "
                    "It can help compare source-backed civic facts, but candidate preference questions are outside scope."
                ),
                status="unable_to_verify",
                confidence="high",
                sources=[],
                note="Candidate preference questions are outside CivicShield's nonpartisan scope.",
                suggested_next_steps=[
                    "Use official election sources and nonpartisan voter guides to compare factual ballot information.",
                ],
            )

        if not sources:
            return AskResponse(
                answer=(
                    "Unable to verify from trusted sources. Phase 2 uses only the local trusted source dataset, "
                    "and no retrieved source supports this answer."
                ),
                status="unable_to_verify",
                confidence="low",
                sources=[],
                note="No trusted local source snippet supported a source-grounded answer.",
                suggested_next_steps=[
                    "Check your state's official election website or Vote.gov for current voting information.",
                ],
            )

        if _has_term(lowered, EXACT_DATE_TERMS):
            return AskResponse(
                answer=(
                    "Unable to verify from trusted sources. The local trusted source snippets identify official "
                    "Indiana election resources, but they do not include the current date or deadline needed to "
                    "answer this question."
                ),
                status="unable_to_verify",
                confidence="low",
                sources=[],
                note="The mock provider will not infer current election dates from incomplete source snippets.",
                suggested_next_steps=[
                    "Open the Indiana Voters Portal, Indiana Election Division, or Vote.gov to confirm current dates.",
                ],
            )

        if _has_term(lowered, VOTING_TERMS) and mentions_indiana(lowered):
            source_titles = ", ".join(source.title for source in sources)
            return AskResponse(
                answer=(
                    "For Indiana voting and civic process questions, use the cited official sources to confirm "
                    "the latest details. The retrieved local source snippets point to official Indiana voter "
                    f"resources, including {source_titles}."
                ),
                status="verified",
                confidence="medium",
                sources=[source.to_source() for source in sources],
                note="This is a mock provider response grounded only in retrieved local trusted source snippets.",
                suggested_next_steps=[
                    "Open the cited official source before relying on dates, locations, ID rules, or deadlines.",
                ],
            )

        return AskResponse(
            answer="Unable to verify from trusted sources.",
            status="unable_to_verify",
            confidence="low",
            sources=[],
            note="Retrieved sources did not support a direct answer to this question.",
            suggested_next_steps=[
                "Try a narrower Indiana voting process question or check Vote.gov directly.",
            ],
        )

    def analyze_post(self, content: str, sources: list[TrustedSource]) -> CheckResponse:
        lowered = content.lower()
        is_voting_related = _has_term(lowered, VOTING_TERMS)
        high_risk = _has_term(lowered, HIGH_RISK_TERMS) or is_voting_related
        ai_related = _has_term(lowered, ("ai", "deepfake", "synthetic", "generated"))
        jurisdiction = "Indiana" if mentions_indiana(lowered) else "Unknown"
        if mentions_other_state(lowered):
            jurisdiction = "Outside Indiana"

        topic = "Voting information" if is_voting_related else "Political claim"
        if ai_related:
            topic = "AI-generated or manipulated media"

        verification_status = "unconfirmed"
        if ai_related:
            verification_status = "missing_context"
        elif sources and is_voting_related and jurisdiction == "Indiana":
            verification_status = "missing_context"

        suggested_next_steps = [
            "Find the original post, date, author, and any linked official source.",
            "Compare the claim with official election office sources before sharing.",
        ]
        if high_risk:
            suggested_next_steps.append(
                "Flag for later human review because high-risk election claims should not be treated as final."
            )

        explanation = (
            "This mock Phase 2 analysis extracts structured claim fields and assigns CivicShield labels. "
            "It does not make a final factual ruling unless trusted sources directly support the claim."
        )
        if high_risk:
            explanation += (
                " This item is flagged for later human review because high-risk election claims should "
                "not be treated as final in an automated workflow."
            )

        return CheckResponse(
            claim_text=content,
            topic=topic,
            jurisdiction=jurisdiction,
            is_voting_related=is_voting_related,
            verification_status=verification_status,
            ai_disclosure_status="ai_unclear" if ai_related else "not_applicable",
            sponsor_status="sponsor_unclear",
            risk_level="high" if high_risk else "medium",
            confidence="low",
            explanation=explanation,
            suggested_next_steps=suggested_next_steps,
            sources=[source.to_source() for source in sources],
        )
