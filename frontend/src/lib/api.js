const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function sendChatMessage(message, sessionId = null) {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, session_id: sessionId }),
  });

  if (!response.ok) {
    throw new Error(`Erro do servidor (${response.status})`);
  }

  return response.json();
}
