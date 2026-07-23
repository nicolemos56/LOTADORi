export default function BottomNav() {
  return (
    <nav className="mt-3 flex items-center justify-between rounded-3xl border border-slate-200 bg-white px-4 py-3 shadow-sm">
      {[
        { label: "Início", icon: "🏠", active: true },
        { label: "Viagens", icon: "🧳" },
        { label: "Mensagens", icon: "💬" },
        { label: "Perfil", icon: "👤" },
      ].map((item) => (
        <button
          key={item.label}
          type="button"
          className={`flex flex-1 flex-col items-center gap-1 rounded-3xl px-2 py-2 text-[11px] font-semibold transition ${
            item.active
              ? "bg-emerald-600 text-white shadow-sm"
              : "text-slate-500 hover:text-slate-900"
          }`}
        >
          <span className="text-base">{item.icon}</span>
          {item.label}
        </button>
      ))}
    </nav>
  );
}
