from fastapi.testclient import TestClient
from unittest.mock import patch

from app.services.mcp_server import MCPServer


def test_mcp_server_find_drivers_route_returns_data() -> None:
    app = MCPServer().app
    expected_drivers = [
        {
            "id": 1,
            "nome": "Carlos",
            "classificacao": 4.9,
            "idiomas": ["Português", "Inglês"],
            "distancia": 3.7,
        }
    ]

    with patch("app.services.mcp_server.MCPServer.find_drivers", return_value=expected_drivers):
        client = TestClient(app)
        response = client.post(
            "/tools/find_drivers",
            json={
                "place_id": 1,
                "tourist_location": {"lat": -8.839, "lon": 13.289},
                "language": "Português",
            },
        )

    assert response.status_code == 200
    assert response.json() == expected_drivers
