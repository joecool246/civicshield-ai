from app.models import Incident, IncidentCreateRequest, IncidentUpdateRequest, ReviewTask, ReviewUpdateRequest
from app.trusted_sources import search_trusted_sources


def _sources_for(content: str):
    return [source.to_source() for source in search_trusted_sources(content)]


# TODO: Add authentication and role-based access before production.
REVIEW_TASKS: list[ReviewTask] = [
    ReviewTask(
        id="task-001",
        submitted_content=(
            "Viral post claims all Marion County polling places changed on Election Day "
            "and voters should use a spreadsheet instead of the state portal."
        ),
        extracted_claim="Polling places changed on Election Day in Marion County.",
        topic="Polling place claim",
        jurisdiction="Indiana",
        is_voting_related=True,
        suggested_verification_status="unconfirmed",
        suggested_risk_level="high",
        ai_disclosure_status="not_applicable",
        sponsor_status="sponsor_unclear",
        confidence="low",
        sources=_sources_for("Indiana polling place county election office"),
    ),
    ReviewTask(
        id="task-002",
        submitted_content=(
            "A robocall circulating online uses synthetic audio to impersonate a candidate "
            "and tells voters the registration deadline has moved."
        ),
        extracted_claim=(
            "Synthetic audio impersonates a candidate and claims the voter registration deadline changed."
        ),
        topic="Candidate impersonation and voting deadline claim",
        jurisdiction="Indiana",
        is_voting_related=True,
        suggested_verification_status="missing_context",
        suggested_risk_level="critical",
        ai_disclosure_status="ai_unclear",
        sponsor_status="sponsor_missing",
        confidence="low",
        sources=_sources_for("Indiana voter registration deadline election division"),
    ),
    ReviewTask(
        id="task-003",
        submitted_content=(
            "Screenshot claims students are no longer eligible to vote in Indiana unless "
            "they use a campus housing address."
        ),
        extracted_claim="Students face a new Indiana voter eligibility restriction.",
        topic="Voter eligibility claim",
        jurisdiction="Indiana",
        is_voting_related=True,
        suggested_verification_status="unconfirmed",
        suggested_risk_level="high",
        ai_disclosure_status="not_applicable",
        sponsor_status="sponsor_unclear",
        confidence="low",
        sources=_sources_for("Indiana voter registration eligibility"),
    ),
]

PUBLISHED_INCIDENTS: list[Incident] = []


def list_review_tasks() -> list[ReviewTask]:
    return REVIEW_TASKS


def update_review_task(task_id: str, payload: ReviewUpdateRequest) -> ReviewTask | None:
    task = find_review_task(task_id)
    if task is None:
        return None

    update = payload.model_dump(exclude_unset=True)
    for key, value in update.items():
        if value is not None:
            setattr(task, key, value)
    return task


def find_review_task(task_id: str) -> ReviewTask | None:
    for task in REVIEW_TASKS:
        if task.id == task_id:
            return task
    return None


def create_incident_from_task(payload: IncidentCreateRequest) -> Incident | None:
    task = find_review_task(payload.task_id)
    if task is None:
        return None

    incident = Incident(
        id=f"review-{task.id}",
        title=payload.title or task.extracted_claim,
        incident_type=task.topic,
        location=task.jurisdiction,
        status=task.suggested_verification_status,
        risk_level=task.suggested_risk_level,
        summary=payload.summary
        or (
            f"Human review workflow item based on submitted content: {task.submitted_content}"
        ),
        evidence=[
            f"Extracted claim: {task.extracted_claim}",
            f"Reviewer notes: {task.reviewer_notes or 'No reviewer notes yet.'}",
            "Published from mock in-memory admin review workflow.",
        ],
        sources=task.sources,
    )

    existing_index = next(
        (index for index, item in enumerate(PUBLISHED_INCIDENTS) if item.id == incident.id),
        None,
    )
    if existing_index is None:
        PUBLISHED_INCIDENTS.append(incident)
    else:
        PUBLISHED_INCIDENTS[existing_index] = incident

    task.review_status = "published"
    return incident


def update_published_incident(incident_id: str, payload: IncidentUpdateRequest) -> Incident | None:
    for incident in PUBLISHED_INCIDENTS:
        if incident.id == incident_id:
            update = payload.model_dump(exclude_unset=True)
            for key, value in update.items():
                if value is not None:
                    setattr(incident, key, value)
            return incident
    return None
