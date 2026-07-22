import asyncio
from collections import defaultdict
from typing import Any

from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect


class TripConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[str, list[WebSocket]] = defaultdict(list)
        self.simulation_tasks: dict[str, asyncio.Task[None]] = {}

    async def connect(self, trip_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[trip_id].append(websocket)

    def disconnect(self, trip_id: str, websocket: WebSocket) -> None:
        connections = self.active_connections.get(trip_id)
        if not connections:
            return
        if websocket in connections:
            connections.remove(websocket)
        if not connections:
            self.active_connections.pop(trip_id, None)
            task = self.simulation_tasks.pop(trip_id, None)
            if task and not task.done():
                task.cancel()

    async def broadcast(self, trip_id: str, message: dict[str, Any]) -> None:
        connections = list(self.active_connections.get(trip_id, []))
        for connection in connections:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                self.disconnect(trip_id, connection)
            except Exception:
                self.disconnect(trip_id, connection)

    def start_simulation(self, trip_id: str) -> None:
        if trip_id in self.simulation_tasks:
            return
        self.simulation_tasks[trip_id] = asyncio.create_task(self._simulate_trip(trip_id))

    async def _simulate_trip(self, trip_id: str) -> None:
        # Simula a atualização de posição do driver-guide enquanto houver clientes conectados.
        coordinates = [
            {"lat": -8.8390, "lon": 13.2890},
            {"lat": -8.8386, "lon": 13.2894},
            {"lat": -8.8382, "lon": 13.2898},
            {"lat": -8.8378, "lon": 13.2902},
            {"lat": -8.8374, "lon": 13.2906},
        ]
        index = 0

        try:
            while self.active_connections.get(trip_id):
                payload = {
                    "trip_id": trip_id,
                    "lat": coordinates[index]["lat"],
                    "lon": coordinates[index]["lon"],
                    "status": "moving",
                    "step": index + 1,
                }
                await self.broadcast(trip_id, payload)

                index = (index + 1) % len(coordinates)
                await asyncio.sleep(2.0)
        except asyncio.CancelledError:
            return
