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

## Production Overview

Recommended split deployment:
- Backend: container deployment (Render, Fly.io, or similar)
- Frontend: static deployment (Vercel, Netlify, or similar)

## Backend Deployment Notes (Render/Fly.io style)

- Build from `backend/Dockerfile`
- Expose port `8000`
- Set `DATABASE_URL` environment variable
- For container persistence, mount storage and point SQLite to mounted path

## Frontend Deployment Notes (Vercel/Netlify style)

- Build command: `npm run build`
- Publish directory: `dist`
- Set `VITE_API_BASE_URL` to deployed backend URL if needed

## Environment Variables

### Backend
- `DATABASE_URL` (optional)
- Default local value: `sqlite:///./polyglotbench.db`

### Frontend
- `VITE_API_BASE_URL` (optional)
- Default local value: `http://localhost:8000`

## SQLite Limitation

SQLite is suitable for local development and lightweight deployments. It is not ideal for high-concurrency production workloads.

## Future PostgreSQL Plan

PostgreSQL support is planned for future releases to improve concurrency, durability, and scaling.
