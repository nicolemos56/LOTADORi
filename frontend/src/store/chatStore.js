import { create } from "zustand";
import { sendChatMessage, pingBackend } from "../lib/api.js";

let nextId = 1;
const newMessage = (role, text, extra = {}) => ({
  id: nextId++,
  role,
  text,
  ...extra,
});

export const useChatStore = create((set, get) => ({
  messages: [
    newMessage(
      "agent",
      "Olá! Sou o Lotadori, o teu agente autónomo de turismo. Diz-me o que pretende fazer hoje e trato de tudo.",
    ),
  ],
  isSending: false,
  sessionId: null,
  tripId: null,
  driverLocation: null,
  showQuickActions: true,

  profile: {
    name: null,
    language: "pt",
    nationality: null,
    currentCity: null,
    interests: [],
  },

  updateProfile: (data) =>
    set((state) => ({ profile: { ...state.profile, ...data } })),

  setTripId: (tripId) => set({ tripId }),
  setDriverLocation: (driverLocation) => set({ driverLocation }),
  hideQuickActions: () => set({ showQuickActions: false }),

  sendMessage: async (text) => {
    const trimmed = text.trim();
    if (!trimmed || get().isSending) return;
    // Log for debugging in the browser context
    try {
      window.__appLogs = window.__appLogs || [];
      window.__appLogs.push(`sendMessage start: ${trimmed} session:${get().sessionId}`);
    } catch (e) {}

    set((state) => ({
      messages: [...state.messages, newMessage("tourist", trimmed)],
      isSending: true,
      showQuickActions: false,
    }));

    try {
      window.__appLogs = window.__appLogs || [];
      window.__appLogs.push(`calling sendChatMessage -> ${trimmed}`);
      const data = await sendChatMessage(trimmed, get().sessionId);
      window.__appLogs.push(`sendChatMessage returned`);
      const agentMessage = newMessage("agent", data.reply, {
        uiComponent: data.ui_component,
        payload: data.payload,
        sessionId: data.session_id,
      });

      const messages = [...get().messages, agentMessage];
      if (data.payload?.progress_steps?.length) {
        messages.push(
          newMessage("agent", "", {
            uiComponent: "progress_steps",
            payload: data.payload,
          })
        );
      }

      set((state) => ({
        messages,
        sessionId: data.session_id ?? state.sessionId,
      }));

      const payload = data.payload ?? {};
      if (payload.trip_id) {
        get().setTripId(payload.trip_id);
      }
      if (payload.city) {
        get().updateProfile({ currentCity: payload.city });
      }
      if (payload.interests?.length) {
        get().updateProfile({ interests: payload.interests });
      }
    } catch (err) {
      try { window.__appLogs.push('sendMessage caught error: ' + (err?.message || String(err))); } catch (e) {}
      set((state) => ({
        messages: [
          ...state.messages,
          newMessage(
            "agent",
            "Não consegui falar com o servidor. Confirma que o backend está a correr e tenta outra vez.",
            { isError: true }
          ),
        ],
      }));
    } finally {
      set({ isSending: false });
    }
  },
  testConnection: async () => {
    if (get().isSending) return;
    set((state) => ({ isSending: true }));
    try {
      const data = await pingBackend();
      // Show the full backend response for the test button so it matches
      // exactly what `test_connection` returns on the server.
      const agentMessage = newMessage("agent", JSON.stringify(data, null, 2), {
        uiComponent: data.ui_component,
        payload: data.payload,
        sessionId: data.session_id,
      });
      set((state) => ({ messages: [...state.messages, agentMessage], sessionId: data.session_id ?? state.sessionId }));
    } catch (e) {
      set((state) => ({ messages: [...state.messages, newMessage("agent", "Teste falhou: não foi possível contactar o backend.", { isError: true })] }));
    } finally {
      set({ isSending: false });
    }
  },
}));
