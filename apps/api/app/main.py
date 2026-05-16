from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.ai.providers import get_ai_provider
from app.mock_data import INCIDENTS
from app.models import AskRequest, AskResponse, CheckRequest, CheckResponse, Incident
from app.trusted_sources import search_trusted_sources


app = FastAPI(
    title="CivicShield AI API",
    description="Phase 2 AI-ready API for nonpartisan civic verification workflows.",
    version="0.2.0",
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
    return {"status": "ok", "service": "civicshield-api", "phase": "2"}


@app.post("/api/ask", response_model=AskResponse)
def ask_civicshield(payload: AskRequest) -> AskResponse:
    question = payload.question.strip()
    provider = get_ai_provider()
    sources = search_trusted_sources(question)
    return provider.answer_question(question, sources)


@app.post("/api/check", response_model=CheckResponse)
def check_this_post(payload: CheckRequest) -> CheckResponse:
    content = payload.content.strip()
    provider = get_ai_provider()
    sources = search_trusted_sources(content)
    return provider.analyze_post(content, sources)


@app.get("/api/incidents", response_model=list[Incident])
def list_incidents():
    return INCIDENTS


@app.get("/api/incidents/{incident_id}", response_model=Incident)
def get_incident(incident_id: str):
    for incident in INCIDENTS:
        if incident.id == incident_id:
            return incident
    raise HTTPException(status_code=404, detail="Incident not found")
