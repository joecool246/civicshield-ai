# CivicShield AI

CivicShield AI is a nonpartisan civic verification platform for helping voters
verify political information in the AI era.

Phase 3 adds a mock human review dashboard so high-risk political and election
claims are not treated as final AI judgments:

- Next.js frontend in `apps/web`
- FastAPI backend in `apps/api`
- Shared civic labels in `packages/shared`
- AI provider abstraction with a mock provider by default
- Local trusted source snippets in `apps/api/data/trusted_sources`
- Source-grounded Ask CivicShield responses
- Structured Check This Post output
- Admin review queue at `/admin`
- Mock in-memory incident publishing from reviewed tasks

This phase does not include a database, authentication, browser extension, bias
audit lab, or production deployment.

## Production TODO

TODO: Add authentication and role-based access before production. The `/admin`
page and `/api/admin/*` routes are intentionally unauthenticated for the local
Phase 3 MVP only.

## Requirements

- Node.js 20 or newer
- npm 10 or newer
- Python 3.11 or newer

## Run the backend

From the repo root:

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Health check:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

Backend routes:

- `GET /health`
- `POST /api/ask`
- `POST /api/check`
- `GET /api/incidents`
- `GET /api/incidents/{id}`
- `GET /api/admin/review-queue`
- `POST /api/admin/review/{task_id}`
- `POST /api/admin/incidents`
- `PATCH /api/admin/incidents/{incident_id}`

## Run the frontend

In a second terminal, from the repo root:

```powershell
npm install
npm run dev:web
```

Open:

```text
http://localhost:3000
```

The frontend reads the API URL from `NEXT_PUBLIC_API_URL`. If unset, it uses:

```text
http://localhost:8000
```

## Test the Admin Dashboard

1. Start the backend and frontend.
2. Open `http://localhost:3000/admin`.
3. Confirm the review queue shows mock high-risk election claims.
4. Add reviewer notes and save them.
5. Change verification status or risk level.
6. Mark a task approved, rejected, or needs more evidence.
7. Click `Publish as incident`.
8. Open `/incidents` and confirm the published mock incident appears.

All review state is in memory and resets when the backend restarts.

## AI Provider Setup

Local development uses the mock provider by default. No API key is required.

```text
CIVICSHIELD_AI_PROVIDER=mock
```

To test the OpenAI placeholder later, set both variables before starting the
backend:

```powershell
$env:CIVICSHIELD_AI_PROVIDER="openai"
$env:OPENAI_API_KEY="your_api_key_here"
uvicorn app.main:app --reload --port 8000
```

The OpenAI provider is intentionally a placeholder. It only activates when
`OPENAI_API_KEY` is present and still returns deterministic safe output until a
real source-grounded prompt, validation layer, and tests are added.

## Trusted Sources

Trusted source snippets live in:

```text
apps/api/data/trusted_sources/
```

Current sample sources include Vote.gov, the Indiana Voters Portal, the Indiana
Election Division, and an Indiana county election office placeholder. Ask
CivicShield retrieves from these local files before answering. If no trusted
source supports the answer, it returns `unable_to_verify`.

## Pages

- `/` explains CivicShield and the mock-data boundary.
- `/ask` lets users submit civic questions and receive source-grounded answers.
- `/check` lets users paste political content and receive structured CivicShield labels.
- `/incidents` lists mock and admin-published incident examples.
- `/incidents/[id]` shows a mock incident detail view.
- `/admin` shows the mock human review queue.
- `/methodology` explains nonpartisan verification principles and label meanings.

## Product Principles

- Do not endorse candidates.
- Do not generate voting recommendations.
- Use official sources first.
- Cite sources whenever answering civic questions.
- Show uncertainty clearly.
- Never claim perfect deepfake detection.
- Do not invent sources.
- Label content as verified, misleading, disputed, unconfirmed, missing context, or unable to verify.
- Separate evidence from interpretation.
- Use human review for high-risk political or election claims.

## Phase 3 Limitations

- The default provider is deterministic mock logic, not real AI.
- Local retrieval is simple keyword matching over JSON files, not vector search.
- The OpenAI provider is a safe placeholder and does not call the OpenAI API yet.
- Review tasks and admin-published incidents are in-memory only.
- There is no database, authentication, upload storage, browser extension, or bias audit lab.
