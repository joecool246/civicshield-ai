import type {
  AskResponse,
  BiasAudit,
  CheckResponse,
  Incident,
  ReviewTask,
  ReviewTaskUpdate,
} from "@/lib/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function askCivicShield(question: string) {
  return request<AskResponse>("/api/ask", {
    method: "POST",
    body: JSON.stringify({ question }),
  });
}

export function checkPost(content: string) {
  return request<CheckResponse>("/api/check", {
    method: "POST",
    body: JSON.stringify({ content }),
  });
}

export function listIncidents() {
  return request<Incident[]>("/api/incidents", {
    cache: "no-store",
  });
}

export function getIncident(id: string) {
  return request<Incident>(`/api/incidents/${id}`, {
    cache: "no-store",
  });
}

export function listReviewQueue() {
  return request<ReviewTask[]>("/api/admin/review-queue", {
    cache: "no-store",
  });
}

export function updateReviewTask(taskId: string, payload: ReviewTaskUpdate) {
  return request<ReviewTask>(`/api/admin/review/${taskId}`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function publishIncident(taskId: string) {
  return request<Incident>("/api/admin/incidents", {
    method: "POST",
    body: JSON.stringify({ task_id: taskId }),
  });
}

export function listBiasAudits() {
  return request<BiasAudit[]>("/api/bias-audits", {
    cache: "no-store",
  });
}

export function getBiasAudit(id: string) {
  return request<BiasAudit>(`/api/bias-audits/${id}`, {
    cache: "no-store",
  });
}
