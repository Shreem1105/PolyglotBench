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
- Backend: Python, FastAPI (planned), Pydantic
- Frontend: React + TypeScript (planned)
- Data/Storage: Lightweight file-based snapshots initially; database later
- Visualization: Charting library for comparative metrics dashboards
- Deployment: Containerized services (planned)

## 6. MVP Roadmap
1. Scaffold backend/frontend architecture and documentation
2. Implement tokenizer adapter layer and baseline metrics engine
3. Add core API endpoints for analysis and comparison
4. Build frontend views for input, result tables, and visualizations
5. Add export and leaderboard workflows
6. Validate metrics against research examples and refine fairness scoring

## 7. Latency Note
For the MVP, latency is initially estimated from token inflation patterns and complexity proxies, not measured from live end-to-end model inference.
