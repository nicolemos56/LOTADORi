# Sprint 04 — Mapa em Tempo Real e Experiência Durante a Viagem

> **Lotador** · *"Da curiosidade à experiência."*
> Duração sugerida: 2 semanas · Pré-requisitos: entregáveis da [Sprint 03](ai_sprint_03.md)

## Objetivo da Sprint

Implementar a fase **Mobilidade → Experiência**: o mapa aparece apenas depois de o driver aceitar o pedido (*"O mapa é consequência. Nunca o protagonista."*), mostra o driver a aproximar-se em tempo real e, durante o trajeto, a IA continua ativa — partilha curiosidades sobre o destino e faz sugestões contextuais. No fim da sprint, o turista acompanha a viagem completa: driver a caminho → embarque → em viagem → chegada.

## Fluxo alvo (do conversa.md)

```
IA: Carlos aceitou o pedido. Tempo estimado: 7 minutos.
[Mapa abre mostrando o driver a vir até ao turista, em tempo real]
— durante a viagem —
IA: Sabias que... o Mussulo formou-se através de...
IA: Gostarias de conhecer um restaurante típico quando chegares?
```

## User Stories

- **US-13** — Como turista, quero ver no mapa o driver a vir até mim em tempo real, com tempo estimado atualizado.
- **US-14** — Como turista, quero acompanhar o trajeto até ao destino durante a viagem.
- **US-15** — Como turista, quero aprender curiosidades sobre o destino enquanto viajo ("Sabias que...").
- **US-16** — Como turista, quero receber sugestões contextuais para a chegada (ex.: restaurante típico no Mussulo).

## Tarefas Técnicas

### Backend (WebSockets)
- [ ] Endpoint WebSocket `WS /trips/{id}/track` — emite a posição do driver em tempo real
- [ ] Simulador de movimento (MVP): interpola a posição do driver ao longo da rota (driver → turista, depois turista → destino) e emite atualizações a cada 2–3 s
- [ ] Máquina de estados da viagem: `driver_en_route` → `arrived_pickup` → `in_trip` → `arrived_destination`; transições emitidas pelo WebSocket
- [ ] Atualizar `trips.status` conforme os eventos

### Frontend (React-Leaflet + OpenStreetMap)
- [ ] Componente de mapa com React-Leaflet — só é montado quando `trip.status = accepted` (nunca antes)
- [ ] Marcadores: turista, driver (com foto/ícone), destino; linha de rota
- [ ] Ligação ao WebSocket: marcador do driver move-se em tempo real; ETA atualizado
- [ ] Transições de estado visíveis: "Carlos está a caminho" → "Carlos chegou" → "Em viagem para o Mussulo" → "Chegaste!"
- [ ] O chat permanece acessível com o mapa aberto (mapa e conversa coexistem — a conversa continua a ser o centro)

### Inteligência Artificial (IA ativa durante o trajeto)
- [ ] LangGraph: estado `in_trip_companion` — ativado quando a viagem começa
- [ ] Curiosidades sobre o destino, enviadas espaçadamente durante o percurso ("Sabias que o Mussulo formou-se através de...")
- [ ] Sugestões contextuais de chegada: tool `get_nearby_suggestions(place_id, category)` (restaurantes típicos, passeios de barco)
- [ ] As mensagens da IA em viagem são proativas (iniciadas pelo servidor via WebSocket), não apenas reativas

## Critérios de Aceitação

1. O mapa nunca aparece antes de o driver aceitar o pedido.
2. O marcador do driver move-se suavemente em tempo real até ao turista e depois até ao destino (simulado).
3. Os quatro estados da viagem são atingidos por ordem e refletidos na UI e na BD.
4. Durante a viagem, o turista recebe pelo menos 2 curiosidades sobre o destino e 1 sugestão contextual de chegada.
5. Ao chegar, o estado passa a `arrived_destination` — gancho para a avaliação (Sprint 05).

## Entregáveis

- Mapa em tempo real (React-Leaflet + WebSockets) com simulador de movimento
- Máquina de estados da viagem completa
- IA companheira de viagem: curiosidades + sugestões proativas
- Experiência ponta a ponta: da escolha do driver até à chegada ao destino


---
*Próxima sprint:* [ai_sprint_05.md](ai_sprint_05.md) — Pós-Viagem, Memória e Deploy
