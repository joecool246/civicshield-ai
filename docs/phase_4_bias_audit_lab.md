# Phase 4: AI Bias Audit Lab

## Goal

Create the first MVP of CivicShield's AI political bias audit lab.

This module tests how AI systems answer political and civic questions.

## Required frontend page

/bias-audit

## Purpose

The bias audit lab should help users understand whether AI systems show problems like:

- Asymmetric framing
- Poor source balance
- Emotional language
- Candidate favoritism
- Refusal inconsistency
- Voting advice risk
- Weak uncertainty disclosure

## Seed audit topics

Create mock or seed audits for:

- Voter ID laws
- Immigration
- Policing
- Climate policy
- Candidate comparison
- Voting advice refusal
- Ballot measure explanation

## Scoring dimensions

Use these dimensions:

- source_balance_score
- framing_score
- symmetry_score
- refusal_consistency_score
- candidate_neutrality_score
- voting_advice_flag
- uncertainty_transparency_score
- overall_bias_risk

## Output

The page should show:

- Model name
- Topic
- Prompt
- Mock model response
- Scores
- Notes
- Overall bias risk

## Methodology

Update the methodology page to explain that:

- Scores are not proof of intentional bias.
- The audit looks for patterns across prompts.
- The system checks framing, source use, refusal behavior, and voting advice.
- Human review is needed before publishing real claims about specific models.

## Acceptance criteria

- /bias-audit page exists.
- It displays mock audit data.
- It explains the scoring dimensions.
- It does not make unsupported claims about real AI systems.