import type { RiskLevel, ReviewStatus, VerificationStatus } from "@civicshield/shared";

export type Source = {
  title: string;
  url: string;
  publisher: string;
};

export type AskResponse = {
  answer: string;
  status: VerificationStatus;
  confidence: "low" | "medium" | "high";
  sources: Source[];
  note: string;
  suggested_next_steps: string[];
};

export type CheckResponse = {
  claim_text: string;
  topic: string;
  jurisdiction: string;
  is_voting_related: boolean;
  verification_status: VerificationStatus;
  ai_disclosure_status:
    | "ai_disclosed"
    | "ai_not_disclosed"
    | "ai_unclear"
    | "not_applicable";
  sponsor_status:
    | "sponsor_found"
    | "sponsor_missing"
    | "sponsor_unclear"
    | "not_applicable";
  risk_level: RiskLevel;
  confidence: "low" | "medium" | "high";
  explanation: string;
  suggested_next_steps: string[];
  sources: Source[];
};

export type Incident = {
  id: string;
  title: string;
  incident_type: string;
  location: string;
  status: VerificationStatus;
  risk_level: RiskLevel;
  summary: string;
  evidence: string[];
  sources: Source[];
};

export type ReviewTask = {
  id: string;
  submitted_content: string;
  extracted_claim: string;
  topic: string;
  jurisdiction: string;
  is_voting_related: boolean;
  suggested_verification_status: VerificationStatus;
  suggested_risk_level: RiskLevel;
  ai_disclosure_status:
    | "ai_disclosed"
    | "ai_not_disclosed"
    | "ai_unclear"
    | "not_applicable";
  sponsor_status:
    | "sponsor_found"
    | "sponsor_missing"
    | "sponsor_unclear"
    | "not_applicable";
  confidence: "low" | "medium" | "high";
  sources: Source[];
  reviewer_notes: string;
  review_status: ReviewStatus;
};

export type ReviewTaskUpdate = Partial<{
  review_status: ReviewStatus;
  reviewer_notes: string;
  suggested_verification_status: VerificationStatus;
  suggested_risk_level: RiskLevel;
}>;

export type BiasAudit = {
  id: string;
  model_name: string;
  topic: string;
  prompt: string;
  mock_model_response: string;
  source_balance_score: number;
  framing_score: number;
  symmetry_score: number;
  refusal_consistency_score: number;
  candidate_neutrality_score: number;
  voting_advice_flag: boolean;
  uncertainty_transparency_score: number;
  overall_bias_risk: RiskLevel;
  methodology_notes: string;
};
