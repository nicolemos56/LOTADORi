import { create } from "zustand";
import { sendChatMessage } from "../lib/api.js";

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
      "Bem-vindo a Angola! 👋 Sou o Lotadori, o teu agente de viagem. Diz-me a tua cidade para começarmos."
    ),
  ],
  isSending: false,
  sessionId: null,
  tripId: null,
  driverLocation: null,

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

  sendMessage: async (text) => {
    const trimmed = text.trim();
    if (!trimmed || get().isSending) return;

    set((state) => ({
      messages: [...state.messages, newMessage("tourist", trimmed)],
      isSending: true,
    }));

    try {
      const data = await sendChatMessage(trimmed, get().sessionId);
      set((state) => ({
        messages: [
          ...state.messages,
          newMessage("agent", data.reply, {
            uiComponent: data.ui_component,
            payload: data.payload,
            sessionId: data.session_id,
          }),
        ],
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
    } catch {
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
}));
