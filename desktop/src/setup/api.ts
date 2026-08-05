import type { Detection, SetupError } from "./types";

const BASE_URL = "http://127.0.0.1:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, init);
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw (body?.detail?.error ?? { code: "NETWORK_ERROR", message: `EDWIN setup request failed (${response.status}).`, retryable: true }) as SetupError;
  }
  return response.json();
}

export const setupApi = {
  health: () => request<{ status: string }>("/health"),
  detect: () => request<Detection>("/setup/detect", { method: "POST" }),
  state: () => request<{ state: { setup: { status: string; selected_model_id: string | null; last_error: SetupError | null } } }>("/setup/state"),
  select: (modelId: string) => request("/setup/model-selection", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ model_id: modelId }) }),
  install: () => request("/setup/install", { method: "POST" }),
  installStatus: () => request<{ installation: { status: string; phase: string; progress: { percent: number | null; indeterminate: boolean }; message: string; error: SetupError | null } | null; setup_status: string }>("/setup/install-status"),
  verify: () => request("/setup/verify", { method: "POST" }),
  retry: (operation: "detect" | "install" | "verify") => request("/setup/retry", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ operation }) }),
};
