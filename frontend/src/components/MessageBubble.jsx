import { useChatStore } from "../store/chatStore.js";
import TripMap from "./TripMap.jsx";
import { Clock3, DollarSign, MapPin, Star } from "lucide-react";

const interestOptions = ["História", "Gastronomia", "Natureza", "Vida Noturna", "Praias"];

function getCoordinates(source) {
  if (!source) return null;
  const lat = source.lat ?? source.location?.lat;
  const lon = source.lon ?? source.location?.lon;
  if (lat == null || lon == null) return null;
  const latNum = typeof lat === "number" ? lat : Number(lat);
  const lonNum = typeof lon === "number" ? lon : Number(lon);
  if (!Number.isFinite(latNum) || !Number.isFinite(lonNum)) return null;
  return [latNum, lonNum];
}

export default function MessageBubble({ message }) {
  const isTourist = message.role === "tourist";
  const sendMessage = useChatStore((state) => state.sendMessage);
  const driverLocation = useChatStore((state) => state.driverLocation);
  const inlineMapPosition = getCoordinates(driverLocation) || getCoordinates(message.payload?.driver);

  const bubbleStyle = isTourist
    ? "bg-slate-900 text-white rounded-br-sm"
    : message.isError
      ? "bg-rose-50 text-rose-700 border border-rose-200 rounded-bl-sm"
      : "bg-white text-slate-900 shadow-[0_10px_30px_-20px_rgba(15,23,42,0.4)] rounded-bl-sm";

  return (
    <div className={`flex ${isTourist ? "justify-end" : "justify-start"}`}>
      <div className={`max-w-[85%] rounded-3xl px-5 py-4 text-sm leading-relaxed ${bubbleStyle}`}>
        <div className="whitespace-pre-wrap break-words">{message.text}</div>

        {message.uiComponent === "interest_prompt" && (
          <div className="mt-4 flex flex-wrap gap-2">
            {interestOptions.map((interest) => (
              <button
                key={interest}
                type="button"
                onClick={() => sendMessage(interest)}
                className="rounded-full border border-emerald-500 bg-white px-3 py-1.5 text-xs font-semibold text-emerald-700 transition hover:bg-emerald-50"
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
                    <span className="inline-flex items-center gap-1 rounded-full bg-amber-100 px-2.5 py-1 text-xs font-semibold text-amber-700">
                      <Star className="h-3.5 w-3.5" /> {place.rating}
                    </span>
                  </div>

                  <p className="text-xs text-slate-600">{place.description}</p>

                  <div className="flex flex-wrap gap-2 text-[11px] text-slate-600">
                    <span className="inline-flex items-center gap-1 rounded-full bg-white px-2.5 py-1">
                      <Clock3 className="h-3.5 w-3.5" /> {place.visit_duration_minutes} min
                    </span>
                    <span className="inline-flex items-center gap-1 rounded-full bg-white px-2.5 py-1">
                      <DollarSign className="h-3.5 w-3.5" /> {place.avg_cost} USD
                    </span>
                    <span className="inline-flex items-center gap-1 rounded-full bg-white px-2.5 py-1">
                      <MapPin className="h-3.5 w-3.5" /> {place.distance_km} km
                    </span>
                    <span className="inline-flex items-center gap-1 rounded-full bg-white px-2.5 py-1">
                      <Clock3 className="h-3.5 w-3.5" /> {place.best_time}
                    </span>
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
                      onClick={() => sendMessage(`Reservar ${place.name}`)}
                      className="rounded-full border border-slate-300 bg-slate-100 px-3 py-1.5 text-xs font-semibold text-slate-800 transition hover:bg-slate-200"
                    >
                      {place.category === "Hotel" || place.category === "Alojamento" || place.category === "Hospedaria"
                        ? "Reservar quarto"
                        : place.category === "Restaurante"
                        ? "Reservar mesa"
                        : place.category === "Atividade"
                        ? "Reservar passeio"
                        : "Reservar"}
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

        {message.uiComponent === "progress_steps" && message.payload?.progress_steps && (
          <div className="mt-4 rounded-3xl border border-slate-200 bg-slate-50 p-4 text-slate-900 shadow-sm">
            <div className="mb-3 text-sm font-semibold text-slate-900">Acompanhe o progresso</div>
            <div className="space-y-3">
              {message.payload.progress_steps.map((step, index) => (
                <div
                  key={`${step.title}-${index}`}
                  className="flex items-start gap-3 rounded-2xl border border-slate-200 bg-white p-3"
                >
                  <div className="mt-0.5 h-7 w-7 flex-shrink-0 rounded-full bg-slate-100 text-center text-xs font-semibold leading-7 text-slate-500">
                    {step.completed ? "✓" : "…"}
                  </div>
                  <div>
                    <p className="font-semibold text-slate-900">{step.title}</p>
                    {step.subtitle && <p className="text-xs text-slate-500">{step.subtitle}</p>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {message.uiComponent === "reservation_card" && message.payload?.reservation && (
          <div className="mt-4 overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
            {message.payload.reservation.photo_url && (
              <img src={message.payload.reservation.photo_url} alt={message.payload.reservation.name} className="h-44 w-full object-cover" />
            )}
            <div className="space-y-3 p-4 text-slate-900">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <h3 className="text-lg font-semibold">{message.payload.reservation.name}</h3>
                  <p className="text-xs text-slate-500">{message.payload.reservation.status}</p>
                </div>
                <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-700">
                  Confirmado
                </span>
              </div>
              <div className="grid gap-2 text-sm text-slate-600">
                <p>📅 {message.payload.reservation.checkin} – {message.payload.reservation.checkout}</p>
                <p>👥 {message.payload.reservation.guests}</p>
                <p>🔖 Código de reserva: {message.payload.reservation.code}</p>
              </div>
              {message.payload.reservation.cta && (
                <button
                  type="button"
                  className="w-full rounded-full bg-emerald-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-emerald-700"
                >
                  {message.payload.reservation.cta}
                </button>
              )}
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

        {message.uiComponent === "map_view" && message.payload?.driver_selected && (
          <div className="mt-4 overflow-hidden rounded-3xl border border-slate-200 bg-slate-50 p-0 shadow-sm">
            <div className="p-4 text-slate-900">
              <p className="font-semibold">Mapa ativado</p>
              <p className="text-xs text-slate-500">A rota do Driver-Guide está disponível abaixo.</p>
            </div>
            <div className="h-64">
              <div className="h-full w-full rounded-b-3xl overflow-hidden">
                <TripMap position={inlineMapPosition} />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
