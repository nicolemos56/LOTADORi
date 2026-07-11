# Sprint 03 — Driver-Guides: Confiança e Reserva

> **Lotador** · *"Da curiosidade à experiência."*
> Duração sugerida: 2 semanas · Pré-requisitos: entregáveis da [Sprint 02](ai_sprint_02.md)

## Objetivo da Sprint

Implementar a fase **Confiança → Mobilidade**: quando o turista decide sair do hotel, o agente muda de papel — deixa de ser guia e passa a ser **gestor da viagem**. Apresenta driver-guides certificados com classificação e comentários, e gere o pedido e a confirmação da viagem. No fim da sprint, o turista escolhe um driver e recebe a confirmação com tempo estimado.

## Fluxo alvo (do conversa.md)

```
IA: Deseja que encontre um Driver-Guide certificado para acompanhá-lo?
Turista: Sim.
IA: Temos estes disponíveis:
    ★★★★★ Carlos — 215 viagens — Português, Inglês
    ★★★★★ Pedro — 410 viagens — Português, Francês
    ★★★★☆ Manuel — 90 viagens — Português
Turista: Carlos.
IA: Perfeito. Carlos aceitou o pedido. Tempo estimado: 7 minutos.
```

## User Stories

- **US-09** — Como turista, quero ver uma lista de driver-guides com classificação, comentários de outros turistas, foto, idiomas, preço e especialidades para escolher com confiança.
- **US-10** — Como turista, quero que os drivers apresentados estejam próximos de mim e falem um idioma que eu entenda.
- **US-11** — Como turista, quero pedir um driver e receber confirmação com tempo estimado de chegada.
- **US-12** — Como turista, quero poder recusar/trocar de driver antes de confirmar.

## Tarefas Técnicas

### Inteligência Artificial
- [ ] LangGraph: novo subgrafo "Gestor de Viagem" com estados:
  - `offer_driver` → `list_drivers` → `driver_selected` → `request_pending` → `request_accepted`
- [ ] Transição de papel guia → gestor: o tom da persona muda (menos narrativo, mais operacional)
- [ ] Tool `find_drivers(place_id, tourist_location, language)` — consulta geoespacial + filtros

### Dados
- [ ] Seed de driver-guides (mín. 6): nome, foto, idiomas, nº de viagens, classificação, preço base, especialidades, localização atual
- [ ] Tabela `reviews` — comentários de turistas sobre drivers (autor, texto, estrelas, data)
- [ ] Tabela `trips` — pedido de viagem: turista, driver, local de destino, estado (`pending`, `accepted`, `in_progress`, `completed`, `cancelled`), timestamps

### Backend
- [ ] `GET /drivers?place_id=&lang=` — lista ordenada por classificação; distância calculada com PostGIS (`ST_Distance`, `ST_DWithin`)
- [ ] `POST /trips` — criar pedido de viagem
- [ ] Simulador de aceitação (MVP): o driver "aceita" automaticamente após alguns segundos e calcula tempo estimado de chegada pela distância
- [ ] `GET /trips/{id}` — estado do pedido

### Frontend
- [ ] Cards de driver no chat: foto, nome, ★ classificação, nº de viagens, idiomas (bandeiras/etiquetas), preço, especialidades
- [ ] Vista de comentários/experiências de turistas por driver
- [ ] Fluxo de confirmação: "Carlos aceitou o pedido. Tempo estimado: 7 minutos." com estado visível
- [ ] Botão para cancelar/trocar de driver enquanto o pedido está pendente
- [ ] Guardar viagem ativa na store Zustand

## Critérios de Aceitação

1. A lista de drivers só aparece depois de o turista aceitar a oferta do agente (nunca antes — o serviço pago surge naturalmente).
2. Os drivers aparecem ordenados por classificação, com todos os dados (foto, viagens, idiomas, preço, especialidades, comentários).
3. A distância/tempo estimado é calculada com PostGIS a partir das localizações reais (seed).
4. Ao escolher um driver, o pedido é criado, "aceite" pelo simulador e o turista vê a confirmação com tempo estimado.
5. A conversa mantém o contexto: o agente sabe qual o destino escolhido na Sprint 02.

## Entregáveis

- Fase "Gestor de Viagem" no LangGraph com mudança de papel do agente
- Marketplace de driver-guides com classificações e comentários
- Fluxo completo de pedido → aceitação → confirmação (simulado)
- Consultas geoespaciais PostGIS funcionais


---
*Próxima sprint:* [ai_sprint_04.md](ai_sprint_04.md) — Mapa em Tempo Real e Experiência Durante a Viagem
