from typing import Literal

from pydantic import BaseModel, Field


VerificationStatus = Literal[
    "verified",
    "misleading",
    "disputed",
    "unconfirmed",
    "missing_context",
    "unable_to_verify",
]
RiskLevel = Literal["low", "medium", "high", "critical"]
AiDisclosureStatus = Literal[
    "ai_disclosed",
    "ai_not_disclosed",
    "ai_unclear",
    "not_applicable",
]
SponsorStatus = Literal[
    "sponsor_found",
    "sponsor_missing",
    "sponsor_unclear",
    "not_applicable",
]
Confidence = Literal["low", "medium", "high"]


class Source(BaseModel):
    title: str
    url: str
    publisher: str


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)


class AskResponse(BaseModel):
    answer: str
    status: VerificationStatus
    confidence: Confidence
    sources: list[Source]
    note: str
    suggested_next_steps: list[str]


class CheckRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=4000)


class CheckResponse(BaseModel):
    claim_text: str
    topic: str
    jurisdiction: str
    is_voting_related: bool
    verification_status: VerificationStatus
    ai_disclosure_status: AiDisclosureStatus
    sponsor_status: SponsorStatus
    risk_level: RiskLevel
    confidence: Confidence
    explanation: str
    suggested_next_steps: list[str]
    sources: list[Source]


class Incident(BaseModel):
    id: str
    title: str
    incident_type: str
    location: str
    status: VerificationStatus
    risk_level: RiskLevel
    summary: str
    evidence: list[str]
    sources: list[Source]
