from __future__ import annotations

from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from sqlalchemy import func

from app.core.database import SessionLocal
from app.models.driver import Driver
from app.models.place import Place


class TouristLocation(BaseModel):
    lat: float = Field(..., ge=-90.0, le=90.0)
    lon: float = Field(..., ge=-180.0, le=180.0)


class FindDriversRequest(BaseModel):
    place_id: int
    tourist_location: TouristLocation
    language: str = Field(..., min_length=2)

    @validator("language")
    def normalize_language(cls, value: str) -> str:
        return value.strip().title()


class DriverResponse(BaseModel):
    id: int
    nome: str
    classificacao: float | None
    idiomas: list[str]
    distancia: float


class MCPServer:
    def __init__(self) -> None:
        self.app = FastAPI(
            title="LOTADORi MCP Server",
            description="Servidor MCP para ferramentas geoespaciais de driver-guides.",
            version="0.1.0",
        )
        self._register_routes()

    def _register_routes(self) -> None:
        self.app.post("/tools/find_drivers", response_model=list[DriverResponse])(
            self._find_drivers_endpoint
        )

    async def _find_drivers_endpoint(self, request: FindDriversRequest) -> list[DriverResponse]:
        return self.find_drivers(
            place_id=request.place_id,
            tourist_location=request.tourist_location,
            language=request.language,
        )

    @staticmethod
    def _create_point(lat: float, lon: float):
        return func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)

    def find_drivers(
        self,
        place_id: int,
        tourist_location: TouristLocation,
        language: str,
    ) -> list[DriverResponse]:
        with SessionLocal() as session:
            if place_id is not None:
                place = session.get(Place, place_id)
                if place is None:
                    raise HTTPException(status_code=404, detail="Place not found")

            user_point = self._create_point(
                tourist_location.lat,
                tourist_location.lon,
            )

            max_distance_meters = 25000
            query = (
                session.query(
                    Driver.id,
                    Driver.name,
                    Driver.rating.label("classificacao"),
                    Driver.languages,
                    func.ST_Distance(Driver.location, user_point).label("distancia_metros"),
                )
                .filter(Driver.languages.any(language))
                .filter(func.ST_DWithin(Driver.location, user_point, max_distance_meters))
                .order_by(func.ST_Distance(Driver.location, user_point))
                .limit(10)
            )

            results: list[DriverResponse] = []
            for row in query:
                results.append(
                    DriverResponse(
                        id=row.id,
                        nome=row.name,
                        classificacao=float(row.classificacao)
                        if row.classificacao is not None
                        else None,
                        idiomas=row.languages or [],
                        distancia=round(float(row.distancia_metros) / 1000.0, 2),
                    )
                )

            return results


mcp_server = MCPServer().app


if __name__ == "__main__":
    uvicorn.run("app.services.mcp_server:mcp_server", host="0.0.0.0", port=8081, reload=False)
