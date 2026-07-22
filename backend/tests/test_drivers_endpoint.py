from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app


def test_drivers_endpoint_calls_travel_agent_service() -> None:
    expected_drivers = [
        {
            "id": 1,
            "nome": "Carlos",
            "classificacao": 4.9,
            "idiomas": ["Português", "Inglês"],
            "distancia": 3.7,
        }
    ]

    with patch("app.routers.chat.agent_service.get_drivers", return_value=expected_drivers):
        client = TestClient(app)
        response = client.get(
            "/drivers",
            params={"place_id": 1, "lat": -8.839, "lon": 13.289, "language": "Português"},
        )

    assert response.status_code == 200
    assert response.json() == {"drivers": expected_drivers}
