import { useEffect, useRef, useState } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";

function MapUpdater({ position }) {
  const map = useMap();

  useEffect(() => {
    const target = position ?? [-11.202, 17.874];
    map.setView(target, map.getZoom(), { animate: false });
    setTimeout(() => {
      try { map.invalidateSize(); } catch (e) {}
    }, 100);
  }, [map, position]);

  return null;
}

export default function TripMap({ position }) {
  const defaultCenter = [-11.202, 17.874]; // Centro de Angola
  const mapPosition = position ?? defaultCenter;

  return (
    <div className="h-64 w-full overflow-hidden rounded-3xl bg-slate-950 shadow-inner">
      <MapContainer
        center={mapPosition}
        zoom={7}
        scrollWheelZoom={true}
        style={{ height: '100%', width: '100%' }}
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
