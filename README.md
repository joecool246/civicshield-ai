# CivicShield AI

CivicShield AI is a nonpartisan civic technology platform designed to help voters verify political information in the AI era.

## Mission

CivicShield protects voters from AI-driven political misinformation by helping them verify political information, track suspicious political content, and understand civic issues through official, nonpartisan sources.

## Core problem

AI is making political information easier to fake, harder to verify, and harder for voters to trust.

CivicShield aims to become a verification layer between voters and political information.

## Initial scope

The first pilot focuses on an Indiana 2026 MVP.

## Core modules

### Ask CivicShield

An official-source civic assistant that answers election and policy questions using verified sources.

### Check This Post

A tool where users can paste or upload political content and receive a verification-oriented analysis.

### Incident Tracker

A public dashboard of suspicious, misleading, or AI-related political content.

### AI Bias Audit Lab

A later-stage benchmark for auditing how AI systems answer political and civic questions.

## Tech stack

### Frontend

- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui

Location:

apps/web

### Backend

- FastAPI
- Python

Location:

apps/api

### Later

- PostgreSQL
- pgvector
- AI provider abstraction
- Admin review dashboard
- Browser extension
- Public incident database

## Project structure

apps/
  web/
  api/
docs/
  civicshield_spec.json
  phase_1_mvp.md
  phase_2_ai_pipeline.md
  phase_3_admin_dashboard.md
  phase_4_bias_audit_lab.md
packages/
  shared/
AGENTS.md
README.md

## Phase 1 goal

Create a runnable MVP with:

- Next.js frontend
- FastAPI backend
- Basic pages
- Mock backend routes
- Frontend connected to backend
- Clean CivicShield branding
- Local setup instructions

## Product principles

- Do not endorse candidates.
- Do not generate voting recommendations.
- Use official sources first.
- Cite sources whenever answering civic questions.
- Show uncertainty clearly.
- Never claim perfect deepfake detection.
- Label content as verified, misleading, disputed, unconfirmed, missing context, or unable to verify.

## Current status

This repo currently contains the project specification and build-phase instructions.

The next step is to build Phase 1.