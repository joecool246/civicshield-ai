export const verificationStatuses = [
  "verified",
  "misleading",
  "disputed",
  "unconfirmed",
  "missing_context",
  "unable_to_verify",
] as const;

export const riskLevels = ["low", "medium", "high", "critical"] as const;
export const reviewStatuses = [
  "pending",
  "in_review",
  "approved",
  "rejected",
  "published",
  "needs_more_evidence",
] as const;

export type VerificationStatus = (typeof verificationStatuses)[number];
export type RiskLevel = (typeof riskLevels)[number];
export type ReviewStatus = (typeof reviewStatuses)[number];
