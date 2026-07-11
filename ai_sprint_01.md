# Sprint 01 — Fundação e Setup do Projeto

> **Lotador** · *"Da curiosidade à experiência."*
> Duração sugerida: 2 semanas · Pré-requisitos: nenhum

## Objetivo da Sprint

Montar a fundação técnica do projeto: repositório organizado, backend FastAPI a correr, frontend React com uma interface de chat funcional e base de dados PostgreSQL + PostGIS pronta para dados geoespaciais. No fim da sprint, o turista consegue trocar mensagens simples com o backend (ainda sem IA).

## User Stories

- **US-01** — Como programador, quero um monorepo organizado (`frontend/` + `backend/`) para que a equipa trabalhe de forma consistente.
- **US-02** — Como turista, quero abrir a aplicação e ver uma interface de chat limpa para começar a conversar.
- **US-03** — Como turista, quero enviar uma mensagem e receber uma resposta do servidor (eco/placeholder) para validar a comunicação ponta a ponta.
- **US-04** — Como programador, quero modelos de dados iniciais (turista, local turístico, driver-guide) para suportar as próximas sprints.

## Tarefas Técnicas

### Estrutura do Repositório
- [ ] Criar monorepo com `frontend/` e `backend/`
- [ ] `README.md` com visão do projeto e instruções de arranque
- [ ] `.gitignore`, `.env.example` (chaves LLM, ligação à BD)
- [ ] `docker-compose.yml` com serviço PostgreSQL + PostGIS

### Backend (FastAPI)
- [ ] Esqueleto FastAPI com estrutura `app/` (routers, models, services, core)
- [ ] Endpoint `GET /health` (verificação de vida do serviço)
- [ ] Endpoint `POST /chat` que recebe mensagem e devolve resposta placeholder
- [ ] Configuração via variáveis de ambiente (`pydantic-settings`)
- [ ] CORS configurado para o frontend local

### Frontend (React 18 + Tailwind + Zustand)
- [ ] Projeto React 18 (Vite) com Tailwind CSS configurado
- [ ] Store Zustand: histórico da conversa e dados do perfil do turista
- [ ] Componente de chat: lista de mensagens, campo de entrada, botão enviar
- [ ] Diferenciação visual turista vs. agente (bolhas de chat)
- [ ] Ligação ao endpoint `POST /chat` via fetch/axios

### Base de Dados (PostgreSQL + PostGIS)
- [ ] Subir PostgreSQL com extensão PostGIS via Docker
- [ ] Modelos SQLAlchemy iniciais:
  - `tourists` — id, nome, idioma, nacionalidade, cidade atual, interesses
  - `places` — id, nome, descrição, categoria, foto_url, classificação, duração da visita, custo médio, melhor horário, `location (GEOGRAPHY Point)`
  - `drivers` — id, nome, foto_url, idiomas, nº de viagens, classificação, preço base, especialidades, `location (GEOGRAPHY Point)`
- [ ] Migrações com Alembic

## Critérios de Aceitação

1. `docker compose up` sobe a base de dados com PostGIS ativo (`SELECT PostGIS_version();` funciona).
2. `GET /health` devolve `200 OK`.
3. O frontend abre no browser, envia uma mensagem e mostra a resposta do backend no chat.
4. As tabelas `tourists`, `places` e `drivers` existem com as colunas geoespaciais.
5. O README permite a um novo programador arrancar o projeto do zero.

## Entregáveis

- Monorepo funcional com frontend + backend + base de dados
- Interface de chat com comunicação ponta a ponta (sem IA)
- Modelos de dados e migrações iniciais
- Documentação de arranque (README)


---
*Próxima sprint:* [ai_sprint_02.md](ai_sprint_02.md) — Agente Conversacional: Descoberta e Recomendação
