const API_URL = "http://127.0.0.1:8000";

export async function getHardware() {
  const response = await fetch(`${API_URL}/hardware`);

  if (!response.ok) {
    throw new Error("Failed to fetch hardware.");
  }

  return response.json();
}

export async function sendChat(message: string) {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to contact EDWIN.");
  }

  return response.json();
}

export async function getStatus() {
  const response = await fetch(`${API_URL}/status`);

  if (!response.ok) {
    throw new Error("Failed to fetch status.");
  }

  return response.json();
}
export async function getOnboarding() {
  const response = await fetch(`${API_URL}/onboarding`);

  if (!response.ok) {
    throw new Error("Failed to fetch onboarding state.");
  }

  return response.json();
}
export async function completeOnboarding(selectedModel: string) {
  const response = await fetch(`${API_URL}/onboarding/complete`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      selected_model: selectedModel,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to complete onboarding.");
  }

  return response.json();
}