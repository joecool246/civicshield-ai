from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.admin_workflow import (
    PUBLISHED_INCIDENTS,
    create_incident_from_task,
    list_review_tasks,
    update_published_incident,
    update_review_task,
)
from app.ai.providers import get_ai_provider
from app.bias_audits import get_bias_audit, list_bias_audits
from app.mock_data import INCIDENTS
from app.models import (
    AskRequest,
    AskResponse,
    BiasAudit,
    CheckRequest,
    CheckResponse,
    Incident,
    IncidentCreateRequest,
    IncidentUpdateRequest,
    ReviewTask,
    ReviewUpdateRequest,
)
from app.trusted_sources import search_trusted_sources


app = FastAPI(
    title="CivicShield AI API",
    description="Phase 4 API for civic verification, human review, and mock AI bias audits.",
    version="0.4.0",
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
    return {"status": "ok", "service": "civicshield-api", "phase": "4"}


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
    return [*INCIDENTS, *PUBLISHED_INCIDENTS]


@app.get("/api/incidents/{incident_id}", response_model=Incident)
def get_incident(incident_id: str):
    for incident in [*INCIDENTS, *PUBLISHED_INCIDENTS]:
        if incident.id == incident_id:
            return incident
    raise HTTPException(status_code=404, detail="Incident not found")


@app.get("/api/admin/review-queue", response_model=list[ReviewTask])
def get_review_queue():
    return list_review_tasks()


@app.post("/api/admin/review/{task_id}", response_model=ReviewTask)
def review_task(task_id: str, payload: ReviewUpdateRequest):
    updated = update_review_task(task_id, payload)
    if updated is None:
        raise HTTPException(status_code=404, detail="Review task not found")
    return updated


@app.post("/api/admin/incidents", response_model=Incident)
def publish_incident(payload: IncidentCreateRequest):
    incident = create_incident_from_task(payload)
    if incident is None:
        raise HTTPException(status_code=404, detail="Review task not found")
    return incident


@app.patch("/api/admin/incidents/{incident_id}", response_model=Incident)
def patch_incident(incident_id: str, payload: IncidentUpdateRequest):
    incident = update_published_incident(incident_id, payload)
    if incident is None:
        raise HTTPException(status_code=404, detail="Published mock incident not found")
    return incident


@app.get("/api/bias-audits", response_model=list[BiasAudit])
def get_bias_audits():
    return list_bias_audits()


@app.get("/api/bias-audits/{audit_id}", response_model=BiasAudit)
def get_one_bias_audit(audit_id: str):
    audit = get_bias_audit(audit_id)
    if audit is None:
        raise HTTPException(status_code=404, detail="Bias audit not found")
    return audit
