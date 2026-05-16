# CivicShield AI

CivicShield AI is a nonpartisan civic verification platform for helping voters
verify political information in the AI era.

Phase 4 adds a mock AI Bias Audit Lab for studying political AI response risks:

- Next.js frontend in `apps/web`
- FastAPI backend in `apps/api`
- Shared civic labels in `packages/shared`
- AI provider abstraction with a mock provider by default
- Local trusted source snippets in `apps/api/data/trusted_sources`
- Source-grounded Ask CivicShield responses
- Structured Check This Post output
- Admin review queue at `/admin`
- Mock in-memory incident publishing from reviewed tasks
- Bias Audit Lab at `/bias-audit`

This phase does not include a database, authentication, browser extension, real
AI calls, or production deployment.

## Production TODO

TODO: Add authentication and role-based access before production. The `/admin`
page and `/api/admin/*` routes are intentionally unauthenticated for the local
MVP only.

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
- `GET /api/bias-audits`
- `GET /api/bias-audits/{audit_id}`

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

## Test the Bias Audit Lab

1. Start the backend and frontend.
2. Open `http://localhost:3000/bias-audit`.
3. Confirm mock audit rows appear for voter ID laws, immigration, policing,
   climate policy, candidate comparison, voting advice refusal, and ballot
   measure explanation.
4. Confirm each card shows the model name, topic, prompt, mock response, scores,
   voting advice flag, overall risk, and methodology notes.

The audit data is mock-only. Scores are not proof of intentional bias, and
human review is required before publishing real claims about specific models.

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
- `/bias-audit` shows the mock AI political bias audit lab.
- `/methodology` explains nonpartisan verification principles and audit limitations.

## Product Principles

- Do not endorse candidates.
- Do not generate voting recommendations.
- Use official sources first.
- Cite sources whenever answering civic questions.
- Show uncertainty clearly.
- Never claim perfect deepfake or bias detection.
- Do not invent sources.
- Do not claim that real models are biased from mock audit data.
- Label content as verified, misleading, disputed, unconfirmed, missing context, or unable to verify.
- Separate evidence from interpretation.
- Use human review for high-risk political or election claims.

## Phase 4 Limitations

- The default provider is deterministic mock logic, not real AI.
- Bias audit data is seeded mock data and does not evaluate real models.
- Local retrieval is simple keyword matching over JSON files, not vector search.
- The OpenAI provider is a safe placeholder and does not call the OpenAI API yet.
- Review tasks, admin-published incidents, and bias audits are in-memory/mock data only.
- There is no database, authentication, upload storage, browser extension, or production deployment.
