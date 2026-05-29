import type {
  AnalyzeRequest,
  AnalyzeResponse,
  LeaderboardResponse,
  ModelsResponse,
  SubmissionResponse,
  SubmissionsResponse,
} from "../types/api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    let detail = "Request failed.";
    try {
      const payload = (await response.json()) as { detail?: string };
      detail = payload.detail ?? detail;
    } catch {
      detail = response.statusText || detail;
    }
    throw new Error(detail);
  }

  return (await response.json()) as T;
}

export function getModels(): Promise<ModelsResponse> {
  return request<ModelsResponse>("/models");
}

export function analyzeText(payload: AnalyzeRequest): Promise<AnalyzeResponse> {
  return request<AnalyzeResponse>("/analyze", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getLeaderboard(): Promise<LeaderboardResponse> {
  return request<LeaderboardResponse>("/leaderboard");
}

export function saveSubmissionFromAnalysis(
  payload: AnalyzeRequest
): Promise<SubmissionResponse> {
  return request<SubmissionResponse>("/submissions/from-analysis", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getSubmissions(limit = 20): Promise<SubmissionsResponse> {
  return request<SubmissionsResponse>(`/submissions?limit=${limit}`);
}
