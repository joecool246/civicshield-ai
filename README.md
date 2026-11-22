# CivicShield AI — Civic Verification Research Prototype

**A full-stack, nonpartisan civic-information verification prototype with human review workflows.**

**Stack:** Next.js 14, TypeScript, React, Tailwind CSS, FastAPI, Python.  
**Status:** Local research MVP. Uses mock provider responses, seeded audit data, and in-memory review state. **Not a deployed verification service.**

## Why this project matters

CivicShield explores how a civic-information product can separate **claims**, **supporting sources**, **reviewer decisions**, and **public-facing incident summaries**. It favors explicit uncertainty and human oversight rather than presenting an unverified AI judgment as fact.

### Engineering highlights

- Next.js pages for civic Q&A, claim checks, incidents, human review, and a bias-audit lab.
- FastAPI endpoints with typed request and response models.
- Local source lookup and an explicit `unable_to_verify` result when support is missing.
- A review-to-publication workflow for *mock incidents*.
- Python tests covering administrative workflows, audit behavior, and the verification pipeline.

### Try it locally

```bash
# Terminal 1
cd apps/api
python -m venv .venv
# Activate the virtual environment for your OS
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

```bash
# Terminal 2, from the repository root
npm install
npm run dev:web
```

Visit `http://localhost:3000` and explore **Ask**, **Check**, **Admin**, and **Bias Audit**. No API key is needed in the default mock mode.

### Current boundaries

This project **does not yet call a live LLM**, authenticate admins, persist production records, or run real bias evaluations. The source lookup is local keyword search. Results from the bias lab are synthetic demonstrations, **not findings about real models**.

### Next engineering milestones

- Add real provider calls with source-grounded response validation and evaluation fixtures.
- Add authentication, role-based authorization, and persistent records before deploying admin tools.
- Add repeatable frontend/API integration tests and screenshots of the local demo.

---

## Detailed project documentation

# CivicShield AI

**Nonpartisan civic-information verification workbench** · Next.js 14 · TypeScript · FastAPI · Python

CivicShield is a **local MVP** for exploring source-grounded civic answers, structured checks of political claims, human review workflows, and audits of AI responses. It is designed around a principle: **show evidence and uncertainty instead of presenting unverified claims as facts.**

> **Demo boundary:** The current default AI provider is deterministic mock logic. The bias-audit records and incidents are illustrative. This repository does **not** demonstrate real model-bias measurements, real-time misinformation detection, or a production deployment.

## What you can explore

| Workflow | Implementation |
| --- | --- |
| Ask CivicShield | Search locally bundled trusted-source snippets and return source-aware answers or `unable_to_verify` |
| Check This Post | Produce structured labels and supporting context for submitted text |
| Review queue | Inspect mock high-risk claims, add reviewer notes, and update review status |
| Incident publishing | Publish reviewed demo tasks to an in-memory incident feed |
| Bias Audit Lab | Explore seeded *mock* response-risk examples with methodology notes |

The application contains a Next.js frontend (`apps/web`), a FastAPI backend (`apps/api`), and shared civic labels (`packages/shared`). The provider boundary separates local deterministic logic from a future real-model integration.

## Quick start

**Prerequisites:** Node.js 20+, npm 10+, Python 3.11+.

Start the API from the repository root:

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

In another terminal, from the **repository root**:

```powershell
npm install
npm run dev:web
```

Visit **http://localhost:3000**. API health check: **http://localhost:8000/health**. The frontend defaults to `http://localhost:8000` unless `NEXT_PUBLIC_API_URL` is set.

The default `CIVICSHIELD_AI_PROVIDER=mock` requires no external credentials. Do not assume that setting `openai` enables actual OpenAI calls: the provider is currently a placeholder.

## Guided walkthrough

1. Open `/ask` and ask a civic-information question. Inspect whether returned local snippets support the answer.
2. Open `/check` to examine a structured claim-check result.
3. Open `/admin`, review a mock task, change its status, and publish it as a demo incident.
4. Open `/incidents` to see the published in-memory record.
5. Open `/bias-audit` to review seeded audit examples. **These scores are illustrative, not measurements of real models.**

Review state resets on backend restart.

## Architecture and key routes

- `apps/web`: Next.js pages for ask, check, incidents, admin review, methodology, and bias audits.
- `apps/api/app/main.py`: FastAPI routes including `POST /api/ask`, `POST /api/check`, `GET /api/incidents`, `GET /api/admin/review-queue`, and `GET /api/bias-audits`.
- `apps/api/data/trusted_sources`: local source snippets; retrieval is keyword-based, not vector retrieval.
- `packages/shared`: shared data labels.

## Engineering decisions

- The system explicitly distinguishes source evidence from interpretation.
- Unsupported questions should return `unable_to_verify`, not invented citations.
- High-risk mock tasks have a human-review step before publishing.
- AI-provider abstraction allows the application to run locally without paid API calls.

## Limitations and next steps

**Not production-ready:** no authentication/authorization, persistent database, actual model inference, production deployment, or browser extension. In particular, `/admin` and `/api/admin/*` are intentionally unauthenticated in this local demo; **do not expose them publicly**.

Next engineering milestones: add role-based access, persistent review state, real source-grounded model integration with validation, automated tests, and a reproducible evaluation dataset.

## Screenshots / demo

Add screenshots or a short walkthrough recording only after capturing the app running locally. No screenshots or external deployment are claimed here.

**Scope:** educational and experimental nonpartisan software. No electoral endorsements, voting recommendations, or claims that mock bias results describe real-world model behavior.
