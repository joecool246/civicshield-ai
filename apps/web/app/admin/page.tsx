"use client";

import { FormEvent, useEffect, useState } from "react";
import { riskLevels, verificationStatuses } from "@civicshield/shared";
import type { RiskLevel, ReviewStatus, VerificationStatus } from "@civicshield/shared";
import { listReviewQueue, publishIncident, updateReviewTask } from "@/lib/api";
import type { ReviewTask } from "@/lib/types";
import { RiskBadge, StatusBadge } from "@/components/status-badge";
import { SourcesList } from "@/components/sources-list";

function pretty(value: string) {
  return value.replaceAll("_", " ");
}

export default function AdminPage() {
  const [tasks, setTasks] = useState<ReviewTask[]>([]);
  const [notes, setNotes] = useState<Record<string, string>>({});
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  async function refreshQueue() {
    setError("");
    try {
      const queue = await listReviewQueue();
      setTasks(queue);
      setNotes(Object.fromEntries(queue.map((task) => [task.id, task.reviewer_notes])));
    } catch {
      setError("Could not load the review queue. Make sure the backend is running.");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    refreshQueue();
  }, []);

  async function updateTask(taskId: string, payload: Parameters<typeof updateReviewTask>[1]) {
    setError("");
    setMessage("");
    try {
      const updated = await updateReviewTask(taskId, payload);
      setTasks((current) => current.map((task) => (task.id === taskId ? updated : task)));
      setNotes((current) => ({ ...current, [taskId]: updated.reviewer_notes }));
      setMessage(`Updated ${taskId}.`);
    } catch {
      setError("Could not update this review task.");
    }
  }

  async function saveNotes(event: FormEvent<HTMLFormElement>, taskId: string) {
    event.preventDefault();
    await updateTask(taskId, { reviewer_notes: notes[taskId] ?? "" });
  }

  async function publishTask(taskId: string) {
    setError("");
    setMessage("");
    try {
      await publishIncident(taskId);
      await refreshQueue();
      setMessage(`Published ${taskId} as a public mock incident.`);
    } catch {
      setError("Could not publish this review task.");
    }
  }

  return (
    <div className="page-shell">
      <h1 className="section-title">Admin Review Dashboard</h1>
      <p className="section-copy">
        Human review queue for high-risk political and election claims. This
        Phase 3 page is mock-only and has no authentication yet.
      </p>
      <div className="mt-4 rounded-md border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900">
        TODO: Add authentication and role-based access before production.
      </div>

      {isLoading && <div className="panel mt-8 text-civic-muted">Loading review queue...</div>}
      {error && <div className="panel mt-8 text-civic-red">{error}</div>}
      {message && <div className="panel mt-8 text-civic-teal">{message}</div>}

      <div className="mt-8 space-y-6">
        {tasks.map((task) => (
          <article key={task.id} className="panel">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-civic-muted">
                  {task.id} - {pretty(task.review_status)}
                </p>
                <h2 className="mt-2 text-2xl font-semibold text-civic-ink">{task.topic}</h2>
              </div>
              <div className="flex flex-wrap gap-2">
                <StatusBadge status={task.suggested_verification_status} />
                <RiskBadge level={task.suggested_risk_level} />
              </div>
            </div>

            <div className="mt-5 grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
              <section className="rounded-lg border border-civic-line p-4">
                <h3 className="text-sm font-semibold text-civic-ink">Submitted content</h3>
                <p className="mt-2 text-sm leading-6 text-civic-muted">{task.submitted_content}</p>
                <h3 className="mt-5 text-sm font-semibold text-civic-ink">Extracted claim</h3>
                <p className="mt-2 text-sm leading-6 text-civic-muted">{task.extracted_claim}</p>
              </section>

              <section className="rounded-lg border border-civic-line p-4">
                <dl className="grid gap-3 text-sm sm:grid-cols-2">
                  <div>
                    <dt className="font-medium text-civic-ink">Jurisdiction</dt>
                    <dd className="mt-1 text-civic-muted">{task.jurisdiction}</dd>
                  </div>
                  <div>
                    <dt className="font-medium text-civic-ink">Voting related</dt>
                    <dd className="mt-1 text-civic-muted">
                      {task.is_voting_related ? "Yes" : "No"}
                    </dd>
                  </div>
                  <div>
                    <dt className="font-medium text-civic-ink">AI disclosure</dt>
                    <dd className="mt-1 capitalize text-civic-muted">
                      {pretty(task.ai_disclosure_status)}
                    </dd>
                  </div>
                  <div>
                    <dt className="font-medium text-civic-ink">Sponsor</dt>
                    <dd className="mt-1 capitalize text-civic-muted">
                      {pretty(task.sponsor_status)}
                    </dd>
                  </div>
                  <div>
                    <dt className="font-medium text-civic-ink">Confidence</dt>
                    <dd className="mt-1 capitalize text-civic-muted">{task.confidence}</dd>
                  </div>
                </dl>
              </section>
            </div>

            <div className="mt-5 grid gap-4 lg:grid-cols-2">
              <label className="text-sm font-medium text-civic-ink">
                Verification status
                <select
                  className="input mt-2"
                  value={task.suggested_verification_status}
                  onChange={(event) =>
                    updateTask(task.id, {
                      suggested_verification_status: event.target.value as VerificationStatus,
                    })
                  }
                >
                  {verificationStatuses.map((status) => (
                    <option key={status} value={status}>
                      {pretty(status)}
                    </option>
                  ))}
                </select>
              </label>

              <label className="text-sm font-medium text-civic-ink">
                Risk level
                <select
                  className="input mt-2"
                  value={task.suggested_risk_level}
                  onChange={(event) =>
                    updateTask(task.id, { suggested_risk_level: event.target.value as RiskLevel })
                  }
                >
                  {riskLevels.map((level) => (
                    <option key={level} value={level}>
                      {pretty(level)}
                    </option>
                  ))}
                </select>
              </label>
            </div>

            <form onSubmit={(event) => saveNotes(event, task.id)} className="mt-5">
              <label className="text-sm font-medium text-civic-ink" htmlFor={`${task.id}-notes`}>
                Reviewer notes
              </label>
              <textarea
                id={`${task.id}-notes`}
                className="input mt-2 min-h-28"
                value={notes[task.id] ?? ""}
                onChange={(event) =>
                  setNotes((current) => ({ ...current, [task.id]: event.target.value }))
                }
                placeholder="Add source checks, uncertainty, and reviewer rationale."
              />
              <button className="button mt-3" type="submit">
                Save notes
              </button>
            </form>

            <div className="mt-5 flex flex-wrap gap-2">
              {(["approved", "rejected", "needs_more_evidence"] as ReviewStatus[]).map((status) => (
                <button
                  key={status}
                  className="rounded-md border border-civic-line bg-white px-3 py-2 text-sm font-medium capitalize text-civic-ink hover:bg-civic-paper"
                  onClick={() => updateTask(task.id, { review_status: status })}
                  type="button"
                >
                  Mark {pretty(status)}
                </button>
              ))}
              <button className="button" onClick={() => publishTask(task.id)} type="button">
                Publish as incident
              </button>
            </div>

            <section className="mt-5">
              <h3 className="mb-3 text-sm font-semibold text-civic-ink">Sources</h3>
              <SourcesList sources={task.sources} />
            </section>
          </article>
        ))}
      </div>
    </div>
  );
}
