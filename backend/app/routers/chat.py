from fastapi import APIRouter, Body

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import generate_reply
from app.services.travel_agent import TravelAgentService

router = APIRouter(tags=["chat"])
agent_service = TravelAgentService()


@router.post("/chat", response_model=ChatResponse)
def chat(body: dict = Body(...)) -> ChatResponse:
    message = body.get("message") or body.get("text")
    session_id = body.get("session_id") if "session_id" in body else body.get("sessionId")
    request = ChatRequest(message=message, session_id=session_id)
    result = agent_service.handle_message(request.message, request.session_id)
    return ChatResponse(**result)



@router.post("/ping")
def ping(body: dict = Body(...)):
    """Simple connectivity endpoint used by the frontend test helper.
    Expects a JSON body like { "message": "Ola servidor" } and replies
    with { "reply": "Ola frontend" } to validate round-trip.
    """
    message = body.get("message") if isinstance(body, dict) else None
    if isinstance(message, str) and message.strip() == "Ola servidor":
        return {"reply": "Ola frontend"}

    return {"reply": "pong", "received": message}


@router.post("/test-connection")
def test_connection(body: dict = Body(...)):
    """Dedicated JSON test endpoint used by the frontend 'Testar ligação' button.
    Always returns a JSON object with a friendly message and echoes the input.
    """
    message = body.get("message") if isinstance(body, dict) else None
    return {"status": "ok", "message_received": message, "reply": "Ola frontend"}


@router.get("/places")
def get_places(city: str | None = None, interests: str | None = None):
    interests_list = [item.strip() for item in interests.split(",") if item.strip()] if interests else []
    return {
        "city": city or "Luanda",
        "places": agent_service._get_places(city, interests_list),
    }


@router.get("/drivers")
def get_drivers(
    place_id: int,
    lat: float,
    lon: float,
    language: str,
):
    drivers = agent_service.get_drivers(
        place_id=place_id,
        tourist_location={"lat": lat, "lon": lon},
        language=language,
    )
    return {"drivers": drivers}
