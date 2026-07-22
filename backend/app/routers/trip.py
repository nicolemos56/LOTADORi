from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.websocket_manager import TripConnectionManager

router = APIRouter(tags=["trip"])
manager = TripConnectionManager()


@router.websocket("/ws/trip/{trip_id}")
async def trip_updates(websocket: WebSocket, trip_id: str) -> None:
    await manager.connect(trip_id, websocket)
    manager.start_simulation(trip_id)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(trip_id, websocket)
    except Exception:
        manager.disconnect(trip_id, websocket)
