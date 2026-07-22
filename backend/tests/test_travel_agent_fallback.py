from unittest.mock import patch

from app.services.travel_agent import TravelAgentService


def test_travel_agent_uses_internal_bot_on_gemini_error() -> None:
    agent = TravelAgentService()
    session_id = "test-session"
    agent.get_or_create_session(session_id)

    with patch.object(agent, "_call_gemini", return_value="Erro Gemini (500): Internal Server Error"):
        result = agent.handle_message("Sim", session_id=session_id)

    assert result["reply"].startswith(
        "A API de IA está temporariamente indisponível"
    ) or result["reply"].startswith(
        "Desculpa, estou com um problema temporário na API de IA."
    )
    assert result["ui_component"] in {"city_prompt", "interest_prompt", "place_cards", "place_detail"}
