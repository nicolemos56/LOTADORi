import { useChatStore } from "../store/chatStore.js";

const suggestions = [
  "Reservar hotel",
  "Reservar jantar",
  "Chamar guide-driver",
  "Tour guiado em Luanda",
  "Recomenda-me um passeio",
];

export default function QuickSuggestions() {
  const sendMessage = useChatStore((state) => state.sendMessage);
  const hideQuickActions = useChatStore((state) => state.hideQuickActions);

  const handleClick = async (item) => {
    hideQuickActions();
    await sendMessage(item);
  };

  return (
    <div className="grid gap-3 sm:grid-cols-2">
      {suggestions.map((item) => (
        <button
          key={item}
          type="button"
          onClick={() => handleClick(item)}
          className="rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-left text-sm leading-6 text-slate-700 shadow-sm transition hover:border-emerald-300 hover:bg-white"
        >
          {item}
        </button>
      ))}
    </div>
  );
}
