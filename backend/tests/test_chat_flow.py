from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_chat_welcome_flow_returns_guided_response():
    response = client.post("/chat", json={"message": "Olá"})

    assert response.status_code == 200
    body = response.json()

    assert body["reply"]
    assert body["ui_component"] == "city_prompt"
    assert body["session_id"]


def test_places_endpoint_filters_by_interests():
    response = client.get("/places", params={"city": "Luanda", "interests": "História,Natureza"})

    assert response.status_code == 200
    body = response.json()

    assert body["city"] == "Luanda"
    assert body["places"]
    assert any(place["name"] == "Ilha do Mussulo" for place in body["places"])
