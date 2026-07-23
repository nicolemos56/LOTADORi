import { useState, useRef } from "react";
import { useChatStore } from "../store/chatStore.js";

export default function MessageInput() {
  const [text, setText] = useState("");
  const inputRef = useRef(null);
  const sendMessage = useChatStore((state) => state.sendMessage);
  const hideQuickActions = useChatStore((state) => state.hideQuickActions);
  const isSending = useChatStore((state) => state.isSending);

  const handleSubmit = (event) => {
    event.preventDefault();
    const currentText = inputRef.current ? inputRef.current.value : text;
    if (!currentText?.trim() || isSending) return;
    hideQuickActions();
    sendMessage(currentText);
    setText("");
    if (inputRef.current) inputRef.current.value = "";
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex items-center gap-3 border-t border-slate-200 bg-white px-5 py-4"
    >
      <input
        ref={inputRef}
        type="text"
        value={text}
        onChange={(event) => setText(event.target.value)}
        placeholder="Diz o que pretende. O agente trata do resto."
        autoFocus
        className="flex-1 rounded-full border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
      />
      <button
        type="submit"
        disabled={isSending}
        className="inline-flex items-center gap-2 rounded-full bg-emerald-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-40"
      >
        {isSending ? "A processar…" : "Enviar"}
      </button>
      {/* Temporary debug button: directly calls sendChatMessage to isolate UI state issues */}
    </form>
  );
}
