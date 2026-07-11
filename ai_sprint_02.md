# Sprint 02 — Agente Conversacional: Descoberta e Recomendação

> **Lotador** · *"Da curiosidade à experiência."*
> Duração sugerida: 2 semanas · Pré-requisitos: entregáveis da [Sprint 01](ai_sprint_01.md)

## Objetivo da Sprint

Dar vida ao agente: integrar o LLM com a persona "Lotador" e implementar as fases **Descoberta → Interesse → Recomendação** do fluxo. No fim da sprint, o turista é acolhido, indica a cidade e os seus interesses, e recebe recomendações ricas de locais turísticos de Luanda em formato de cards.

## Fluxo alvo (do conversa.md)

```
Turista: Olá.
IA: Bem-vindo a Angola. Sou o Lotador, o teu Agente de viagem. Em que cidade estás?
Turista: Luanda.
IA: É a tua primeira vez em Angola? Que tipo de lugares gostas?
    ○ História ○ Gastronomia ○ Natureza ○ Vida Noturna ○ Praias
IA: Com base no teu perfil, recomendo: [cards com foto, classificação, duração, custo, distância, melhor horário]
```

## User Stories

- **US-05** — Como turista, quero ser acolhido pelo agente e dizer onde estou para receber ajuda contextualizada.
- **US-06** — Como turista, quero escolher os meus interesses (História, Gastronomia, Natureza, Vida Noturna, Praias) para receber recomendações personalizadas.
- **US-07** — Como turista, quero ver recomendações com foto, classificação, duração, custo médio, distância e melhor horário — não apenas nomes.
- **US-08** — Como turista, quero escolher um local (ex.: Mussulo) e receber uma apresentação convincente do destino.

## Tarefas Técnicas

### Inteligência Artificial
- [ ] Integrar LLM: OpenAI API (GPT-4o) **ou** Groq API (Llama 3) — decidir por latência/custo; abstrair o provider num serviço único
- [ ] System prompt da persona "Lotador": acolhedor, conhecedor de Angola, conduz naturalmente o turista até ao serviço (desperta curiosidade → apresenta destino → explica porque vale a pena)
- [ ] LangGraph: grafo de estados da fase "Guia":
  - `welcome` → `ask_city` → `ask_profile` → `recommend` → `present_place`
- [ ] Persistência do estado da conversa por sessão (memória do grafo)
- [ ] Function calling / tools: `get_places(city, interests)` consulta a BD e devolve locais

### Dados
- [ ] Seed de locais turísticos de Luanda com dados completos (foto, classificação, duração, custo médio, coordenadas, melhor horário, categorias):
  - Ilha do Mussulo · Fortaleza de São Miguel · Miradouro da Lua · Museu da Escravatura · Marginal de Luanda · Ilha de Luanda
- [ ] (Opcional MVP) ChromaDB com descrições dos locais para recomendação semântica

### Backend
- [ ] Endpoint `POST /chat` passa a invocar o grafo LangGraph (substitui o placeholder da Sprint 01)
- [ ] Endpoint `GET /places?city=&interests=` para alimentar os cards
- [ ] Respostas estruturadas: o backend devolve `{ message, ui_component, payload }` para o frontend renderizar cards e botões

### Frontend
- [ ] Componente de seleção de interesses (chips/botões: História, Gastronomia, Natureza, Vida Noturna, Praias)
- [ ] Cards de recomendação no chat: foto, nome, ★ classificação, duração, custo médio, distância, melhor horário
- [ ] Card expandido ao escolher um local (ex.: "Excelente escolha. O Mussulo é...") com destaques (✔ praia ✔ gastronomia ✔ passeios de barco) e tempo estimado de viagem
- [ ] Guardar perfil do turista (cidade, interesses, primeira vez) na store Zustand

## Critérios de Aceitação

1. Uma conversa nova começa sempre com o acolhimento e a pergunta da cidade.
2. A seleção de interesses altera as recomendações devolvidas.
3. As recomendações aparecem como cards com todos os campos (foto, classificação, duração, custo, distância, melhor horário).
4. Ao escolher "Mussulo", o agente apresenta o destino e termina com a oferta: *"Deseja que encontre um Driver-Guide certificado para acompanhá-lo?"* (gancho para a Sprint 03).
5. O agente responde em português por omissão e mantém a persona em toda a conversa.

## Entregáveis

- Agente conversacional funcional (fase "Guia") com LangGraph + LLM
- Base de locais turísticos de Luanda com seed completo
- UI de chat rica: seleção de interesses + cards de recomendação
- Transição preparada para a fase "Gestor de Viagem"

---
*Próxima sprint:* [ai_sprint_03.md](ai_sprint_03.md) — Driver-Guides: Confiança e Reserva
