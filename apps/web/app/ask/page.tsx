"use client";

import { FormEvent, useState } from "react";
import { askCivicShield } from "@/lib/api";
import type { AskResponse } from "@/lib/types";
import { SourcesList } from "@/components/sources-list";
import { StatusBadge } from "@/components/status-badge";

export default function AskPage() {
  const [question, setQuestion] = useState("What ID do I need to vote in Indiana?");
  const [result, setResult] = useState<AskResponse | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      setResult(await askCivicShield(question));
    } catch {
      setError("Could not reach the CivicShield API. Make sure the backend is running.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="page-shell">
      <h1 className="section-title">Ask CivicShield</h1>
      <p className="section-copy">
        Ask a civic process question and see a mock source-grounded answer. This
        MVP abstains when the mock dataset does not support a reliable response.
      </p>

      <div className="mt-8 grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <form onSubmit={onSubmit} className="panel">
          <label className="text-sm font-medium text-civic-ink" htmlFor="question">
            Civic question
          </label>
          <textarea
            id="question"
            className="input mt-2 min-h-36"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="When is the registration deadline?"
          />
          <button className="button mt-4" disabled={isLoading || question.trim().length === 0}>
            {isLoading ? "Checking..." : "Ask"}
          </button>
          {error && <p className="mt-4 text-sm text-civic-red">{error}</p>}
        </form>

        <section className="panel">
          <div className="flex flex-wrap items-center gap-2">
            <h2 className="text-xl font-semibold text-civic-ink">Mock answer</h2>
            {result && <StatusBadge status={result.status} />}
          </div>
          {result ? (
            <div className="mt-4 space-y-5">
              <p className="leading-7 text-civic-muted">{result.answer}</p>
              <p className="rounded-md bg-civic-paper p-3 text-sm text-civic-muted">
                Confidence: {result.confidence}. {result.note}
              </p>
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
            <p className="mt-4 text-civic-muted">
              Submit a question to see the mock answer and citation area.
            </p>
          )}
        </section>
      </div>
    </div>
  );
}
