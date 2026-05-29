# PolyglotBench

## 1. Project Title
PolyglotBench

## 2. Short Description
PolyglotBench is a live tokenization fairness observatory for comparing how multilingual text is segmented across language models and tokenizer families.

## 3. Research Motivation
This project is inspired by the paper "The Script Tax: Measuring Tokenization-Driven Efficiency and Latency Disparities in Multilingual Language Models." Different scripts can incur higher token counts for equivalent meaning, leading to cost and performance disparities. PolyglotBench is designed to make those disparities visible, measurable, and discussable.

## 4. Planned Features
- Multi-model tokenizer comparison for the same input text
- Per-language/script token inflation and fertility analysis
- Estimated cost and latency impact projections
- Fairness leaderboard across languages and scripts
- Exportable analysis results for reporting and reproducibility

## 5. Planned Tech Stack
- Backend: Python, FastAPI, Pydantic, SQLAlchemy
- Frontend: React + TypeScript + Vite
- Data/Storage: SQLite in local development; PostgreSQL planned for future deployment
- Visualization: Charting library for comparative metrics dashboards
- Deployment: Containerized services (planned)

## 6. MVP Roadmap
1. Scaffold backend/frontend architecture and documentation
2. Implement tokenizer adapter layer and baseline metrics engine
3. Add core API endpoints for analysis and comparison
4. Build frontend views for input, result tables, and visualizations
5. Add export and leaderboard workflows
6. Add saved submission workflows and prepare for future community benchmarks

## 7. Latency Note
For the MVP, latency is initially estimated from token inflation patterns and complexity proxies, not measured from live end-to-end model inference.

## Environment Setup

### Backend env
- Copy `backend/.env.example` if you want custom local values.
- Runtime config is environment-based (`ENVIRONMENT`, `DATABASE_URL`, `DEFAULT_BASELINE_MODEL`, `CORS_ORIGINS`).
- `DATABASE_URL` defaults to `sqlite:///./polyglotbench.db`.

### Frontend env
- `frontend/.env.example` includes `VITE_API_BASE_URL=http://localhost:8000`.

## Docker Quickstart

```powershell
docker compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

## Deployment Docs
- See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for local, Docker, and production deployment guidance.

## Backend Operations
- `GET /health` for liveness checks.
- `GET /ready` for readiness checks with database connectivity verification.
- CORS support is enabled for frontend dev origins (configurable via `CORS_ORIGINS`).

## Frontend Features
- model selector
- baseline selector
- token count table
- token multiplier chart
- fairness score chart
- estimated latency visualization
- example multilingual inputs
- recent community analyses panel
- save analysis submission action

## Observatory Features
- automatic language detection for analyzed text
- fairness leaderboard generation from multilingual benchmark comparison
- saved analysis submissions backed by local SQLite
- database files ignored by Git in local development
- future PostgreSQL support planned

## Run Locally

### Backend (FastAPI)
```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (React + Vite)
```powershell
cd frontend
npm install
npm run dev
```

- Backend default URL: `http://localhost:8000`
- Frontend runs on Vite's default local dev port (typically `http://localhost:5173`)
