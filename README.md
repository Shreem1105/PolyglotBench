# PolyglotBench

**A live tokenization fairness observatory for multilingual LLMs.**

![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-Strict-3178C6?logo=typescript&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![PostgreSQL-ready](https://img.shields.io/badge/Database-PostgreSQL--ready-336791?logo=postgresql&logoColor=white)
![Research-inspired](https://img.shields.io/badge/Research-Inspired-6A1B9A)

## Live Demo

- [Launch PolyglotBench](https://polyglot-bench.vercel.app)
- [Open FastAPI Docs](https://polyglotbench-api.onrender.com/docs)

Use the frontend link for the interactive dashboard and the FastAPI docs link for direct API testing.

## Research Motivation
Multilingual language models are often treated as if they are script- and language-neutral.  
In practice, tokenizer behavior can inflate sequence length for some scripts compared with others.  
That inflation can create downstream disparities in cost, latency proxies, and accessibility.  
PolyglotBench turns this research direction into an interactive observatory for measuring and communicating these differences.

## Key Features
- Real-time tokenizer comparison
- Fertility calculation
- Token multiplier
- Estimated latency multiplier
- Estimated attention-cost multiplier
- Fairness score
- Multilingual language detection
- Fairness leaderboard
- Saved community analyses
- CSV/JSON export
- Dockerized backend/frontend
- SQLite default and PostgreSQL-ready config

## Demo Screenshots
![Dashboard Placeholder](docs/assets/dashboard-placeholder.png)
![Charts Placeholder](docs/assets/charts-placeholder.png)
![Leaderboard Placeholder](docs/assets/leaderboard-placeholder.png)

Screenshot guidance: [docs/assets/README.md](docs/assets/README.md)

## Architecture Overview
```text
User Text
   ↓
React Dashboard
   ↓
FastAPI Backend
   ↓
Tokenizer + Metrics Services
   ↓
SQLite/PostgreSQL
   ↓
Charts, Exports, Leaderboard
```

## Tech Stack
### Backend
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite/PostgreSQL
- tiktoken
- Hugging Face Transformers

### Frontend
- React
- TypeScript
- Vite
- Recharts

### DevOps
- Docker
- Docker Compose

## Metrics
- `token_count`: number of tokenizer-produced tokens for a given model.
- `fertility`: tokens per word (`token_count / word_count`).
- `token_multiplier`: token count relative to baseline model.
- `estimated_attention_cost_multiplier`: squared token multiplier (`token_multiplier^2`).
- `estimated_latency_multiplier`: current proxy equal to token multiplier.
- `fairness_score`: normalized 0-100 score where lower token inflation yields higher fairness.

## Quickstart
### Backend
```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```powershell
cd frontend
npm install
npm run dev
```

## Docker Quickstart
```powershell
docker compose up --build
```

## API Endpoints
- `GET /`
- `GET /health`
- `GET /ready`
- `GET /models`
- `POST /analyze`
- `POST /compare`
- `POST /export`
- `GET /leaderboard`
- `POST /submissions/from-analysis`
- `GET /submissions`

## Example API Request
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial intelligence is changing how people build software.",
    "model_ids": ["gpt-4o-mini", "gpt-4o", "xlm-roberta-base"],
    "baseline_model_id": "gpt-4o-mini"
  }'
```

## Repository Structure
```text
polyglotbench/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   └── nginx.conf
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API_EXAMPLES.md
│   ├── DATABASE.md
│   ├── DEMO_SCRIPT.md
│   └── DEPLOYMENT.md
├── research/
├── docker-compose.yml
└── README.md
```

## Development Status
MVP complete. Deployment and production hardening in progress.

## Roadmap
- public deployment
- PDF reports
- Alembic migrations
- richer tokenizer registry
- larger curated multilingual benchmark
- admin-reviewed public leaderboard
- real latency benchmarking

## Research Attribution
This project is inspired by the Script Tax research direction on tokenization-driven disparities in multilingual language models.

## Resume Line
Developed PolyglotBench, a full-stack tokenization fairness observatory for multilingual LLMs with FastAPI, React, SQLAlchemy, Docker, tokenizer adapters, fairness metrics, exports, and leaderboard visualization.

## Additional Docs
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/API_EXAMPLES.md](docs/API_EXAMPLES.md)
- [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md)
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- [docs/DATABASE.md](docs/DATABASE.md)
