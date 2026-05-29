# PolyglotBench

**A live tokenization fairness observatory for multilingual LLMs.**

![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-Strict-3178C6?logo=typescript&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![PostgreSQL-ready](https://img.shields.io/badge/Database-PostgreSQL--ready-336791?logo=postgresql&logoColor=white)
![Research-inspired](https://img.shields.io/badge/Research-Inspired-6A1B9A)

## Live Demo

Public links are provided below for both the interactive observatory and the backend API documentation.

* [Launch PolyglotBench](https://polyglot-bench.vercel.app)
* [Open FastAPI Docs](https://polyglotbench-api.onrender.com/docs)

## Research Motivation
Large language models are often expected to work equally well across different languages and writing systems. However, the way text is tokenized can vary significantly from one language to another.

Some languages require more tokens to represent the same information, which can increase cost, latency, and overall model efficiency differences. These effects are often hidden from users and developers.

PolyglotBench was created to make these differences visible through an interactive observatory that allows users to compare tokenizer behavior across languages and models.

## Research Origin
PolyglotBench was inspired by research on tokenization-driven disparities in multilingual language models. The project extends ideas explored in a published research paper accepted to the EACL 2026 LoResLM Workshop.

The research investigates how different writing systems can experience significantly different tokenization efficiency, resulting in measurable differences in cost, latency, and accessibility when interacting with modern language models.

This observatory was built to transform those research findings into an interactive tool that researchers, students, and developers can use to explore tokenization fairness in practice.

### Research Links
Google Scholar:

https://scholar.google.com/citations?view_op=view_citation&hl=en&user=sRBI_S4AAAAJ&citation_for_view=sRBI_S4AAAAJ:u-x6o8ySG0sC

Research Paper PDF:

(PDF link coming soon)

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

## Additional Docs
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/API_EXAMPLES.md](docs/API_EXAMPLES.md)
- [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md)
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- [docs/DATABASE.md](docs/DATABASE.md)
