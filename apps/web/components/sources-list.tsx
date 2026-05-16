import type { Source } from "@/lib/types";

export function SourcesList({ sources }: { sources: Source[] }) {
  if (sources.length === 0) {
    return (
      <p className="rounded-md border border-dashed border-civic-line bg-white p-4 text-sm text-civic-muted">
        No source in the Phase 1 mock dataset supports a citation yet.
      </p>
    );
  }

  return (
    <ul className="space-y-3">
      {sources.map((source) => (
        <li key={source.url} className="rounded-md border border-civic-line bg-white p-4">
          <a
            href={source.url}
            target="_blank"
            rel="noreferrer"
            className="font-medium text-civic-blue hover:underline"
          >
            {source.title}
          </a>
          <p className="mt-1 text-sm text-civic-muted">{source.publisher}</p>
        </li>
      ))}
    </ul>
  );
}
