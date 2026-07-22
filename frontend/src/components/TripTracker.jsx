import { useEffect, useState } from "react";
import { useChatStore } from "../store/chatStore.js";
import TripMap from "./TripMap.jsx";

export default function TripTracker({ tripId }) {
  const [status, setStatus] = useState("desconectado");
  const [error, setError] = useState(null);
  const setDriverLocation = useChatStore((state) => state.setDriverLocation);
  const location = useChatStore((state) => state.driverLocation);

  useEffect(() => {
    if (!tripId) return;

    const apiUrl = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
    const wsProtocol = apiUrl.startsWith("https") ? "wss" : "ws";
    const wsHost = apiUrl.replace(/^https?:\/\//, "");
    const socket = new WebSocket(`${wsProtocol}://${wsHost}/ws/trip/${tripId}`);

    setStatus("conectando");
    setError(null);

    socket.onopen = () => {
      setStatus("conectado");
      socket.send("ready");
    };

    socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        setDriverLocation(payload);
      } catch (err) {
        setError("Erro ao processar a atualização de localização");
      }
    };

    socket.onclose = () => setStatus("desconectado");
    socket.onerror = () => setError("Falha na conexão WebSocket");

    return () => socket.close();
  }, [tripId, setDriverLocation]);

  return (
    <div className="border-t border-slate-200 bg-slate-50 p-4 text-sm text-slate-700">
      <div className="mb-2 flex items-center justify-between gap-3">
        <span className="font-semibold">Trip tracker</span>
        <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-700">
          {status}
        </span>
      </div>
      <p className="text-xs text-slate-500">Trip ID: {tripId}</p>
      {error && <p className="mt-2 text-sm text-red-600">{error}</p>}

      {location ? (
        <div className="mt-3 grid gap-1 text-slate-700">
          <p>Lat: {location.lat}</p>
          <p>Lon: {location.lon}</p>
          <p>Status: {location.status}</p>
          <p>Step: {location.step}</p>
        </div>
      ) : (
        <p className="mt-3 text-slate-500">Aguardar atualizações de localização do driver...</p>
      )}

      <TripMap position={location ? [location.lat, location.lon] : null} />
    </div>
  );
}
