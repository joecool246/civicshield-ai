# CivicShield AI Build Instructions

You are building CivicShield AI, a nonpartisan civic verification platform.

## Core rule
Build incrementally. Do not attempt to build the entire platform at once.

## Tech stack
- Frontend: Next.js, TypeScript, Tailwind CSS, shadcn/ui
- Backend: FastAPI, Python
- Database: PostgreSQL
- Vector search: pgvector
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

## Build style
- Keep code clean and simple.
- Add comments only where helpful.
- Include setup instructions.
- Include tests for important backend logic.
- Make the MVP runnable locally.