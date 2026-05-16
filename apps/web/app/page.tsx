import Link from "next/link";
import { ArrowRight, FileSearch, Landmark, ListChecks } from "lucide-react";

const capabilities = [
  {
    title: "Ask civic questions",
    copy: "Get source-grounded answers from the local trusted source set.",
    icon: Landmark,
  },
  {
    title: "Check a political post",
    copy: "Paste a claim and see a verification label, risk level, and next steps.",
    icon: FileSearch,
  },
  {
    title: "Track incidents",
    copy: "Review mock examples of suspicious or context-missing political content.",
    icon: ListChecks,
  },
];

export default function HomePage() {
  return (
    <div className="bg-civic-paper">
      <section className="page-shell grid gap-10 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wide text-civic-teal">
            Indiana 2026 pilot - Phase 2 source-grounded MVP
          </p>
          <h1 className="mt-4 max-w-4xl text-4xl font-semibold tracking-normal text-civic-ink sm:text-5xl">
            CivicShield helps voters verify political information in the AI era.
          </h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-civic-muted">
            AI can make political information easier to fake and harder to trust.
            CivicShield is a nonpartisan verification layer built around official
            sources, transparent labels, and clear uncertainty.
          </p>
          <div className="mt-7 flex flex-wrap gap-3">
            <Link href="/check" className="button gap-2">
              Check a post <ArrowRight size={16} aria-hidden="true" />
            </Link>
            <Link
              href="/ask"
              className="inline-flex items-center justify-center rounded-md border border-civic-line bg-white px-4 py-2 text-sm font-medium text-civic-ink hover:bg-slate-50"
            >
              Ask CivicShield
            </Link>
          </div>
        </div>
        <div className="panel">
          <h2 className="text-xl font-semibold text-civic-ink">Phase 2 boundaries</h2>
          <div className="mt-5 space-y-4 text-sm leading-6 text-civic-muted">
            <p>
              This MVP uses a local trusted source dataset and a mock AI provider,
              so the product flow works without API keys, databases, auth, or production systems.
            </p>
            <p>
              CivicShield does not endorse candidates, does not recommend votes,
              and does not claim perfect detection of synthetic or manipulated media.
            </p>
          </div>
        </div>
      </section>

      <section className="border-y border-civic-line bg-white">
        <div className="page-shell grid gap-4 md:grid-cols-3">
          {capabilities.map((item) => (
            <article key={item.title} className="rounded-lg border border-civic-line p-5">
              <item.icon className="h-6 w-6 text-civic-blue" aria-hidden="true" />
              <h2 className="mt-4 text-lg font-semibold text-civic-ink">{item.title}</h2>
              <p className="mt-2 text-sm leading-6 text-civic-muted">{item.copy}</p>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
