from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import generate_reply
from app.services.travel_agent import TravelAgentService

router = APIRouter(tags=["chat"])
agent_service = TravelAgentService()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    result = agent_service.handle_message(request.message, request.session_id)
    return ChatResponse(**result)


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
