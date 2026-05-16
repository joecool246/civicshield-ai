# Phase 1: CivicShield MVP Scaffold

## Goal

Create the first runnable MVP of CivicShield AI.

This phase should only build the foundation:

- Next.js frontend
- FastAPI backend
- Mock data
- Basic pages
- Backend routes
- Local setup instructions

Do not add real AI, database, auth, browser extension, admin dashboard, bias audit lab, or production deployment yet.

## Required structure

apps/
  web/
  api/
packages/
  shared/
docs/

## Frontend

Build a Next.js + TypeScript app in:

apps/web

Required pages:

- /
- /ask
- /check
- /incidents
- /methodology

The frontend should have clean, nonpartisan CivicShield branding.

Core message:

CivicShield helps voters verify political information in the AI era.

## Backend

Build a FastAPI app in:

apps/api

Required routes:

- GET /health
- POST /api/ask
- POST /api/check
- GET /api/incidents
- GET /api/incidents/{id}

Use mock data only.

## CivicShield labels

Use these labels:

- verified
- misleading
- disputed
- unconfirmed
- missing_context
- unable_to_verify

## Frontend behavior

The homepage should explain:

- What CivicShield is
- Why political information is harder to verify in the AI era
- What users can do with the tool
- That CivicShield is nonpartisan
- That the MVP uses mock data first

The Ask page should include:

- A civic question input
- A mock source-grounded answer
- A source/citation display area
- An unable-to-verify state

The Check page should include:

- A text input for a political claim or post
- A mock result card
- Verification status
- Risk level
- AI disclosure status
- Sponsor status
- Suggested next steps

The Incidents page should include:

- A list of mock incidents
- Status badges
- Risk badges
- A detail view or route for one incident

The Methodology page should explain:

- CivicShield does not endorse candidates
- CivicShield uses official sources first
- CivicShield does not claim perfect deepfake detection
- CivicShield separates verified, misleading, disputed, unconfirmed, missing context, and unable-to-verify labels
- High-risk claims should eventually go through human review

## Acceptance criteria

- Frontend runs locally.
- Backend runs locally.
- Frontend can call backend.
- Homepage explains CivicShield clearly.
- Ask page has a civic question input.
- Check page has a political post/claim input.
- Incidents page shows mock incidents.
- Methodology page explains nonpartisan verification principles.
- README includes setup commands.

## Do not build yet

- Real AI integration
- PostgreSQL
- Authentication
- Browser extension
- Admin dashboard
- Bias audit lab
- Production deployment