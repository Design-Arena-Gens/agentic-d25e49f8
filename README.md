# PerplexiPlay – Agent Playground and Testing Environment

Open-source platform to build, test, and benchmark agentic AI agents using CrewAI, LangChain, and OpenAI.

- Backend: FastAPI + SQLAlchemy (PostgreSQL in Docker, SQLite in dev/tests)
- Frontends: Streamlit (local) and minimal Next.js landing (Vercel)
- Auth: JWT access + refresh, rotation, revocation; Argon2/Bcrypt password hashing
- Store: users, agent configs, experiments, results

## Quick Start (Local)

Requirements:
- Docker and Docker Compose

Run the full stack:

```bash
docker compose up --build
```

Services:
- API: http://localhost:8000 (OpenAPI at `/docs`)
- Streamlit: http://localhost:8501
- Postgres: internal Docker network

Default environment (edit as needed in `docker-compose.yml`):
- POSTGRES_DB: `perplexiplay`
- POSTGRES_USER: `perplexi`
- POSTGRES_PASSWORD: `perplexi`

## Development (without Docker)

Backend (FastAPI, SQLite dev):

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- API URL: http://localhost:8000
- OpenAPI: http://localhost:8000/docs

Streamlit UI (points to local API by default):

```bash
cd frontend_streamlit
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export API_BASE_URL=http://localhost:8000/api
streamlit run app.py
```

## API Overview

Auth endpoints:
- POST `/api/auth/register`
- POST `/api/auth/login`
- POST `/api/auth/refresh`
- POST `/api/auth/logout`

Agents:
- POST `/api/agents/` (create)
- GET `/api/agents/` (list)
- GET `/api/agents/{id}` (get)
- PUT `/api/agents/{id}` (update)
- DELETE `/api/agents/{id}` (delete)

Experiments:
- POST `/api/experiments` (start; synchronous stub)
- GET `/api/experiments/{id}` (status/results)

Frameworks supported: `crewai`, `langchain`, `openai` (stubbed; extend `backend/app/services/agent_engine.py`).

## Auth Details

- Password hashing via Passlib with Argon2 (fallback Bcrypt).
- JWT access (15 min) + refresh (7 days) tokens.
- Refresh rotation and revocation via DB tables.
- Bearer auth required for non-auth endpoints.

## Tests

```bash
pip install -r backend/requirements.txt
pytest -q
```

## Vercel Deployment (Next.js frontend)

This repo includes a minimal Next.js landing page that deploys to Vercel. The API and Streamlit are intended to run locally or in your own infra.

Deploy (requires configured `VERCEL_TOKEN`):

```bash
vercel deploy --prod --yes --token $VERCEL_TOKEN --name agentic-d25e49f8
```

After a few seconds:

```bash
curl https://agentic-d25e49f8.vercel.app
```

## Project Structure

```
backend/
  app/
    core/        # config, database, security
    models/      # SQLAlchemy models
    routers/     # FastAPI routers (auth, agents, experiments)
    services/    # Agent engine stubs
    main.py
  requirements.txt
  Dockerfile
frontend_streamlit/
  app.py
  requirements.txt
  Dockerfile
app/              # Next.js app router (Vercel landing)
.github/workflows/ci.yml
docker-compose.yml
```

## Extending Agent Engine
Implement real integrations in `backend/app/services/agent_engine.py` using your preferred SDKs. Add provider credentials via environment variables and extend `params` validation.

## License
MIT
