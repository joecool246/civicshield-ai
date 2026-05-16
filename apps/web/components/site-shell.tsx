import Link from "next/link";
import { ShieldCheck } from "lucide-react";

const navItems = [
  { href: "/", label: "Home" },
  { href: "/ask", label: "Ask" },
  { href: "/check", label: "Check" },
  { href: "/incidents", label: "Incidents" },
  { href: "/methodology", label: "Methodology" },
];

export function SiteHeader() {
  return (
    <header className="border-b border-civic-line bg-white/95">
      <div className="mx-auto flex max-w-6xl flex-col gap-4 px-4 py-4 sm:flex-row sm:items-center sm:justify-between">
        <Link href="/" className="flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center rounded-md bg-civic-blue text-white">
            <ShieldCheck size={21} aria-hidden="true" />
          </span>
          <span>
            <span className="block text-base font-semibold text-civic-ink">CivicShield AI</span>
            <span className="block text-xs text-civic-muted">Nonpartisan verification MVP</span>
          </span>
        </Link>
        <nav className="flex flex-wrap gap-2 text-sm">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="rounded-md px-3 py-2 text-civic-muted hover:bg-civic-paper hover:text-civic-ink"
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className="border-t border-civic-line bg-white">
      <div className="mx-auto max-w-6xl px-4 py-8 text-sm text-civic-muted">
        CivicShield AI Phase 1 uses mock data only. It does not endorse candidates,
        recommend votes, or claim perfect deepfake detection.
      </div>
    </footer>
  );
}
