"use client";

import { FormEvent, useState } from "react";
import { checkPost } from "@/lib/api";
import type { CheckResponse } from "@/lib/types";
import { SourcesList } from "@/components/sources-list";
import { RiskBadge, StatusBadge } from "@/components/status-badge";

export default function CheckPage() {
  const [content, setContent] = useState(
    "A post says polling places changed across the county with no official link.",
  );
  const [result, setResult] = useState<CheckResponse | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      setResult(await checkPost(content));
    } catch {
      setError("Could not reach the CivicShield API. Make sure the backend is running.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="page-shell">
      <h1 className="section-title">Check This Political Post</h1>
      <p className="section-copy">
        Paste a political claim, ad text, social post, or screenshot transcript.
        CivicShield returns structured labels and flags high-risk claims for review.
      </p>

      <div className="mt-8 grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <form onSubmit={onSubmit} className="panel">
          <label className="text-sm font-medium text-civic-ink" htmlFor="content">
            Political content
          </label>
          <textarea
            id="content"
            className="input mt-2 min-h-48"
            value={content}
            onChange={(event) => setContent(event.target.value)}
            placeholder="Paste a claim, post, URL, or screenshot text."
          />
          <button className="button mt-4" disabled={isLoading || content.trim().length === 0}>
            {isLoading ? "Reviewing..." : "Check post"}
          </button>
          {error && <p className="mt-4 text-sm text-civic-red">{error}</p>}
        </form>

        <section className="panel">
          <h2 className="text-xl font-semibold text-civic-ink">Mock result</h2>
          {result ? (
            <div className="mt-4 space-y-5">
              <div className="flex flex-wrap gap-2">
                <StatusBadge status={result.verification_status} />
                <RiskBadge level={result.risk_level} />
              </div>
              <dl className="grid gap-3 text-sm sm:grid-cols-2">
                <div>
                  <dt className="font-medium text-civic-ink">Topic</dt>
                  <dd className="mt-1 text-civic-muted">{result.topic}</dd>
                </div>
                <div>
                  <dt className="font-medium text-civic-ink">Jurisdiction</dt>
                  <dd className="mt-1 text-civic-muted">{result.jurisdiction}</dd>
                </div>
                <div>
                  <dt className="font-medium text-civic-ink">Voting related</dt>
                  <dd className="mt-1 text-civic-muted">
                    {result.is_voting_related ? "Yes" : "No"}
                  </dd>
                </div>
                <div>
                  <dt className="font-medium text-civic-ink">Confidence</dt>
                  <dd className="mt-1 capitalize text-civic-muted">{result.confidence}</dd>
                </div>
                <div>
                  <dt className="font-medium text-civic-ink">AI disclosure</dt>
                  <dd className="mt-1 capitalize text-civic-muted">
                    {result.ai_disclosure_status.replaceAll("_", " ")}
                  </dd>
                </div>
                <div>
                  <dt className="font-medium text-civic-ink">Sponsor</dt>
                  <dd className="mt-1 capitalize text-civic-muted">
                    {result.sponsor_status.replaceAll("_", " ")}
                  </dd>
                </div>
              </dl>
              <p className="leading-7 text-civic-muted">{result.explanation}</p>
              <div>
                <h3 className="mb-3 text-sm font-semibold text-civic-ink">
                  Suggested next steps
                </h3>
                <ul className="list-disc space-y-2 pl-5 text-sm leading-6 text-civic-muted">
                  {result.suggested_next_steps.map((step) => (
                    <li key={step}>{step}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h3 className="mb-3 text-sm font-semibold text-civic-ink">Sources</h3>
                <SourcesList sources={result.sources} />
              </div>
            </div>
          ) : (
            <p className="mt-4 text-civic-muted">Submit content to see the mock result card.</p>
          )}
        </section>
      </div>
    </div>
  );
}
