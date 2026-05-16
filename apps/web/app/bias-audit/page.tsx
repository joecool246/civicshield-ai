"use client";

import { useEffect, useState } from "react";
import { listBiasAudits } from "@/lib/api";
import type { BiasAudit } from "@/lib/types";
import { RiskBadge } from "@/components/status-badge";

const scoreLabels = [
  ["source_balance_score", "Source balance"],
  ["framing_score", "Framing"],
  ["symmetry_score", "Symmetry"],
  ["refusal_consistency_score", "Refusal consistency"],
  ["candidate_neutrality_score", "Candidate neutrality"],
  ["uncertainty_transparency_score", "Uncertainty transparency"],
] as const;

function ScoreBar({ label, value }: { label: string; value: number }) {
  return (
    <div>
      <div className="mb-1 flex items-center justify-between gap-3 text-xs">
        <span className="font-medium text-civic-ink">{label}</span>
        <span className="text-civic-muted">{value}/100</span>
      </div>
      <div className="h-2 rounded-full bg-civic-paper">
        <div
          className="h-2 rounded-full bg-civic-blue"
          style={{ width: `${Math.max(0, Math.min(100, value))}%` }}
        />
      </div>
    </div>
  );
}

export default function BiasAuditPage() {
  const [audits, setAudits] = useState<BiasAudit[]>([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadAudits() {
      try {
        setAudits(await listBiasAudits());
      } catch {
        setError("Could not load mock bias audits. Make sure the backend is running.");
      } finally {
        setIsLoading(false);
      }
    }

    loadAudits();
  }, []);

  return (
    <div className="page-shell">
      <h1 className="section-title">AI Bias Audit Lab</h1>
      <p className="section-copy">
        Mock political AI audit results for studying source balance, framing,
        refusal consistency, candidate neutrality, and voting advice risk. These
        scores are not proof of intentional bias and do not evaluate real models.
      </p>

      <section className="mt-6 rounded-lg border border-civic-line bg-white p-5">
        <h2 className="text-xl font-semibold text-civic-ink">Methodology notes</h2>
        <ul className="mt-3 list-disc space-y-2 pl-5 text-sm leading-6 text-civic-muted">
          <li>Scores look for patterns across prompts, not one-off proof of bias.</li>
          <li>The mock audit checks framing, source use, refusal behavior, and voting advice risk.</li>
          <li>Human review is needed before publishing real claims about specific models.</li>
          <li>This MVP uses mock data only and makes no real AI API calls.</li>
        </ul>
      </section>

      {isLoading && <div className="panel mt-8 text-civic-muted">Loading audits...</div>}
      {error && <div className="panel mt-8 text-civic-red">{error}</div>}

      <div className="mt-8 space-y-6">
        {audits.map((audit) => (
          <article key={audit.id} className="panel">
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-civic-muted">
                  {audit.model_name} - {audit.topic}
                </p>
                <h2 className="mt-2 text-2xl font-semibold text-civic-ink">{audit.prompt}</h2>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                <RiskBadge level={audit.overall_bias_risk} />
                <span className="badge border-slate-200 bg-slate-50 text-slate-700">
                  Voting advice: {audit.voting_advice_flag ? "flagged" : "not flagged"}
                </span>
              </div>
            </div>

            <div className="mt-5 grid gap-4 lg:grid-cols-[1fr_0.9fr]">
              <section className="rounded-lg border border-civic-line p-4">
                <h3 className="text-sm font-semibold text-civic-ink">Mock model response</h3>
                <p className="mt-2 text-sm leading-6 text-civic-muted">
                  {audit.mock_model_response}
                </p>
                <h3 className="mt-5 text-sm font-semibold text-civic-ink">
                  Reviewer or methodology notes
                </h3>
                <p className="mt-2 text-sm leading-6 text-civic-muted">
                  {audit.methodology_notes}
                </p>
              </section>

              <section className="space-y-4 rounded-lg border border-civic-line p-4">
                {scoreLabels.map(([key, label]) => (
                  <ScoreBar key={key} label={label} value={audit[key]} />
                ))}
              </section>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
