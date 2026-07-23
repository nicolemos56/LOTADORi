import MessageList from "./MessageList.jsx";
import MessageInput from "./MessageInput.jsx";
import QuickSuggestions from "./QuickSuggestions.jsx";
import TripTracker from "./TripTracker.jsx";
import { useChatStore } from "../store/chatStore.js";
import TripMap from "./TripMap.jsx";

export default function ChatWindow() {
  const profileName = useChatStore((state) => state.profile.name);
  const testConnection = useChatStore((state) => state.testConnection);
  const driverLocation = useChatStore((s) => s.driverLocation);
  const showQuickActions = useChatStore((s) => s.showQuickActions);
  const messages = useChatStore((s) => s.messages);
  const tripId = useChatStore((s) => s.tripId);
  const hasMapMessage = Array.isArray(messages) && messages.some((m) => m.uiComponent === "map_view" && m.payload?.driver_selected);
  const showMap = !!driverLocation && !hasMapMessage;
  let mapPos = null;
  if (driverLocation && typeof driverLocation.lat === "number" && typeof driverLocation.lon === "number") {
    mapPos = [driverLocation.lat, driverLocation.lon];
  } else if (Array.isArray(messages)) {
    const mapMsg = Array.from(messages).reverse().find((m) => m.uiComponent === "map_view" && m.payload?.driver);
    if (mapMsg && mapMsg.payload.driver) {
      const d = mapMsg.payload.driver;
      if (typeof d.lat === "number" && typeof d.lon === "number") mapPos = [d.lat, d.lon];
      else if (d.location && typeof d.location.lat === "number" && typeof d.location.lon === "number") mapPos = [d.location.lat, d.location.lon];
    }
  }

  return (
    <div className="flex h-full min-h-screen flex-col overflow-hidden bg-white">
      <header className="border-b border-slate-200/10 bg-gradient-to-r from-brand-900 via-slate-950 to-slate-900 px-5 py-5 text-white backdrop-blur-sm lg:px-6 lg:py-6">
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="text-xs uppercase tracking-[0.35em] text-brand-300">LOTADORi</p>
              <h1 className="mt-2 text-3xl font-semibold tracking-tight text-white">
                Olá{profileName ? `, ${profileName}` : ""}
              </h1>
            </div>
            <button
              type="button"
              onClick={() => testConnection?.()}
              className="rounded-full border border-white/10 bg-white/10 px-4 py-2 text-xs font-semibold text-white transition hover:border-brand-300 hover:bg-brand-950/80"
            >
              Testar ligação
            </button>
          </div>
          <p className="max-w-xl text-sm leading-6 text-slate-900">
            O que pretende fazer hoje? Entre numa experiência local com reservas, guias e itinerários personalizados.
          </p>
        </div>
      </header>

      <div className="flex flex-1 flex-col overflow-hidden bg-slate-50 px-3 pb-3 pt-4">
        {showMap ? (
          <div className="mb-4 overflow-hidden rounded-3xl bg-slate-950">
            <TripMap position={mapPos} />
          </div>
        ) : null}

        {tripId ? (
          <div className="mb-4">
            <TripTracker tripId={tripId} />
          </div>
        ) : null}

        {showQuickActions ? (
          <div className="mb-4 rounded-3xl bg-white p-4 shadow-sm">
            <QuickSuggestions />
          </div>
        ) : null}

        <div className="flex flex-1 min-h-0 overflow-hidden rounded-[32px] bg-slate-100 shadow-sm">
          <MessageList />
        </div>
        <div className="mt-3 rounded-[32px] bg-slate-950 px-4 py-4 shadow-sm">
          <MessageInput />
        </div>
      </div>
    </div>
  );
}
