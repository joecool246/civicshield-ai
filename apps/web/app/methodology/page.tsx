const principles = [
  "CivicShield does not endorse candidates or generate voting recommendations.",
  "Official sources come first when answering civic and election process questions.",
  "The product never claims perfect deepfake or synthetic media detection.",
  "Evidence is separated from interpretation so users can see what is known and what remains uncertain.",
  "High-risk political and election claims move through the mock human review workflow.",
  "Bias audit scores are mock indicators for review, not proof of intentional bias.",
];

const labels = [
  ["Verified", "Supported by official or primary evidence in the review set."],
  ["Misleading", "Contains a real element but presents it in a materially distorted way."],
  ["Disputed", "Credible sources disagree or the claim is contested by evidence."],
  ["Unconfirmed", "Not enough reliable evidence is available yet."],
  ["Missing context", "A claim may be incomplete without date, source, sponsor, or original media."],
  ["Unable to verify", "CivicShield cannot support the answer or claim from trusted sources."],
];

export default function MethodologyPage() {
  return (
    <div className="page-shell">
      <h1 className="section-title">Methodology</h1>
      <p className="section-copy">
        CivicShield is designed as a nonpartisan civic verification platform.
        Phase 4 demonstrates local source retrieval, mock provider output, an
        in-memory human review queue, and a mock AI bias audit lab before real AI
        calls, databases, or production access controls are added.
      </p>

      <section className="mt-8 grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <div className="panel">
          <h2 className="text-xl font-semibold text-civic-ink">Verification principles</h2>
          <ul className="mt-4 list-disc space-y-3 pl-5 text-sm leading-6 text-civic-muted">
            {principles.map((principle) => (
              <li key={principle}>{principle}</li>
            ))}
          </ul>
        </div>

        <div className="panel">
          <h2 className="text-xl font-semibold text-civic-ink">Labels</h2>
          <div className="mt-4 divide-y divide-civic-line">
            {labels.map(([label, description]) => (
              <div key={label} className="grid gap-1 py-3 sm:grid-cols-[150px_1fr]">
                <dt className="font-medium text-civic-ink">{label}</dt>
                <dd className="text-sm leading-6 text-civic-muted">{description}</dd>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="panel mt-6">
        <h2 className="text-xl font-semibold text-civic-ink">Bias audit limitations</h2>
        <ul className="mt-4 list-disc space-y-3 pl-5 text-sm leading-6 text-civic-muted">
          <li>Scores are not proof of intentional bias.</li>
          <li>The audit looks for patterns across prompts rather than isolated responses.</li>
          <li>The system checks framing, source use, refusal behavior, and voting advice risk.</li>
          <li>Human review is needed before publishing real claims about specific models.</li>
          <li>This MVP uses mock audit data only and does not call real AI systems.</li>
        </ul>
      </section>
    </div>
  );
}
