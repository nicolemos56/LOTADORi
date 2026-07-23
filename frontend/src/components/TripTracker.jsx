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

  return null;
}
