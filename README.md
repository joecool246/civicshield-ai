# CivicShield AI

CivicShield AI is a nonpartisan civic verification platform for helping voters
verify political information in the AI era.

Phase 1 is a local MVP scaffold with mock data only:

- Next.js frontend in `apps/web`
- FastAPI backend in `apps/api`
- Shared civic labels in `packages/shared`
- Basic pages for Home, Ask, Check, Incidents, and Methodology
- Mock API routes for health, civic questions, content checks, and incidents

This phase does not include real AI, a database, authentication, browser
extension, admin dashboard, bias audit lab, or production deployment.

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

## Pages

- `/` explains CivicShield and the Phase 1 mock-data boundary.
- `/ask` lets users submit civic process questions and receive mock source-backed answers.
- `/check` lets users paste political content and receive a mock verification result.
- `/incidents` lists mock incident tracker examples.
- `/incidents/[id]` shows a mock incident detail view.
- `/methodology` explains nonpartisan verification principles and label meanings.

## Product Principles

- Do not endorse candidates.
- Do not generate voting recommendations.
- Use official sources first.
- Cite sources whenever answering civic questions.
- Show uncertainty clearly.
- Never claim perfect deepfake detection.
- Label content as verified, misleading, disputed, unconfirmed, missing context, or unable to verify.
- Separate evidence from interpretation.
- Use human review later for high-risk political or election claims.

## Phase 1 Limitations

- Responses are deterministic mock logic, not real AI.
- Sources are static examples, not live retrieval.
- Incidents are illustrative mock records.
- There is no database, authentication, upload storage, admin review queue, or browser extension.
