# CivicShield AI

CivicShield AI is a nonpartisan civic verification platform for helping voters
verify political information in the AI era.

Phase 2 adds an AI-ready pipeline while keeping the app runnable without real
API keys:

- Next.js frontend in `apps/web`
- FastAPI backend in `apps/api`
- Shared civic labels in `packages/shared`
- AI provider abstraction with a mock provider by default
- OpenAI provider placeholder that only activates when configured with an API key
- Local trusted source snippets in `apps/api/data/trusted_sources`
- Source-grounded Ask CivicShield responses
- Structured Check This Post output

This phase does not include a database, authentication, browser extension, admin
dashboard, bias audit lab, or production deployment.

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

The OpenAI provider is intentionally a placeholder in Phase 2. It only activates
when `OPENAI_API_KEY` is present and still returns deterministic safe output
until a real source-grounded prompt, validation layer, and tests are added.

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
- Do not invent sources.
- Label content as verified, misleading, disputed, unconfirmed, missing context, or unable to verify.
- Separate evidence from interpretation.
- Use human review later for high-risk political or election claims.

## Phase 2 Limitations

- The default provider is deterministic mock logic, not real AI.
- Local retrieval is simple keyword matching over JSON files, not vector search.
- The OpenAI provider is a safe placeholder and does not call the OpenAI API yet.
- Incidents remain illustrative mock records.
- There is no database, authentication, upload storage, admin review queue, or browser extension.
