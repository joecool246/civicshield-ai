# Phase 2: AI Pipeline and Source-Grounded Civic Assistant

## Goal

Add the first AI-assisted workflow for CivicShield while keeping outputs source-grounded and safe.

This phase should improve:

- Ask CivicShield
- Check This Post
- Source retrieval
- Structured AI outputs

## Rules

The AI must not:

- Endorse candidates
- Recommend who to vote for
- Invent sources
- Claim perfect deepfake detection
- Make final high-risk election judgments without review

## Source-grounded assistant

The Ask CivicShield assistant should:

1. Receive a civic question.
2. Search trusted source snippets.
3. Generate an answer only from retrieved sources.
4. Cite sources.
5. Abstain if sources are missing.

If no source supports the answer, return:

Unable to verify from trusted sources.

## Check This Post pipeline

For submitted political content, extract:

- claim_text
- topic
- jurisdiction if available
- political entities
- voting-related risk
- sponsor disclosure status
- AI disclosure status
- verification status
- risk level
- confidence
- explanation
- suggested next steps

## AI provider abstraction

Create an AI service abstraction.

Suggested files:

apps/api/app/ai/base.py
apps/api/app/ai/mock_provider.py
apps/api/app/ai/openai_provider.py

The app should work without an API key using the mock provider.

Use the real provider only when an API key is present.

## Trusted source dataset

Create a small local trusted source dataset first.

Suggested folder:

apps/api/data/trusted_sources/

Add sample source files for:

- Vote.gov
- Indiana Election Division placeholder
- County election office placeholder

## High-risk claims

High-risk claims should create a review task instead of being treated as final.

High-risk triggers include:

- Voting deadline claim
- Polling place claim
- Voter eligibility claim
- Candidate impersonation
- Synthetic audio or video claim
- Election Day misinformation
- Threats or intimidation
- Viral political claim

## Acceptance criteria

- The app runs without real AI keys.
- Mock AI returns structured JSON.
- Ask CivicShield returns source-cited answers.
- Unsupported questions return unable_to_verify.
- High-risk election claims are flagged for review.