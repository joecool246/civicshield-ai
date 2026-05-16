import re

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.mock_data import INCIDENTS, OFFICIAL_SOURCES
from app.models import AskRequest, AskResponse, CheckRequest, CheckResponse, Incident

STATE_NAMES = {
    "alabama",
    "alaska",
    "arizona",
    "arkansas",
    "california",
    "colorado",
    "connecticut",
    "delaware",
    "florida",
    "georgia",
    "hawaii",
    "idaho",
    "illinois",
    "iowa",
    "kansas",
    "kentucky",
    "louisiana",
    "maine",
    "maryland",
    "massachusetts",
    "michigan",
    "minnesota",
    "mississippi",
    "missouri",
    "montana",
    "nebraska",
    "nevada",
    "new hampshire",
    "new jersey",
    "new mexico",
    "new york",
    "north carolina",
    "north dakota",
    "ohio",
    "oklahoma",
    "oregon",
    "pennsylvania",
    "rhode island",
    "south carolina",
    "south dakota",
    "tennessee",
    "texas",
    "utah",
    "vermont",
    "virginia",
    "washington",
    "west virginia",
    "wisconsin",
    "wyoming",
}
VOTING_TERMS = ("register", "registration", "vote", "voting", "polling", "id")


def mentions_term(text: str, terms: tuple[str, ...]) -> bool:
    return any(re.search(rf"\b{re.escape(term)}\b", text) for term in terms)


def mentions_state(text: str, states: set[str]) -> bool:
    return any(re.search(rf"\b{re.escape(state)}\b", text) for state in states)


app = FastAPI(
    title="CivicShield AI API",
    description="Phase 1 mock API for nonpartisan civic verification workflows.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "civicshield-api"}


@app.post("/api/ask", response_model=AskResponse)
def ask_civicshield(payload: AskRequest) -> AskResponse:
    question = payload.question.strip()
    lowered = question.lower()
    mentions_indiana = mentions_state(lowered, {"indiana"})
    mentions_other_state = mentions_state(lowered, STATE_NAMES)

    if mentions_other_state:
        return AskResponse(
            answer=(
                "Phase 1 currently only includes Indiana mock source coverage. "
                "I cannot verify this question from the current trusted source set."
            ),
            status="unable_to_verify",
            confidence="low",
            sources=[],
            note="CivicShield has not expanded Phase 1 mock coverage beyond Indiana.",
            suggested_next_steps=[
                "Check your state's official election website or Vote.gov for current voting information.",
            ],
        )

    if any(term in lowered for term in ["who should i vote", "endorse", "best candidate"]):
        return AskResponse(
            answer=(
                "CivicShield does not endorse candidates or provide voting recommendations. "
                "It can help you find official election information and compare source-backed facts."
            ),
            status="unable_to_verify",
            confidence="high",
            sources=OFFICIAL_SOURCES if mentions_indiana else [],
            note="Candidate preference questions are outside CivicShield's nonpartisan scope.",
            suggested_next_steps=[
                "Use official election sources to compare factual candidate and ballot information.",
            ],
        )

    if mentions_term(lowered, VOTING_TERMS):
        if mentions_indiana:
            return AskResponse(
                answer=(
                    "For Indiana voting questions, start with the Indiana Voters Portal and Vote.gov. "
                    "This Phase 1 response is a mock answer and should be checked against the cited official sources."
                ),
                status="verified",
                confidence="medium",
                sources=OFFICIAL_SOURCES,
                note="Phase 1 uses mock source-grounded answers, not live retrieval.",
                suggested_next_steps=[
                    "Confirm details through the Indiana Voters Portal or Vote.gov before acting.",
                ],
            )

        return AskResponse(
            answer=(
                "Phase 1 currently only includes Indiana mock source coverage. "
                "I cannot verify this question from the current trusted source set."
            ),
            status="unable_to_verify",
            confidence="low",
            sources=[],
            note="Ask about Indiana voting information to use the current Phase 1 mock source coverage.",
            suggested_next_steps=[
                "Check your state's official election website or Vote.gov for current voting information.",
            ],
        )

    return AskResponse(
        answer=(
            "CivicShield could not verify this question from the Phase 1 mock source set. "
            "Try asking about voter registration, polling places, voter ID, or another official election process."
        ),
        status="unable_to_verify",
        confidence="low",
        sources=[],
        note="No trusted source in the mock dataset supports a direct answer.",
        suggested_next_steps=[
            "Check your state's official election website or Vote.gov for current voting information.",
        ],
    )


@app.post("/api/check", response_model=CheckResponse)
def check_this_post(payload: CheckRequest) -> CheckResponse:
    content = payload.content.strip()
    lowered = content.lower()

    status = "unconfirmed"
    risk = "medium"
    topic = "Political claim"
    explanation = (
        "This mock review cannot verify the claim from the Phase 1 dataset. "
        "Treat it as unconfirmed until an official or primary source supports it."
    )
    next_steps = [
        "Look for an official election office, agency, court, or campaign source.",
        "Check whether the original post includes date, location, sponsor, and full context.",
        "Avoid sharing high-impact voting claims until they are verified.",
    ]

    if any(term in lowered for term in ["polling place", "polls closed", "registration deadline"]):
        topic = "Voting information"
        risk = "high"
        explanation = (
            "Voting process claims can affect voter access. This mock result requires official confirmation "
            "before the claim should be treated as reliable."
        )
    elif any(term in lowered for term in ["ai", "deepfake", "synthetic", "generated"]):
        topic = "AI-generated media"
        status = "missing_context"
        explanation = (
            "The post mentions possible AI-generated content, but CivicShield does not claim perfect detection. "
            "The original file, disclosure, and source context would be needed."
        )
    elif any(term in lowered for term in ["according to", "source:", "official"]):
        status = "missing_context"
        risk = "low"
        explanation = (
            "The post references a source, but this mock checker still needs the original official link "
            "or document before marking the claim verified."
        )

    return CheckResponse(
        claim_text=content,
        topic=topic,
        verification_status=status,
        ai_disclosure_status="ai_unclear",
        sponsor_status="sponsor_unclear",
        risk_level=risk,
        confidence="low" if status == "unconfirmed" else "medium",
        explanation=explanation,
        suggested_next_steps=next_steps,
        sources=OFFICIAL_SOURCES if topic == "Voting information" else [],
    )


@app.get("/api/incidents", response_model=list[Incident])
def list_incidents():
    return INCIDENTS


@app.get("/api/incidents/{incident_id}", response_model=Incident)
def get_incident(incident_id: str):
    for incident in INCIDENTS:
        if incident.id == incident_id:
            return incident
    raise HTTPException(status_code=404, detail="Incident not found")
