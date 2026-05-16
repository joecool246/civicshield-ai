"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { getIncident } from "@/lib/api";
import type { Incident } from "@/lib/types";
import { SourcesList } from "@/components/sources-list";
import { RiskBadge, StatusBadge } from "@/components/status-badge";

export default function IncidentDetailPage() {
  const params = useParams<{ id: string }>();
  const [incident, setIncident] = useState<Incident | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadIncident() {
      try {
        setIncident(await getIncident(params.id));
      } catch {
        setError("Could not load this incident from the CivicShield API.");
      } finally {
        setIsLoading(false);
      }
    }

    loadIncident();
  }, [params.id]);

  return (
    <div className="page-shell">
      <Link href="/incidents" className="text-sm font-medium text-civic-blue hover:underline">
        Back to incidents
      </Link>

      {isLoading && <div className="panel mt-6 text-civic-muted">Loading incident...</div>}
      {error && <div className="panel mt-6 text-civic-red">{error}</div>}
      {incident && (
        <article className="panel mt-6">
          <div className="flex flex-wrap gap-2">
            <StatusBadge status={incident.status} />
            <RiskBadge level={incident.risk_level} />
          </div>
          <h1 className="mt-4 text-3xl font-semibold text-civic-ink">{incident.title}</h1>
          <p className="mt-2 text-sm text-civic-muted">
            {incident.incident_type} - {incident.location}
          </p>
          <p className="mt-5 leading-7 text-civic-muted">{incident.summary}</p>

          <section className="mt-6">
            <h2 className="text-lg font-semibold text-civic-ink">Evidence separated from interpretation</h2>
            <ul className="mt-3 list-disc space-y-2 pl-5 text-sm leading-6 text-civic-muted">
              {incident.evidence.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </section>

          <section className="mt-6">
            <h2 className="mb-3 text-lg font-semibold text-civic-ink">Sources</h2>
            <SourcesList sources={incident.sources} />
          </section>
        </article>
      )}
    </div>
  );
}
