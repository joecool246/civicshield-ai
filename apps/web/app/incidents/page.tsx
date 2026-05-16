"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { listIncidents } from "@/lib/api";
import type { Incident } from "@/lib/types";
import { RiskBadge, StatusBadge } from "@/components/status-badge";

export default function IncidentsPage() {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadIncidents() {
      try {
        setIncidents(await listIncidents());
      } catch {
        setError("Could not reach the CivicShield API. Make sure the backend is running.");
      } finally {
        setIsLoading(false);
      }
    }

    loadIncidents();
  }, []);

  return (
    <div className="page-shell">
      <h1 className="section-title">Incident Tracker</h1>
      <p className="section-copy">
        A public mock dashboard for suspicious, misleading, or AI-related
        political content. These examples are illustrative and not live cases.
      </p>

      <div className="mt-8 space-y-4">
        {isLoading && <div className="panel text-civic-muted">Loading incidents...</div>}
        {error && <div className="panel text-civic-red">{error}</div>}
        {incidents.map((incident) => (
          <Link
            href={`/incidents/${incident.id}`}
            key={incident.id}
            className="block rounded-lg border border-civic-line bg-white p-5 shadow-soft hover:border-civic-blue"
          >
            <div className="flex flex-wrap gap-2">
              <StatusBadge status={incident.status} />
              <RiskBadge level={incident.risk_level} />
            </div>
            <h2 className="mt-4 text-xl font-semibold text-civic-ink">{incident.title}</h2>
            <p className="mt-2 text-sm text-civic-muted">
              {incident.incident_type} - {incident.location}
            </p>
            <p className="mt-3 leading-7 text-civic-muted">{incident.summary}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
