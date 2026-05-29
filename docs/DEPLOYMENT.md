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

## Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `ENVIRONMENT` | `development` | Runtime profile marker used for deployment context. |
| `DATABASE_URL` | `sqlite:///./polyglotbench.db` | SQLAlchemy connection string. Docker uses `sqlite:///./data/polyglotbench.db`. |
| `DEFAULT_BASELINE_MODEL` | `gpt-4o-mini` | Fallback baseline model for fairness comparisons. |
| `CORS_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000` | Comma-separated allowed frontend origins. |
| `VITE_API_BASE_URL` | `http://localhost:8000` | Frontend API base URL. |

`CORS_ORIGINS` is parsed as a comma-separated list. In production, add your deployed frontend domain(s) to this value.

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

## Frontend Deployment Notes (Vercel/Netlify style)

- Build command: `npm run build`
- Publish directory: `dist`
- Set `VITE_API_BASE_URL` to deployed backend URL

## SQLite Limitation

SQLite is suitable for local development and lightweight deployments. It is not ideal for high-concurrency production workloads.

## Future PostgreSQL Plan

PostgreSQL support is planned for future releases to improve concurrency, durability, and scaling.
