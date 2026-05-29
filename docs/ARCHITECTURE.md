# Architecture

## Product Overview
PolyglotBench is a full-stack observatory for analyzing tokenization-driven disparities across languages, scripts, and model/tokenizer families. The system combines comparative API analytics with a dashboard experience for researchers, builders, and evaluators.

## Backend Architecture
- FastAPI application with modular route files (`health`, `models`, `analyze`, `compare`, `export`, `leaderboard`, `submissions`)
- Shared settings module (`app/core/config.py`) for environment-driven config
- SQLAlchemy persistence layer for saved submissions
- Service layer orchestration:
  - `tokenizer_service.py` for tokenizer adapters and caching
  - `metrics_service.py` for deterministic metrics
  - `analysis_service.py` for reusable analysis pipeline
  - `export_service.py` for JSON/CSV serialization support
  - `leaderboard_service.py` for curated benchmark aggregation
  - `submission_service.py` for persistence and retrieval

## Frontend Architecture
- React + TypeScript + Vite single-page dashboard
- API client layer for backend communication
- Component-driven UI:
  - input and model selection
  - summary cards
  - charts
  - results tables
  - leaderboard view
  - submissions panel
- Recharts visualizations for model-level comparisons

## Data Layer
- Local default: SQLite via `DATABASE_URL=sqlite:///./polyglotbench.db`
- Production-ready path: PostgreSQL via `DATABASE_URL=postgresql+psycopg2://...`
- Current schema creation uses SQLAlchemy `create_all` on startup (no Alembic yet)

## Metrics Engine Design
- Text normalization and validation at request boundary
- Baseline model token count computed once per analysis set
- Per-model derived metrics:
  - token counts
  - word/character counts
  - fertility
  - token multiplier
  - estimated attention-cost multiplier
  - estimated latency multiplier
  - cost estimate
  - fairness score
- Language detected once per text and attached to result objects

## API Surface
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

## Data Flow
User text input -> tokenizer adapters -> metrics engine -> cost/fairness calculation -> API response -> frontend visualizations

## Risk Notes
- Commercial tokenizers may not exactly match closed production tokenizers
- Model prices can change and require updates
- Latency is currently estimated from token inflation proxies
- Curated benchmark quality affects leaderboard representativeness
- Schema migrations currently rely on `create_all`; Alembic is recommended before heavy production use
