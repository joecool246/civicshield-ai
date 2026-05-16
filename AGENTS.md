# CivicShield AI Build Instructions

You are building CivicShield AI, a nonpartisan civic verification platform.

## Core rule

Build incrementally. Do not attempt to build the entire platform at once.

## Tech stack

- Frontend: Next.js, TypeScript, Tailwind CSS, shadcn/ui
- Backend: FastAPI, Python
- Database: PostgreSQL later
- Vector search: pgvector later
- Storage placeholder: local first, later Cloudflare R2/S3
- Auth placeholder: no auth for Phase 1 unless needed
- AI placeholder: mock AI responses first, real model integration later

## Product principles

- Do not endorse candidates.
- Do not generate voting recommendations.
- Always cite sources when answering civic questions.
- Use official sources first.
- Show uncertainty clearly.
- Never claim perfect deepfake detection.
- Label content as verified, misleading, disputed, unconfirmed, missing context, or unable to verify.
- Use human review for high-risk political or election claims.
- Separate evidence from interpretation.

## Build style

- Keep code clean and simple.
- Add comments only where helpful.
- Include setup instructions.
- Include tests for important backend logic when relevant.
- Make the MVP runnable locally.
- Use mock data first before adding real AI, databases, auth, or deployment complexity.

## Phase order

1. Build the Phase 1 MVP scaffold.
2. Add AI pipeline and source-grounded assistant.
3. Add admin review dashboard.
4. Add AI bias audit lab.
5. Add browser extension only after the web MVP works.

## Safety and trust

CivicShield should not act like a partisan campaign tool. It should help users verify political information through official sources, public evidence, transparent labels, and uncertainty-aware explanations.