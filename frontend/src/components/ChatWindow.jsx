import MessageList from "./MessageList.jsx";
import MessageInput from "./MessageInput.jsx";

export default function ChatWindow() {
  return (
    <div className="flex h-full w-full max-w-2xl flex-col overflow-hidden bg-white shadow-xl sm:h-[85vh] sm:rounded-2xl">
      <header className="flex items-center gap-3 border-b border-slate-200 bg-emerald-700 px-5 py-4 text-white">
        <span className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-600 text-xl">
          🌍
        </span>
        <div>
          <h1 className="text-lg font-semibold leading-tight">TurismoConnect</h1>
          <p className="text-xs text-emerald-100">Da curiosidade à experiência.</p>
        </div>
      </header>

      <MessageList />
      <MessageInput />
    </div>
  );
}
