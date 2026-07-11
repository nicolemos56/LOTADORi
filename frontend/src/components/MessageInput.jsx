import { useState } from "react";
import { useChatStore } from "../store/chatStore.js";

export default function MessageInput() {
  const [text, setText] = useState("");
  const sendMessage = useChatStore((state) => state.sendMessage);
  const isSending = useChatStore((state) => state.isSending);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!text.trim() || isSending) return;
    sendMessage(text);
    setText("");
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex items-center gap-2 border-t border-slate-200 bg-white px-4 py-3"
    >
      <input
        type="text"
        value={text}
        onChange={(event) => setText(event.target.value)}
        placeholder="Escreve a tua mensagem…"
        autoFocus
        className="flex-1 rounded-full border border-slate-300 px-4 py-2.5 text-sm outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
      />
      <button
        type="submit"
        disabled={!text.trim() || isSending}
        className="rounded-full bg-emerald-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-40"
      >
        Enviar
      </button>
    </form>
  );
}
