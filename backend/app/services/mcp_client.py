from __future__ import annotations

import httpx
from pydantic import BaseModel


class TouristLocation(BaseModel):
    lat: float
    lon: float


class DriverSummary(BaseModel):
    id: int
    nome: str
    classificacao: float | None
    idiomas: list[str]
    distancia: float


class MCPClient:
    def __init__(self, base_url: str = "http://localhost:8081") -> None:
        self.base_url = base_url.rstrip("/")

    def find_drivers(
        self,
        place_id: int,
        tourist_location: TouristLocation,
        language: str,
    ) -> list[DriverSummary]:
        url = f"{self.base_url}/tools/find_drivers"
        payload = {
            "place_id": place_id,
            "tourist_location": tourist_location.dict(),
            "language": language,
        }
        response = httpx.post(url, json=payload, timeout=15.0)
        response.raise_for_status()
        raw = response.json()
        return [DriverSummary(**item) for item in raw]
