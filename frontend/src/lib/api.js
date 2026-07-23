// Principal connector to the backend API.
// This module exposes the main client API used by the chat store.
// If you need to run a simple connectivity test, use `testConnection()` below.

const API_URL = (import.meta.env.VITE_API_URL || "http://127.0.0.1:8000").trim();

export async function sendChatMessage(message, sessionId = null) {
  const endpoint = new URL("/chat", API_URL).toString();
  try { window.__appLogs = window.__appLogs || []; window.__appLogs.push('[api] sendChatMessage -> ' + endpoint + ' ' + JSON.stringify({ message, sessionId })); } catch (e) {}
  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, session_id: sessionId }),
    });
    try {
      if (!response.ok) {
        try { window.__appLogs.push('[api] sendChatMessage response not ok ' + response.status); } catch (e) {}
        throw new Error(`Erro do servidor (${response.status})`);
      }

      const json = await response.json();
      try { window.__appLogs.push('[api] sendChatMessage response json ' + JSON.stringify(json)); } catch (e) {}
      return json;
    } catch (e) {
      try { window.__appLogs.push('[api] sendChatMessage parse/error ' + e.message); } catch (e2) {}
      throw e;
    }
  } catch (e) {
    try { window.__appLogs.push('[api] sendChatMessage fetch error ' + e.message); } catch (e2) {}
    throw e;
  }
}

// Clean connectivity helper: calls a dedicated /ping endpoint on the backend.
// Returns parsed JSON from the backend. Use this for quick health/check tests.
export async function pingBackend(message = "Ola servidor") {
  // Use the new dedicated JSON endpoint for the UI test button
  const endpoint = new URL("/test-connection", API_URL).toString();
  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    throw new Error(`Erro do servidor (${response.status})`);
  }

  return response.json();
}

// Backwards compatibility: some modules may import `testConnection`.
export const testConnection = pingBackend;

