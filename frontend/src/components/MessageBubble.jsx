import { useChatStore } from "../store/chatStore.js";

const interestOptions = ["História", "Gastronomia", "Natureza", "Vida Noturna", "Praias"];

export default function MessageBubble({ message }) {
  const isTourist = message.role === "tourist";
  const sendMessage = useChatStore((state) => state.sendMessage);

  const bubbleStyle = isTourist
    ? "bg-emerald-600 text-white rounded-br-sm"
    : message.isError
      ? "bg-red-50 text-red-700 border border-red-200 rounded-bl-sm"
      : "bg-white text-slate-800 shadow-sm rounded-bl-sm";

  return (
    <div className={`flex ${isTourist ? "justify-end" : "justify-start"}`}>
      <div className={`max-w-[85%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${bubbleStyle}`}>
        <div className="whitespace-pre-wrap">{message.text}</div>

        {message.uiComponent === "interest_prompt" && (
          <div className="mt-3 flex flex-wrap gap-2">
            {interestOptions.map((interest) => (
              <button
                key={interest}
                type="button"
                onClick={() => sendMessage(interest)}
                className="rounded-full border border-emerald-500 px-3 py-1.5 text-xs font-semibold text-emerald-700 transition hover:bg-emerald-50"
              >
                {interest}
              </button>
            ))}
          </div>
        )}

        {message.uiComponent === "place_cards" && message.payload?.places && (
          <div className="mt-3 grid gap-3">
            {message.payload.places.map((place) => (
              <div key={place.name} className="overflow-hidden rounded-2xl border border-slate-200 bg-slate-50">
                {place.photo_url && (
                  <img src={place.photo_url} alt={place.name} className="h-36 w-full object-cover" />
                )}
                <div className="space-y-2 p-3">
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <h3 className="font-semibold text-slate-900">{place.name}</h3>
                      <p className="text-xs text-slate-500">{place.category}</p>
                    </div>
                    <span className="rounded-full bg-amber-100 px-2.5 py-1 text-xs font-semibold text-amber-700">
                      ★ {place.rating}
                    </span>
                  </div>

                  <p className="text-xs text-slate-600">{place.description}</p>

                  <div className="flex flex-wrap gap-2 text-[11px] text-slate-600">
                    <span className="rounded-full bg-white px-2.5 py-1">⏱ {place.visit_duration_minutes} min</span>
                    <span className="rounded-full bg-white px-2.5 py-1">💶 {place.avg_cost} USD</span>
                    <span className="rounded-full bg-white px-2.5 py-1">📍 {place.distance_km} km</span>
                    <span className="rounded-full bg-white px-2.5 py-1">🕒 {place.best_time}</span>
                  </div>

                  <div className="mt-3 flex flex-wrap gap-2">
                    <button
                      type="button"
                      onClick={() => sendMessage(place.name)}
                      className="rounded-full border border-emerald-500 bg-white px-3 py-1.5 text-xs font-semibold text-emerald-700 transition hover:bg-emerald-50"
                    >
                      Ver detalhes
                    </button>
                    <button
                      type="button"
                      onClick={() => sendMessage(`Quero ir para ${place.name}`)}
                      className="rounded-full bg-emerald-600 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-emerald-700"
                    >
                      Quero ir para este lugar
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {message.uiComponent === "place_detail" && (
          <div className="mt-3 overflow-hidden rounded-2xl border border-emerald-100 bg-emerald-50 text-sm text-emerald-900">
            <div className="space-y-3 p-3">
              <p>Excelente escolha. O destino é uma experiência memorável para quem gosta de descobrir Luanda.</p>
              <p className="font-semibold">Deseja que encontre um Driver-Guide certificado para acompanhá-lo?</p>

              {message.payload?.details && (
                <div className="rounded-2xl bg-white p-3 text-slate-700 shadow-sm">
                  <h3 className="font-semibold">{message.payload.details.name}</h3>
                  <p className="text-xs text-slate-500">{message.payload.details.category}</p>
                  <p className="mt-2 text-xs text-slate-600">{message.payload.details.description}</p>
                </div>
              )}

              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => sendMessage("sim")}
                  className="flex-1 rounded-full bg-emerald-600 px-3 py-2 text-xs font-semibold text-white transition hover:bg-emerald-700"
                >
                  Sim
                </button>
                <button
                  type="button"
                  onClick={() => sendMessage("não")}
                  className="flex-1 rounded-full border border-emerald-500 bg-white px-3 py-2 text-xs font-semibold text-emerald-700 transition hover:bg-emerald-50"
                >
                  Não
                </button>
              </div>
            </div>
          </div>
        )}

        {message.uiComponent === "driver_cards" && message.payload?.drivers && (
          <div className="mt-3 grid gap-3">
            {message.payload.drivers.map((driver) => (
              <div key={driver.id} className="overflow-hidden rounded-2xl border border-slate-200 bg-slate-50 p-4 shadow-sm">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h3 className="text-base font-semibold text-slate-900">{driver.name}</h3>
                    <p className="text-xs text-slate-500">{driver.specialties?.join(", ") || "Guia local"}</p>
                  </div>
                  <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-semibold text-amber-700">
                    ★ {driver.rating ?? "N/A"}
                  </span>
                </div>

                <div className="mt-3 grid gap-2 text-[11px] text-slate-600">
                  <p>Idiomas: {driver.languages?.join(", ") || "Português"}</p>
                  <p>Viagens: {driver.trips_count ?? "N/A"}</p>
                  <p>Preço base: {driver.base_price != null ? `${driver.base_price.toFixed(2)} USD` : "Indisponível"}</p>
                  <p>Distância: {driver.distance_km ?? "N/A"} km</p>
                </div>

                <button
                  type="button"
                  onClick={() => sendMessage(`Quero este Driver-Guide: ${driver.name}`)}
                  className="mt-4 w-full rounded-full bg-emerald-600 px-3 py-2 text-xs font-semibold text-white transition hover:bg-emerald-700"
                >
                  Escolher este guia
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
