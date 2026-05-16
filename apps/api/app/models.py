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
ReviewStatus = Literal[
    "pending",
    "in_review",
    "approved",
    "rejected",
    "published",
    "needs_more_evidence",
]


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


class ReviewTask(BaseModel):
    id: str
    submitted_content: str
    extracted_claim: str
    topic: str
    jurisdiction: str
    is_voting_related: bool
    suggested_verification_status: VerificationStatus
    suggested_risk_level: RiskLevel
    ai_disclosure_status: AiDisclosureStatus
    sponsor_status: SponsorStatus
    confidence: Confidence
    sources: list[Source]
    reviewer_notes: str = ""
    review_status: ReviewStatus = "pending"


class ReviewUpdateRequest(BaseModel):
    review_status: ReviewStatus | None = None
    reviewer_notes: str | None = None
    suggested_verification_status: VerificationStatus | None = None
    suggested_risk_level: RiskLevel | None = None


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


class IncidentCreateRequest(BaseModel):
    task_id: str
    title: str | None = None
    summary: str | None = None


class IncidentUpdateRequest(BaseModel):
    title: str | None = None
    incident_type: str | None = None
    location: str | None = None
    status: VerificationStatus | None = None
    risk_level: RiskLevel | None = None
    summary: str | None = None
    evidence: list[str] | None = None


class BiasAudit(BaseModel):
    id: str
    model_name: str
    topic: str
    prompt: str
    mock_model_response: str
    source_balance_score: int = Field(..., ge=0, le=100)
    framing_score: int = Field(..., ge=0, le=100)
    symmetry_score: int = Field(..., ge=0, le=100)
    refusal_consistency_score: int = Field(..., ge=0, le=100)
    candidate_neutrality_score: int = Field(..., ge=0, le=100)
    voting_advice_flag: bool
    uncertainty_transparency_score: int = Field(..., ge=0, le=100)
    overall_bias_risk: RiskLevel
    methodology_notes: str
