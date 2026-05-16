export const verificationStatuses = [
  "verified",
  "misleading",
  "disputed",
  "unconfirmed",
  "missing_context",
  "unable_to_verify",
] as const;

export const riskLevels = ["low", "medium", "high", "critical"] as const;

export type VerificationStatus = (typeof verificationStatuses)[number];
export type RiskLevel = (typeof riskLevels)[number];
