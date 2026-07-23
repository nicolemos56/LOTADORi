from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx
from sqlalchemy import func
from sqlalchemy.exc import OperationalError

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.driver import Driver
from app.models.place import Place
from app.services.mcp_client import MCPClient, TouristLocation


@dataclass
class TravelSession:
    session_id: str
    stage: str = "welcome"
    city: str | None = None
    interests: list[str] = field(default_factory=list)
    first_time: bool | None = None
    selected_place: dict[str, Any] | None = None
    available_drivers: list[dict[str, Any]] = field(default_factory=list)
    selected_driver: dict[str, Any] | None = None
    booking_options: list[dict[str, Any]] = field(default_factory=list)
    selected_booking_option: dict[str, Any] | None = None
    messages: list[dict[str, str]] = field(default_factory=list)


class TravelAgentService:
    def __init__(self) -> None:
        self._sessions: dict[str, TravelSession] = {}
        self.mcp_client = MCPClient()
        self.gemini_api_key = settings.gemini_api_key or settings.groq_api_key or settings.openai_api_key
        self.gemini_model = "gemini-3.5-flash"
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/interactions"
        self.system_prompt = (
            "Tu és o Lotadori, um assistente de viagem angolano caloroso e acolhedor. "
            "Responde sempre em português e mantém a persona. "
            "Guia o turista pelas fases do fluxo: cidade, perfil, recomendações e apresentação de destinos. "
            "Quando o utilizador escolher Mussulo, termina com: 'Deseja que encontre um Driver-Guide certificado para acompanhá-lo?'."
        )

    def get_or_create_session(self, session_id: str | None = None) -> TravelSession:
        if session_id and session_id in self._sessions:
            return self._sessions[session_id]

        new_id = session_id or f"session-{len(self._sessions) + 1}"
        session = TravelSession(session_id=new_id)
        self._sessions[new_id] = session
        return session

    def handle_message(self, message: str, session_id: str | None = None) -> dict[str, Any]:
        session = self.get_or_create_session(session_id)
        text = message.strip()

        if not text:
            return {
                "reply": "Escreve o nome da tua cidade para eu te ajudar.",
                "ui_component": "city_prompt",
                "payload": {},
                "session_id": session.session_id,
            }

        if session.stage == "driver_list":
            selected_driver = self._find_driver_by_name(text, session.available_drivers)
            if selected_driver:
                session.selected_driver = selected_driver
                session.stage = "driver_selected"
                return {
                    "reply": (
                        f"Ótima escolha! O Driver-Guide {selected_driver['name']} está pronto para te acompanhar. "
                        "Vou abrir o mapa e mostrar a posição em tempo real."
                    ),
                    "ui_component": "map_view",
                    "payload": {
                        "driver_selected": True,
                        "trip_id": session.session_id,
                        "driver": selected_driver,
                    },
                    "session_id": session.session_id,
                }

        if session.stage == "booking_options":
            selected_place = self._find_booking_option(text, session.booking_options)
            if selected_place:
                session.selected_booking_option = selected_place
                session.stage = "booking_confirmed"
                reservation = self._mock_booking_reservation(selected_place)
                return {
                    "reply": (
                        f"Ótima escolha! Encontrei disponibilidade para {selected_place['name']}. "
                        "A reserva está pronta para ser confirmada."
                    ),
                    "ui_component": "reservation_card",
                    "payload": {"reservation": reservation},
                    "session_id": session.session_id,
                }

        if self._is_guide_request(text):
            drivers = self._fetch_nearby_drivers_from_db(session_data=session, limit=5)
            used_fallback = False
            if not drivers:
                drivers = self._get_sample_drivers()
                used_fallback = True

            session.stage = "driver_list"
            session.available_drivers = drivers
            reply = (
                "Perfeito, encontrei estes Driver-Guides próximos para ti:\n"
                if not used_fallback
                else "Não consegui carregar a lista de motoristas locais, mas aqui tens algumas sugestões de Driver-Guides:\n"
            )
            reply += self._format_drivers_for_bot(drivers)
            return {
                "reply": reply,
                "ui_component": "driver_cards",
                "payload": {"drivers": drivers},
                "session_id": session.session_id,
            }

        if self._is_booking_request(text):
            booking_options = self._get_booking_options(text)
            if booking_options:
                session.stage = "booking_options"
                session.booking_options = booking_options
                if self._is_hotel_request(text):
                    reply_prefix = (
                        "Encontrei hotéis práticos para a tua estadia. "
                        "Usa os botões abaixo para Ver detalhes, Reservar ou dizer Quero ir para este lugar."
                    )
                elif self._is_restaurant_request(text):
                    reply_prefix = (
                        "Encontrei restaurantes ótimos para jantar. "
                        "Usa os botões abaixo para Ver detalhes, Reservar ou dizer Quero ir para este lugar."
                    )
                elif self._is_activity_request(text):
                    reply_prefix = (
                        "Encontrei atividades e passeios interessantes. "
                        "Usa os botões abaixo para Ver detalhes, Reservar ou dizer Quero ir para este lugar."
                    )
                else:
                    reply_prefix = (
                        "Encontrei estas opções disponíveis. "
                        "Usa os botões abaixo para Ver detalhes, Reservar ou dizer Quero ir para este lugar."
                    )
                return {
                    "reply": reply_prefix,
                    "ui_component": "place_cards",
                    "payload": {"places": booking_options},
                    "session_id": session.session_id,
                }

            return {
                "reply": "Desculpa, não encontrei opções disponíveis no momento. Podes tentar novamente?",
                "ui_component": "interest_prompt",
                "payload": {"city": session.city, "interests": session.interests},
                "session_id": session.session_id,
            }

        if session.stage == "welcome":
            session.stage = "ask_city"
            reply = self._generate_gemini_reply(
                session,
                (
                    f"O utilizador disse: '{text}'.\n"
                    "Inicia a conversa em português, acolhendo-o e a perguntar em qual cidade está."
                ),
            )
            return {
                "reply": reply,
                "ui_component": "city_prompt",
                "payload": {},
                "session_id": session.session_id,
            }

        if session.stage == "ask_city":
            session.city = text
            session.stage = "ask_profile"
            reply = self._generate_gemini_reply(
                session,
                f"O utilizador informou que está em {text}. Responde em português, pergunta se é a primeira vez em Angola e sugere que escolha interesses: História, Gastronomia, Natureza, Vida Noturna ou Praias.",
            )
            return {
                "reply": reply,
                "ui_component": "interest_prompt",
                "payload": {"city": session.city, "interests": []},
                "session_id": session.session_id,
            }

        if session.stage == "ask_profile":
            interests = self._extract_interests(text)
            if not interests:
                reply = self._generate_gemini_reply(
                    session,
                    "O utilizador não escolheu um interesse claro. Pede que escolha um ou mais interesses para poder recomendar locais mais certeiros.",
                )
                return {
                    "reply": reply,
                    "ui_component": "interest_prompt",
                    "payload": {"city": session.city, "interests": []},
                    "session_id": session.session_id,
                }

            session.interests = interests
            session.stage = "recommend"
            places = self._get_places(session.city, interests)
            reply = self._generate_gemini_reply(
                session,
                (
                    f"O utilizador escolheu os interesses: {', '.join(interests)}. "
                    "Apresenta uma recomendação calorosa em português com base nestes locais. "
                    "Menciona pelo menos três locais, incluindo nome, classificação, duração, custo médio, distância e melhor horário."
                ),
                places=places,
            )
            return {
                "reply": reply,
                "ui_component": "place_cards",
                "payload": {"city": session.city, "interests": session.interests, "places": places},
                "session_id": session.session_id,
            }

        if session.stage == "recommend":
            if self._is_place_selection(text):
                place = self._find_place(text)
                session.selected_place = place
                session.stage = "offer_driver"
                reply = self._generate_gemini_reply(
                    session,
                    (
                        f"O utilizador escolheu {place['name']}. "
                        "Fala deste destino em português, destaca os principais motivos para visitar e, se for Mussulo, pergunta se ele deseja um Driver-Guide certificado."
                    ),
                    places=[place],
                )
                return {
                    "reply": reply,
                    "ui_component": "place_detail",
                    "payload": {"selected_place": place["name"], "details": place},
                    "session_id": session.session_id,
                }

            reply = self._generate_gemini_reply(
                session,
                "O utilizador respondeu com algo diferente de um local. Pede para escolher um dos locais recomendados ou um novo interesse.",
            )
            return {
                "reply": reply,
                "ui_component": "interest_prompt",
                "payload": {"city": session.city, "interests": session.interests},
                "session_id": session.session_id,
            }

        if session.stage == "offer_driver":
            normalized = text.strip().lower()
            if normalized in {"sim", "claro", "ok", "ok!", "sim.", "sim!"}:
                drivers = self._fetch_nearby_drivers_from_db(session_data=session, limit=5)
                used_fallback = False
                if not drivers:
                    drivers = self._get_sample_drivers()
                    used_fallback = True

                if drivers:
                    session.stage = "driver_list"
                    session.available_drivers = drivers
                    reply = (
                        "Perfeito, encontrei estes Driver-Guides próximos para ti:\n"
                        if not used_fallback
                        else "Não consegui carregar a lista de motoristas locais, mas aqui tens algumas sugestões de Driver-Guides:\n"
                    )
                    reply += self._format_drivers_for_bot(drivers)
                    return {
                        "reply": reply,
                        "ui_component": "driver_cards",
                        "payload": {"drivers": drivers},
                        "session_id": session.session_id,
                    }
                return {
                    "reply": (
                        "Ainda não tenho motoristas disponíveis para esse destino. "
                        "Por favor, tenta novamente mais tarde ou escolhe outro local."
                    ),
                    "ui_component": "interest_prompt",
                    "payload": {"city": session.city, "interests": session.interests},
                    "session_id": session.session_id,
                }

            if normalized in {"não", "nao", "não obrigado", "nao obrigado", "não, obrigado", "nao, obrigado"}:
                session.stage = "recommend"
                return {
                    "reply": (
                        "Está bem. Sem problema: diz-me para onde queres ir agora. "
                        "Posso sugerir outro destino ou um novo interesse."
                    ),
                    "ui_component": "interest_prompt",
                    "payload": {"city": session.city, "interests": session.interests},
                    "session_id": session.session_id,
                }

            reply = self._generate_gemini_reply(
                session,
                "O utilizador respondeu à oferta de driver e precisa de uma resposta com ação: sim para drivers ou não para recusar.",
            )
            return {
                "reply": reply,
                "ui_component": "interest_prompt",
                "payload": {"city": session.city, "interests": session.interests},
                "session_id": session.session_id,
            }

        if session.stage == "driver_list":
            selected_driver = self._find_driver_by_name(text, session.available_drivers)
            if selected_driver:
                session.selected_driver = selected_driver
                session.stage = "driver_selected"
                return {
                    "reply": (
                        f"Ótima escolha! O Driver-Guide {selected_driver['name']} está pronto para te acompanhar. "
                        "Vou abrir o mapa e mostrar a posição em tempo real."
                    ),
                    "ui_component": "map_view",
                    "payload": {
                        "driver_selected": True,
                        "trip_id": session.session_id,
                        "driver": selected_driver,
                    },
                    "session_id": session.session_id,
                }

        if session.stage == "booking_options":
            selected_place = self._find_booking_option(text, session.booking_options)
            if selected_place:
                session.selected_booking_option = selected_place
                session.stage = "booking_confirmed"
                reservation = self._mock_booking_reservation(selected_place)
                return {
                    "reply": (
                        f"Ótima escolha! Encontrei disponibilidade para {selected_place['name']}. "
                        "A reserva está pronto para ser confirmada."
                    ),
                    "ui_component": "reservation_card",
                    "payload": {"reservation": reservation},
                    "session_id": session.session_id,
                }

            return {
                "reply": (
                    "Não reconheci esse Driver-Guide. Por favor, escolhe um dos motoristas sugeridos na lista."
                ),
                "ui_component": "driver_cards",
                "payload": {"drivers": session.available_drivers},
                "session_id": session.session_id,
            }

        reply = self._generate_gemini_reply(
            session,
            "Continua a conversa em português e ajuda o utilizador a escolher um local ou interesse.",
        )
        return {
            "reply": reply,
            "ui_component": "interest_prompt",
            "payload": {"city": session.city, "interests": session.interests},
            "session_id": session.session_id,
        }

    def get_drivers(
        self,
        place_id: int,
        tourist_location: dict[str, float],
        language: str,
    ) -> list[dict[str, Any]]:
        location = TouristLocation(**tourist_location)
        drivers = self.mcp_client.find_drivers(
            place_id=place_id,
            tourist_location=location,
            language=language,
        )
        return [driver.dict() for driver in drivers]

    def _generate_gemini_reply(
        self,
        session: TravelSession,
        user_content: str,
        places: list[dict[str, Any]] | None = None,
    ) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            *session.messages,
            {"role": "user", "content": user_content},
        ]

        if places:
            places_description = self._format_places_for_prompt(places)
            messages.append({
                "role": "user",
                "content": (
                    "Usa estas descrições de locais para criar uma resposta mais rica:\n"
                    f"{places_description}"
                ),
            })

        reply = self._call_gemini(messages)
        if self._is_gemini_error(reply):
            reply = self._internal_bot_reply(session, user_content, places)

        session.messages.append({"role": "user", "content": user_content})
        if places:
            session.messages.append({"role": "user", "content": places_description})
        session.messages.append({"role": "assistant", "content": reply})
        return reply

    def _generate_groq_reply(self, session: TravelSession, user_content: str) -> str:
        return self._generate_gemini_reply(session, user_content)

    def _find_driver_by_name(self, text: str, drivers: list[dict[str, Any]]) -> dict[str, Any] | None:
        normalized = text.strip().lower()
        for driver in drivers:
            name = driver.get("name", "").lower()
            if name == normalized or name in normalized or normalized in name:
                return driver
        return None

    def _call_gemini(self, messages: list[dict[str, str]]) -> str:
        if not self.gemini_api_key:
            return (
                "Ainda não tenho a chave Gemini configurada. Por favor, define Gemini_API_KEY no ficheiro .env."
            )

        prompt = self._build_prompt(messages)
        payload = {
            "model": self.gemini_model,
            "input": prompt,
        }
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.gemini_api_key,
        }

        try:
            response = httpx.post(self.gemini_url, headers=headers, json=payload, timeout=30.0)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict):
                output_text = data.get("output_text") or data.get("outputText")
                if isinstance(output_text, str) and output_text.strip():
                    return output_text.strip()

                # Interactions may return nested steps and model_output content
                steps = data.get("steps") or []
                if isinstance(steps, list):
                    texts = []
                    for step in steps:
                        if not isinstance(step, dict):
                            continue
                        if step.get("type") != "model_output":
                            continue
                        for content in step.get("content", []):
                            if not isinstance(content, dict):
                                continue
                            text = content.get("text") or content.get("output_text")
                            if isinstance(text, str) and text.strip():
                                texts.append(text.strip())
                    if texts:
                        return "\n".join(texts)

                return str(data)
            return str(data)
        except httpx.HTTPStatusError as exc:
            return f"__GEMINI_ERROR__ Erro Gemini ({exc.response.status_code}): {exc.response.text[:200]}"
        except Exception as exc:
            return f"__GEMINI_ERROR__ {exc.__class__.__name__}: {exc}"

    def _is_gemini_error(self, reply: str) -> bool:
        if not isinstance(reply, str):
            return True
        return reply.startswith("__GEMINI_ERROR__") or "Erro Gemini" in reply or "Ainda estou a preparar" in reply

    def _internal_bot_reply(
        self,
        session: TravelSession,
        user_content: str,
        places: list[dict[str, Any]] | None = None,
    ) -> str:
        normalized = user_content.strip().lower()

        if session.stage in {"welcome", "ask_city"}:
            return (
                "Desculpa, estou com um problema temporário na API de IA. "
                "Vamos continuar sem a IA: diz-me a tua cidade para eu te ajudar."
            )

        if session.stage == "ask_profile":
            return (
                "A API de IA não está disponível agora, mas posso continuar. "
                "Qual o teu interesse principal: História, Gastronomia, Natureza, Vida Noturna ou Praias?"
            )

        if session.stage == "recommend":
            return (
                "A API de IA está temporariamente indisponível. "
                "Por favor, escolhe um dos locais recomendados ou um novo interesse para eu continuar."
            )

        if session.stage == "offer_driver":
            drivers = self._fetch_nearby_drivers_from_db(session_data=session, limit=3)
            if drivers:
                drivers_description = self._format_drivers_for_bot(drivers)
                return (
                    "A API de IA está temporariamente indisponível, mas consegui continuar com o meu bot. "
                    "Aqui estão alguns Driver-Guides próximos que posso sugerir agora:\n"
                    f"{drivers_description}"
                )
            return (
                "A API de IA está temporariamente indisponível e não encontrei drivers disponíveis agora. "
                "Tenta novamente daqui a pouco ou escolhe outro destino."
            )

        return (
            "Desculpa, estou com um problema temporário na API de IA. "
            "Vou continuar a ajudar-te com o meu bot interno. "
            "Precisas de um Driver-Guide certificado agora?"
        )

    def _fetch_nearby_drivers_from_db(
        self,
        session_data: TravelSession | None = None,
        limit: int = 3,
    ) -> list[dict[str, Any]]:
        origin = func.ST_SetSRID(func.ST_MakePoint(13.289, -8.839), 4326)

        if session_data and session_data.selected_place:
            place_name = session_data.selected_place.get("name")
            if place_name:
                try:
                    with SessionLocal() as session:
                        place = session.query(Place).filter(Place.name == place_name).first()
                        if place and place.location is not None:
                            origin = place.location
                except OperationalError:
                    return []

        try:
            with SessionLocal() as session:
                query = (
                    session.query(
                        Driver.id,
                        Driver.name,
                        Driver.rating,
                        Driver.languages,
                        Driver.trips_count,
                        Driver.base_price,
                        Driver.specialties,
                        func.ST_Distance(Driver.location, origin).label("distance_m"),
                    )
                    .order_by(func.ST_Distance(Driver.location, origin))
                    .limit(limit)
                )
                results = []
                for row in query:
                    results.append(
                        {
                            "id": row.id,
                            "name": row.name,
                            "rating": float(row.rating) if row.rating is not None else None,
                            "languages": row.languages or [],
                            "trips_count": row.trips_count,
                            "base_price": float(row.base_price) if row.base_price is not None else None,
                            "specialties": row.specialties or [],
                            "distance_km": round(float(row.distance_m) / 1000.0, 1),
                        }
                    )
                return results
        except OperationalError:
            return []

    def _get_sample_drivers(self) -> list[dict[str, Any]]:
        return [
            {
                "id": 0,
                "name": "Paulo Mendes",
                "rating": 4.9,
                "languages": ["Português", "Inglês"],
                "trips_count": 128,
                "base_price": 30.0,
                "specialties": ["Mussulo", "Tour histórico", "Natureza"],
                "distance_km": 2.5,
            },
            {
                "id": 1,
                "name": "Ana Costa",
                "rating": 4.8,
                "languages": ["Português", "Francês"],
                "trips_count": 94,
                "base_price": 28.0,
                "specialties": ["Museus", "Cidade", "Gastronomia"],
                "distance_km": 3.1,
            },
            {
                "id": 2,
                "name": "José Tavares",
                "rating": 4.7,
                "languages": ["Português", "Espanhol"],
                "trips_count": 110,
                "base_price": 26.0,
                "specialties": ["Miradouro", "Passeios culturais"],
                "distance_km": 4.0,
            },
        ]

    def _format_drivers_for_bot(self, drivers: list[dict[str, Any]]) -> str:
        lines = []
        for driver in drivers:
            price_display = (
                f"{driver['base_price']:.2f} USD base"
                if driver["base_price"] is not None
                else "Preço indisponível"
            )
            lines.append(
                f"{driver['name']} — {driver['rating'] or 'N/A'} ★ — {driver['trips_count']} viagens — "
                f"{', '.join(driver['languages'])} — {driver.get('distance_km', 'N/A')} km — "
                f"{price_display}"
            )
        return "\n".join(lines)

    def _build_prompt(self, messages: list[dict[str, str]]) -> str:
        lines = []
        for msg in messages:
            role = msg["role"].upper()
            lines.append(f"[{role}] {msg['content']}")
        return "\n".join(lines)

    def _format_places_for_prompt(self, places: list[dict[str, Any]]) -> str:
        formatted = []
        for place in places:
            formatted.append(
                (
                    f"Nome: {place['name']}; "
                    f"Categoria: {place['category']}; "
                    f"Avaliação: {place['rating']}; "
                    f"Duração: {place['visit_duration_minutes']} min; "
                    f"Custo médio: ${place['avg_cost']:.2f}; "
                    f"Distância: {place['distance_km']} km; "
                    f"Melhor horário: {place['best_time']}. "
                    f"Descrição: {place['description']}"
                )
            )
        return "\n".join(formatted)

    def _is_booking_request(self, text: str) -> bool:
        lower = text.lower()
        return any(key in lower for key in ["hotel", "alojamento", "reserva", "jantar", "restaurante", "comer", "dinner"])

    def _is_hotel_request(self, text: str) -> bool:
        lower = text.lower()
        return any(key in lower for key in ["hotel", "alojamento", "hospedagem", "pousada"])

    def _is_restaurant_request(self, text: str) -> bool:
        lower = text.lower()
        return any(key in lower for key in ["jantar", "restaurante", "restaurantes", "comer", "dinner"])

    def _is_guide_request(self, text: str) -> bool:
        lower = text.lower()
        return any(key in lower for key in ["guide", "driver", "guia", "guide-driver", "chamar guide", "chamar guia"])

    def _is_activity_request(self, text: str) -> bool:
        lower = text.lower()
        return any(key in lower for key in ["tour", "passeio", "atividade", "experiência", "tour guiado", "atividade"])

    def _get_booking_options(self, text: str) -> list[dict[str, Any]]:
        if self._is_hotel_request(text):
            return [
                {
                    "name": "Hotel Patriota",
                    "description": "Hotel confortável no coração de Luanda com pequeno-almoço incluído.",
                    "category": "Hotel",
                    "photo_url": "https://images.unsplash.com/photo-1501117716987-c8a8c4b8f254?auto=format&fit=crop&w=900&q=80",
                    "rating": 4.7,
                    "visit_duration_minutes": 1440,
                    "avg_cost": 120.0,
                    "distance_km": 2.5,
                    "best_time": "Check-in hoje",
                    "highlights": ["Wi-Fi", "Pequeno-almoço", "Piscina"],
                },
                {
                    "name": "Hotel Bahia Azul",
                    "description": "Alojamento boutique perto da marginal, ideal para uma estadia tranquila.",
                    "category": "Hotel",
                    "photo_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=900&q=80",
                    "rating": 4.6,
                    "visit_duration_minutes": 1440,
                    "avg_cost": 105.0,
                    "distance_km": 3.2,
                    "best_time": "Check-in hoje",
                    "highlights": ["Jacuzzi", "Café da manhã", "Localização central"],
                },
            ]
        if self._is_restaurant_request(text):
            return [
                {
                    "name": "Restaurante Kwanza",
                    "description": "Cozinha local premium com pratos tradicionais e ambiente refinado.",
                    "category": "Restaurante",
                    "photo_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=900&q=80",
                    "rating": 4.8,
                    "visit_duration_minutes": 120,
                    "avg_cost": 45.0,
                    "distance_km": 1.8,
                    "best_time": "Jantar hoje",
                    "highlights": ["Pratos locais", "Vinhos", "Ambiente romântico"],
                },
                {
                    "name": "Bistrô da Baía",
                    "description": "Experiência gastronômica com mariscos frescos e vista para o mar.",
                    "category": "Restaurante",
                    "photo_url": "https://images.unsplash.com/photo-1498654896293-37aacf113fd9?auto=format&fit=crop&w=900&q=80",
                    "rating": 4.7,
                    "visit_duration_minutes": 120,
                    "avg_cost": 55.0,
                    "distance_km": 4.1,
                    "best_time": "Jantar hoje",
                    "highlights": ["Mariscos", "Terrace", "Serviço premium"],
                },
            ]
        if self._is_activity_request(text):
            return [
                {
                    "name": "Passeio de Barco ao Mussulo",
                    "description": "Explora as ilhas e enseadas com um guia local em barco tradicional.",
                    "category": "Atividade",
                    "photo_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80",
                    "rating": 4.9,
                    "visit_duration_minutes": 180,
                    "avg_cost": 65.0,
                    "distance_km": 18.0,
                    "best_time": "Final da tarde",
                    "highlights": ["Praia", "Pôr do sol", "Guia local"],
                },
                {
                    "name": "Tour Histórico de Luanda",
                    "description": "Visita os principais marcos históricos da cidade com paragens culturais.",
                    "category": "Atividade",
                    "photo_url": "https://images.unsplash.com/photo-1528909514045-2fa4ac7a08ba?auto=format&fit=crop&w=900&q=80",
                    "rating": 4.8,
                    "visit_duration_minutes": 210,
                    "avg_cost": 50.0,
                    "distance_km": 5.0,
                    "best_time": "Manhã",
                    "highlights": ["Monumentos", "Museus", "Cultura"],
                },
            ]
        return []

    def _find_booking_option(self, text: str, options: list[dict[str, Any]]) -> dict[str, Any] | None:
        lower = text.lower()
        for option in options:
            if option["name"].lower() in lower or any(part in lower for part in option["name"].lower().split()):
                return option
        return None

    def _mock_booking_reservation(self, option: dict[str, Any]) -> dict[str, Any]:
        return {
            "name": option["name"],
            "status": "Reserva confirmada",
            "checkin": "Hoje",
            "checkout": "Amanhã",
            "guests": "2 pessoas",
            "code": f"{option['name'].split()[0].upper()}20250701",
            "photo_url": option.get("photo_url"),
            "cta": "Ver confirmação",
        }

    def _find_place(self, text: str) -> dict[str, Any]:
        places = self._get_places("Luanda", self._extract_interests(text))
        for place in places:
            if place["name"].lower() in text.lower() or any(part in text.lower() for part in place["name"].lower().split()):
                return place
        return places[0]

    def _extract_interests(self, text: str) -> list[str]:
        lower = text.lower()
        mapping = {
            "história": "História",
            "historia": "História",
            "gastronomia": "Gastronomia",
            "natureza": "Natureza",
            "vida noturna": "Vida Noturna",
            "praias": "Praias",
        }
        found = []
        for keyword, label in mapping.items():
            if keyword in lower and label not in found:
                found.append(label)
        return found

    def _get_places(self, city: str | None, interests: list[str]) -> list[dict[str, Any]]:
        if city is None:
            city = "Luanda"
        all_places = [
            {
                "name": "Ilha do Mussulo",
                "description": "Praia paradisíaca com águas cristalinas e passeios de barco.",
                "category": "Praias",
                "photo_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80",
                "rating": 4.8,
                "visit_duration_minutes": 240,
                "avg_cost": 25.0,
                "distance_km": 18.0,
                "best_time": "Manhã",
                "highlights": ["Praia", "Passeios de barco", "Gastronomia"],
            },
            {
                "name": "Fortaleza de São Miguel",
                "description": "Monumento histórico com vista sobre o porto e a cidade.",
                "category": "História",
                "photo_url": "https://images.unsplash.com/photo-1467269204594-9661b134dd2b?auto=format&fit=crop&w=900&q=80",
                "rating": 4.6,
                "visit_duration_minutes": 90,
                "avg_cost": 15.0,
                "distance_km": 8.0,
                "best_time": "Tarde",
                "highlights": ["História", "Vista panorâmica"],
            },
            {
                "name": "Miradouro da Lua",
                "description": "Paisagem espetacular ideal para fotografia e contemplação.",
                "category": "Natureza",
                "photo_url": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80",
                "rating": 4.7,
                "visit_duration_minutes": 120,
                "avg_cost": 10.0,
                "distance_km": 25.0,
                "best_time": "Por do sol",
                "highlights": ["Natureza", "Fotografia", "Miradouro"],
            },
            {
                "name": "Museu da Escravatura",
                "description": "Espaço cultural que conta a memória e a história de Angola.",
                "category": "História",
                "photo_url": "https://images.unsplash.com/photo-1518998053901-5348d3961a04?auto=format&fit=crop&w=900&q=80",
                "rating": 4.5,
                "visit_duration_minutes": 75,
                "avg_cost": 12.0,
                "distance_km": 6.0,
                "best_time": "Manhã",
                "highlights": ["História", "Cultura"],
            },
            {
                "name": "Marginal de Luanda",
                "description": "Passeio urbano com cafés, vida noturna e vista para o Atlântico.",
                "category": "Vida Noturna",
                "photo_url": "https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=900&q=80",
                "rating": 4.4,
                "visit_duration_minutes": 180,
                "avg_cost": 20.0,
                "distance_km": 4.0,
                "best_time": "Noite",
                "highlights": ["Vida Noturna", "Restaurantes"],
            },
        ]

        if not interests:
            return all_places

        filtered = [
            place
            for place in all_places
            if place["name"] == "Ilha do Mussulo"
            or any(interest.lower() in place["category"].lower() for interest in interests)
            or any(interest.lower() in place["description"].lower() for interest in interests)
        ]
        return filtered or all_places

    def _is_place_selection(self, text: str) -> bool:
        return any(name.lower() in text.lower() for name in ["mussulo", "fortaleza", "miradouro", "museu", "marginal"])
