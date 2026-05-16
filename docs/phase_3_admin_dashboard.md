# Phase 3: Admin Review Dashboard

## Goal

Create a human review workflow for CivicShield submissions.

This is important because high-risk political and election claims should not be judged by AI alone.

## Required frontend page

/admin

## Required backend routes

- GET /api/admin/review-queue
- POST /api/admin/review/{task_id}
- POST /api/admin/incidents
- PATCH /api/admin/incidents/{incident_id}

## Reviewer actions

A reviewer should be able to:

- View submitted content
- View extracted claims
- View suggested AI labels
- Change verification status
- Change risk level
- Add reviewer notes
- Publish an incident
- Update an existing incident

## Review statuses

Use:

- pending
- in_review
- approved
- rejected
- published
- needs_more_evidence

## High-risk triggers

Create review tasks when content includes:

- Voting deadline claim
- Polling place claim
- Voter eligibility claim
- Candidate impersonation
- Synthetic audio/video claim
- Election Day misinformation
- Threats or intimidation
- Viral political claim

## Important note

Do not add real authentication yet unless necessary.

Add a clear TODO:

TODO: Add authentication and role-based access before production.

## Acceptance criteria

- Admin page shows review queue.
- A reviewer can update status.
- A reviewer can publish a public incident.
- Public incident appears on /incidents.
- Reviewer notes are stored or mocked depending on current storage layer.