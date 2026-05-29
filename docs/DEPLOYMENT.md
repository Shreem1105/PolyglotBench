# Deployment Guide

## Local Development

### Backend
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Health and readiness checks:
- `GET /health` checks process liveness.
- `GET /ready` runs a lightweight database connectivity check (`SELECT 1`).

### Frontend
```powershell
cd frontend
npm install
npm run dev
```

## Docker Compose

From the project root:

```powershell
docker compose up --build
```

Services:
- Backend API: `http://localhost:8000`
- Frontend app: `http://localhost:5173`

The backend container stores SQLite data in `./backend/data` using:
`DATABASE_URL=sqlite:///./data/polyglotbench.db`

An optional `postgres` service is also included for production-style testing.

## Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `ENVIRONMENT` | `development` | Runtime profile marker used for deployment context. |
| `DATABASE_URL` | `sqlite:///./polyglotbench.db` | SQLAlchemy connection string. Docker uses `sqlite:///./data/polyglotbench.db`. |
| `DEFAULT_BASELINE_MODEL` | `gpt-4o-mini` | Fallback baseline model for fairness comparisons. |
| `CORS_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000` | Comma-separated allowed frontend origins. |
| `VITE_API_BASE_URL` | `http://localhost:8000` | Frontend API base URL. |

`CORS_ORIGINS` is parsed as a comma-separated list. In production, add your deployed frontend domain(s) to this value.

`DATABASE_URL` examples:
- `sqlite:///./polyglotbench.db`
- `postgresql+psycopg2://user:password@host:5432/polyglotbench`

Never commit real database credentials to source control.

## Production Overview

Recommended split deployment:
- Backend: container deployment (Render, Fly.io, or similar)
- Frontend: static deployment (Vercel, Netlify, or similar)

## Backend Deployment Notes (Render/Fly.io style)

- Build from `backend/Dockerfile`
- Expose port `8000`
- Set `DATABASE_URL` and `CORS_ORIGINS` environment variables
- Mount persistent storage if using SQLite in container environments
- Use `GET /ready` for readiness checks in platform health probes

## PostgreSQL Deployment Notes

- Use managed PostgreSQL for production reliability and concurrency.
- Set `DATABASE_URL` to a PostgreSQL URL (`postgresql+psycopg2://...`).
- Keep credentials in platform secret managers, not in `.env.example` or committed compose files.
- Current schema setup uses `create_all`; add Alembic before critical production migration workflows.

## Frontend Deployment Notes (Vercel/Netlify style)

- Build command: `npm run build`
- Publish directory: `dist`
- Set `VITE_API_BASE_URL` to deployed backend URL

## SQLite Limitation

SQLite is suitable for local development and lightweight deployments. It is not ideal for high-concurrency production workloads.

## Future PostgreSQL Plan

PostgreSQL support is planned for future releases to improve concurrency, durability, and scaling.
