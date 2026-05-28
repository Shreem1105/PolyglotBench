# Architecture

## 1. Product Overview
PolyglotBench is a research-informed observatory that highlights tokenization-driven disparities across languages and scripts. Users submit text, select model/tokenizer targets, and receive comparative metrics focused on efficiency, cost, and fairness.

## 2. Backend Architecture
- API layer: HTTP endpoints for health, model listing, analysis, comparison, exports, and leaderboard retrieval
- Tokenizer adapters: Pluggable service interfaces for model-specific tokenization behavior
- Metrics engine: Deterministic computation module for token, cost, and fairness metrics
- Domain schemas: Request/response contracts and typed metric payloads
- Validation and config core: Shared configuration, constants, and validation rules

## 3. Frontend Architecture
- Input workspace: Text entry, language/script metadata, and model selection
- Results dashboard: Comparative tables, ranking cards, and metric visualizations
- Scenario tools: Side-by-side comparisons for multiple model/language combinations
- Export UI: Download options for benchmark output artifacts

## 4. Metrics Engine Design
- Accepts normalized input text and tokenizer outputs per model
- Computes base counts and derived multipliers
- Produces cost proxies and fairness indicators
- Returns a consistent metrics envelope for APIs and UI rendering
- Supports future extension for measured latency ingestion

## 5. Planned API Endpoints
- GET /health
- GET /models
- POST /analyze
- POST /compare
- GET /leaderboard
- POST /export

## 6. Data Flow
User text input -> tokenizer adapters -> metrics engine -> cost/fairness calculation -> API response -> frontend visualizations

## 7. Risk Notes
- Commercial tokenizers may not be exact replicas of proprietary production internals
- Model pricing tables change over time and require periodic updates
- Latency is estimated in the initial version rather than directly measured live
- Document upload and batch ingestion workflows are planned for later phases
