import { useEffect } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";

function MapUpdater({ position }) {
  const map = useMap();

  useEffect(() => {
    if (position) {
      map.setView(position, map.getZoom(), { animate: true });
    }
  }, [map, position]);

  return null;
}

export default function TripMap({ position }) {
  const defaultCenter = [-8.839, 13.289];

  return (
    <div className="mt-4 h-72 overflow-hidden rounded-3xl border border-slate-200">
      <MapContainer
        center={position ?? defaultCenter}
        zoom={15}
        scrollWheelZoom={false}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {position && (
          <>
            <CircleMarker
              center={position}
              radius={10}
              pathOptions={{ color: "#10b981", fillColor: "#10b981", fillOpacity: 0.8 }}
            >
              <Popup>Driver-guide em movimento</Popup>
            </CircleMarker>
            <MapUpdater position={position} />
          </>
        )}
      </MapContainer>
    </div>
  );
}
