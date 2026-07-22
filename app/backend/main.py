from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Kalawenda API", version="0.1.0")


class TouristRequest(BaseModel):
    message: str


class Recommendation(BaseModel):
    title: str
    description: str
    category: str


class Guide(BaseModel):
    name: str
    rating: float
    specialty: str
    eta_minutes: int


class Place(BaseModel):
    name: str
    description: str
    lat: float
    lng: float
    category: str


class TouristResponse(BaseModel):
    intent: str
    message: str
    recommendations: List[Recommendation]
    next_action: str | None = None
    image_url: str | None = None


class PlacesResponse(BaseModel):
    places: List[Place]


class GuidesResponse(BaseModel):
    guides: List[Guide]


@app.get("/")
def read_root():
    return {"message": "Kalawenda API ready"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/places", response_model=PlacesResponse)
def list_places():
    return PlacesResponse(
        places=[
            Place(
                name="Praça Central",
                description="Café, artesanato e início de passeios culturais.",
                lat=-8.839,
                lng=13.289,
                category="cultura",
            ),
            Place(
                name="Trilha da Vista",
                description="Rota curta com miradouros e vistas naturais.",
                lat=-8.845,
                lng=13.296,
                category="natureza",
            ),
            Place(
                name="Mercado do Bairro",
                description="Gastronomia local e música tradicional.",
                lat=-8.833,
                lng=13.285,
                category="gastronomia",
            ),
        ]
    )


@app.get("/guides", response_model=GuidesResponse)
def list_guides():
    return GuidesResponse(
        guides=[
            Guide(name="Ana da Serra", rating=4.9, specialty="Trilhas e cultura", eta_minutes=8),
            Guide(name="Miguel dos Bairros", rating=4.8, specialty="Gastronomia e histórias", eta_minutes=11),
            Guide(name="Sérgio do Porto", rating=4.7, specialty="Passeios urbanos", eta_minutes=6),
        ]
    )


@app.post("/intent", response_model=TouristResponse)
def detect_intent(request: TouristRequest):
    message = request.message.lower()

    if any(term in message for term in ["oi", "olá", "bom dia", "boa tarde", "boa noite", "hello", "hi"]):
        return TouristResponse(
            intent="greet",
            message="Olá! Eu sou a Kalawenda, sua assistente turística em Angola. Posso ajudar a descobrir lugares, guias e rotas com base na sua intenção.",
            recommendations=[
                Recommendation(
                    title="Explorar destinos",
                    description="Posso sugerir pontos turísticos e experiências locais.",
                    category="general",
                )
            ],
            next_action="ask_intent",
            image_url=None,
        )

    if any(term in message for term in ["guia", "guide", "motorista", "driver", "taxi", "taxista"]):
        return TouristResponse(
            intent="find_guide",
            message="Encontrei driver-guides locais com boas avaliações para o seu perfil. Posso mostrar uma lista para você escolher.",
            recommendations=[
                Recommendation(
                    title="Ana da Serra",
                    description="Guia local especializada em trilhas e cultura popular.",
                    category="guide",
                ),
                Recommendation(
                    title="Miguel dos Bairros",
                    description="Conhece os melhores pontos de comida e histórias da cidade.",
                    category="guide",
                ),
            ],
            next_action="show_guides",
            image_url=None,
        )

    if any(term in message for term in ["kalandula", "cachoeiras", "lugar", "destino", "local", "ponto", "turístico", "rotas", "visitar"]):
        if "kalandula" in message:
            return TouristResponse(
                intent="show_place",
                message="Kalandula é um destino encantador, conhecido pelas suas cachoeiras e pela beleza natural. Pode ser uma excelente escolha para um passeio relaxante.",
                recommendations=[
                    Recommendation(
                        title="Cachoeiras de Kalandula",
                        description="Uma das paisagens mais marcantes de Angola para quem gosta de natureza.",
                        category="place",
                    )
                ],
                next_action="offer_guides",
                image_url="https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=900&q=80",
            )

        return TouristResponse(
            intent="find_place",
            message="Estas são sugestões de locais e rotas que combinam com a sua procura.",
            recommendations=[
                Recommendation(
                    title="Praça Central",
                    description="Ponto ideal para começar o passeio com cafés e artesanato local.",
                    category="place",
                ),
                Recommendation(
                    title="Trilha da Vista",
                    description="Rota curta com paisagens e paragens culturais para uma tarde relaxada.",
                    category="place",
                ),
            ],
            next_action="show_map",
            image_url=None,
        )

    return TouristResponse(
        intent="general",
        message="Posso ajudar a descobrir destinos, rotas e guias locais em poucos segundos.",
        recommendations=[
            Recommendation(
                title="Explorar destinos",
                description="Sugiro locais com boa combinação entre cultura, gastronomia e vistas.",
                category="general",
            )
        ],
        next_action="ask_intent",
        image_url=None,
    )
