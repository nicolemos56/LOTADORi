# Lotador: Sistema de táxi inteligente para mobilidade turística em Angola

> *"Da curiosidade à experiência."* Sistema de táxi inteligente para mobilidade turística em Angola

Agente de turismo com IA que converte uma conversa numa experiência física: o turista descobre locais turísticos de Angola a conversar com o agente, escolhe um destino e é ligado a um driver-guide certificado que o leva lá.

**Fluxo do produto:** Descoberta → Interesse → Confiança → Mobilidade → Experiência → Avaliação

## Stack

| Camada | Tecnologia |
| --- | --- |
| Frontend | React 18 (Vite) · Tailwind CSS · Zustand |
| Backend | FastAPI · SQLAlchemy · Alembic · pydantic-settings |
| Base de dados | PostgreSQL 16 + PostGIS 3.4 (Docker) |
| IA (Sprint 02+) | LLM (OpenAI/Groq) · LangGraph |

## Estrutura do repositório

```
.
├── backend/          # API FastAPI
│   ├── app/
│   │   ├── core/     # configuração, ligação à BD
│   │   ├── models/   # modelos SQLAlchemy (tourists, places, drivers)
│   │   ├── routers/  # endpoints (/health, /chat)
│   │   ├── schemas/  # modelos Pydantic (request/response)
│   │   └── services/ # lógica de negócio
│   └── alembic/      # migrações da base de dados
├── frontend/         # App React (interface de chat)
├── docker-compose.yml
└── .env.example
```

## Arranque do zero

### Pré-requisitos

- Python 3.11+
- Node.js 20+
- Docker Desktop

### 1. Variáveis de ambiente

```bash
cp .env.example .env
```

Os valores por omissão funcionam para desenvolvimento local. As chaves LLM só são necessárias a partir da Sprint 02.

### 2. Base de dados (PostgreSQL + PostGIS)

```bash
docker compose up -d
```

Verificar que o PostGIS está ativo:

```bash
docker exec turismoconnect-db psql -U turismo -d turismoconnect -c "SELECT PostGIS_version();"
```

### 3. Backend (FastAPI)

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt

# Aplicar as migrações (cria as tabelas tourists, places, drivers)
alembic upgrade head

# Arrancar a API em http://localhost:8000
uvicorn app.main:app --reload
```

Testar: [http://localhost:8000/health](http://localhost:8000/health) deve devolver `{"status":"ok"}`. Documentação interativa em [http://localhost:8000/docs](http://localhost:8000/docs).

### 4. Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

Abrir [http://localhost:5173](http://localhost:5173), escrever uma mensagem e enviar — a resposta do backend aparece no chat (por agora é um placeholder; a IA chega na Sprint 02).

## Roadmap (sprints)

1. **Sprint 01 — Fundação e Setup** ✅ (este repositório)
2. [Sprint 02 — Agente Conversacional: Descoberta e Recomendação](ai_sprint_02.md)
3. [Sprint 03 — Driver-Guides: Confiança e Reserva](ai_sprint_03.md)
4. [Sprint 04](ai_sprint_04.md) · [Sprint 05](ai_sprint_05.md)
