# Sprint 05 — Pós-Viagem, Memória e Deploy

> **Kalawenda AI Agent** · *"Da curiosidade à experiência."*
> Duração sugerida: 2 semanas · Pré-requisitos: entregáveis da [Sprint 04](ai_sprint_04.md)

## Objetivo da Sprint

Fechar o ciclo e reabri-lo: **Experiência → Avaliação → novo ciclo**. O sistema não termina quando o turista entra no táxi — é aí que começa. Esta sprint implementa a avaliação, o **Travel Memory**, os extras que diferenciam o produto (orçamento inteligente, multilingue, planeador automático, emergências) e coloca o protótipo online.

## Fluxo alvo (do conversa.md)

```
IA: Como foi a experiência? ★★★★★
IA: Gostarias de visitar outro local? Tenho três sugestões perto da tua localização.
— no dia seguinte —
IA: Ontem visitaste: ✔ Fortaleza. Hoje talvez gostes de... Museu Nacional.
```

## User Stories

- **US-17** — Como turista, quero avaliar a experiência (driver e local) no fim da viagem para ajudar outros turistas.
- **US-18** — Como turista, quero que o agente se lembre do que já visitei e sugira novidades (Travel Memory).
- **US-19** — Como turista, quero dizer "tenho apenas 50 dólares" e receber um roteiro adaptado ao meu orçamento.
- **US-20** — Como turista, quero conversar na minha língua (sueco, inglês, francês, português).
- **US-21** — Como turista, quero dizer "tenho apenas 6 horas livres" e receber um plano automático.
- **US-22** — Como turista, quero ajuda de emergência ("perdi o passaporte") com embaixada, contactos úteis e próximos passos.

## Tarefas Técnicas

### Avaliação e Travel Memory
- [ ] Ao chegar (`arrived_destination`), o agente pede avaliação: estrelas + comentário (driver e local)
- [ ] Guardar avaliações em `reviews`; recalcular classificação média do driver
- [ ] Tabela `visits` — histórico de locais visitados por turista
- [ ] LangGraph: estado `post_trip` → oferece 3 sugestões próximas da localização atual (PostGIS) → reinicia o ciclo de descoberta
- [ ] Travel Memory: na abertura de nova sessão, o agente recorda visitas ("Ontem visitaste ✔ Fortaleza. Hoje talvez gostes de...") e exclui locais já visitados das recomendações

### Extras do MVP (diferenciação)
- [ ] **Orçamento inteligente**: tool `plan_by_budget(amount)` — filtra locais e drivers pelo custo, monta roteiro dentro do valor
- [ ] **Multilingue**: deteção automática do idioma do turista (PT/EN/FR/SV); persona responde no idioma detetado; preferência guardada no perfil
- [ ] **Planeador automático**: tool `plan_by_time(hours)` — combina locais por proximidade e duração da visita para caber no tempo disponível
- [ ] **Modo emergência**: intenção `emergency` interrompe qualquer estado do grafo; devolve embaixada do país do turista, contactos úteis (polícia, hospital) e próximos passos

### Deploy e Qualidade
- [ ] Frontend → **Vercel** (build de produção, variáveis de ambiente)
- [ ] Backend → **Render** ou **Railway** (FastAPI + WebSockets; confirmar suporte a WS no plano escolhido)
- [ ] Base de dados PostgreSQL + PostGIS gerida (Render/Railway/Neon)
- [ ] CORS e URLs de produção configurados; `.env.example` atualizado
- [ ] Smoke tests pós-deploy: health check, conversa completa, WebSocket de tracking
- [ ] Guia de demo no README: percurso "do olá à avaliação" em produção

## Critérios de Aceitação

1. Depois da chegada, o turista avalia a experiência e recebe 3 sugestões próximas — o ciclo recomeça sem sair do chat.
2. Numa nova sessão, o agente lembra-se das visitas anteriores e não repete recomendações.
3. "Tenho 50 dólares" e "tenho 6 horas" produzem roteiros adaptados e coerentes.
4. Uma conversa iniciada em inglês, francês ou sueco é respondida no mesmo idioma.
5. "Perdi o passaporte" interrompe qualquer fluxo e devolve informação de emergência correta para a nacionalidade do turista.
6. O protótipo está acessível publicamente (Vercel + Render/Railway) e o fluxo completo funciona em produção.

## Entregáveis

- Ciclo completo fechado: avaliação + Travel Memory + novo ciclo de descoberta
- Extras funcionais: orçamento, multilingue, planeador, emergências
- Protótipo em produção com URL pública
- Documentação de demo para apresentação do MVP

---


🏁 **Fim do plano de sprints do MVP.** Com as 5 sprints concluídas, o Lotador AI Agent cobre todo o fluxo: **Descoberta → Interesse → Confiança → Mobilidade → Experiência → Avaliação** — da curiosidade à experiência.
