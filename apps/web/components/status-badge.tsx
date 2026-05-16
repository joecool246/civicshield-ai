import clsx from "clsx";
import type { RiskLevel, VerificationStatus } from "@civicshield/shared";

type BadgeTone = "blue" | "green" | "gold" | "red" | "gray";

const statusTones: Record<VerificationStatus, BadgeTone> = {
  verified: "green",
  misleading: "red",
  disputed: "gold",
  unconfirmed: "gray",
  missing_context: "blue",
  unable_to_verify: "gray",
};

const riskTones: Record<RiskLevel, BadgeTone> = {
  low: "green",
  medium: "gold",
  high: "red",
  critical: "red",
};

const toneClasses: Record<BadgeTone, string> = {
  blue: "border-blue-200 bg-blue-50 text-blue-800",
  green: "border-emerald-200 bg-emerald-50 text-emerald-800",
  gold: "border-amber-200 bg-amber-50 text-amber-800",
  red: "border-red-200 bg-red-50 text-red-800",
  gray: "border-slate-200 bg-slate-50 text-slate-700",
};

function prettyLabel(value: string) {
  return value.replaceAll("_", " ");
}

export function StatusBadge({ status }: { status: VerificationStatus }) {
  return (
    <span className={clsx("badge", toneClasses[statusTones[status]])}>
      {prettyLabel(status)}
    </span>
  );
}

export function RiskBadge({ level }: { level: RiskLevel }) {
  return (
    <span className={clsx("badge", toneClasses[riskTones[level]])}>
      {prettyLabel(level)} risk
    </span>
  );
}
