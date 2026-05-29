# PolyglotBench Project Audit

## Scope Reviewed
- Backend (`backend/app`, DB layer, services, routes, tests)
- Frontend (`frontend/src`, API client, UX flow, styles)
- Docs (`README`, `docs/*`, backend README)
- Docker (`backend/Dockerfile`, `frontend/Dockerfile`, `docker-compose.yml`)
- Test coverage and execution health

## Validation Snapshot
- Backend tests: `45 passed`
- Frontend production build: `vite build` succeeds
- Known warnings:
  - FastAPI `on_event("startup")` deprecation warning
  - Frontend bundle size warning (`~512KB` main chunk)

## Maturity Scores
- Engineering score: **6.8/10**
- Research score: **5.7/10**
- Portfolio score: **7.6/10**
- Deployment readiness: **5.4/10**

## Findings by Severity

### Critical

1. **Internal errors are exposed directly to clients**  
   - Category: **B (Security), C (API design)**
   - Evidence: `backend/app/api/routes_analyze.py`, `routes_compare.py`, `routes_export.py`, `routes_submissions.py`, `routes_leaderboard.py` convert unexpected exceptions into `HTTPException(500, detail=str(exc))`.
   - Risk: stack/driver/tokenizer internals may leak to end users and logs.
   - Recommendation: return generic 500 messages externally; log detailed errors server-side.

2. **No migrations; schema controlled by `create_all` at startup**  
   - Category: **A (Architecture), E (Database), G (Deployment)**
   - Evidence: `backend/app/main.py` uses `Base.metadata.create_all(bind=engine)`.
   - Risk: unsafe schema evolution, no rollback/versioning, deployment drift.
   - Recommendation: introduce Alembic before production data lifecycle.

3. **Leaderboard silently converts failures into fairness score `0.0`**  
   - Category: **I (Research validity), C (API design), A (Architecture)**
   - Evidence: `backend/app/services/leaderboard_service.py` catches all exceptions per sample/model and appends `0.0`.
   - Risk: hidden tokenizer/model failures become misleading rankings.
   - Recommendation: record explicit error state per model/sample, fail visibly or exclude invalid runs.

### Important

4. **Request-size/rate protections are missing**  
   - Category: **B (Security), H (Performance), G (Deployment)**
   - Evidence: analyze/compare/export accept arbitrary text lengths; no rate limiting or body size guard.
   - Risk: easy CPU/memory abuse and potential API denial-of-service.
   - Recommendation: add input length limits, request throttling, and server-side timeouts.

5. **Tokenizer counting path is memory-heavy for large inputs**  
   - Category: **H (Performance), A (Architecture)**
   - Evidence: `count_tokens()` uses `len(tokenize_text(...))`; `tokenize_text` builds full token list, converting tiktoken IDs to strings.
   - Risk: unnecessary allocations and slower throughput.
   - Recommendation: add lightweight counting path that avoids materializing full token arrays.

6. **`/leaderboard` recomputes full benchmark on every request**  
   - Category: **H (Performance), G (Deployment), A (Architecture)**
   - Evidence: `backend/app/services/leaderboard_service.py` loops across all languages/models per request.
   - Risk: latency spikes, resource contention under traffic.
   - Recommendation: cache leaderboard results with TTL and provide refresh control.

7. **Data model for submissions is denormalized**  
   - Category: **E (Database), A (Architecture)**
   - Evidence: `selected_models` stored as comma-separated string in `backend/app/db/models.py`.
   - Risk: weak queryability, brittle parsing, harder analytics.
   - Recommendation: normalize with a child table or JSON column once migrations are in place.

8. **Backend docs are inconsistent with implemented features**  
   - Category: **J (Resume/demo), A (Architecture)**
   - Evidence: `backend/README.md` still says “No database/frontend yet” and omits current endpoints (`/ready`, `/leaderboard`, `/submissions`).
   - Risk: credibility and onboarding friction for recruiters/labs.
   - Recommendation: align backend README with current architecture and endpoints.

9. **Encoding issues in demo/docs examples for multilingual text**  
   - Category: **I (Research validity), J (Resume/demo)**
   - Evidence: `docs/API_EXAMPLES.md`, `docs/DEMO_SCRIPT.md` include mojibake for Hindi/Arabic samples.
   - Risk: undermines multilingual quality claims and demo trust.
   - Recommendation: fix UTF-8 content and validate rendered markdown on GitHub.

10. **Compose setup lacks production safety defaults**  
    - Category: **G (Deployment), B (Security)**
    - Evidence: `docker-compose.yml` includes default Postgres credentials and no healthchecks/restart policies.
    - Risk: unsafe defaults copied into staging/prod; weaker operational resilience.
    - Recommendation: environment-secret injection, healthchecks, restart policy, and profiles for dev/prod.

11. **No frontend automated tests**  
    - Category: **F (Testing), D (Frontend UX)**
    - Evidence: no `frontend` test files or UI interaction tests.
    - Risk: regressions in API error states, charts, and user flow.
    - Recommendation: add minimal component + integration tests (e.g., vitest + RTL).

12. **No PostgreSQL integration tests despite production-ready claim**  
    - Category: **F (Testing), E (Database), G (Deployment)**
    - Evidence: tests only use SQLite (`backend/app/tests/conftest.py`).
    - Risk: driver/type differences appear only after deployment.
    - Recommendation: add CI matrix job with ephemeral Postgres.

### Nice-to-have

13. **Route validation logic is duplicated across endpoints**  
    - Category: **A (Architecture), C (API design)**
    - Evidence: repeated checks for empty text/model IDs/duplicates in analyze/export/submissions/compare routes.
    - Benefit: cleaner maintainability via shared validators/service layer.

14. **API lacks versioned prefix and consistent error schema contract**  
    - Category: **C (API design)**
    - Evidence: flat routes (`/analyze`, `/compare`, etc.) with ad-hoc error payloads.
    - Benefit: easier long-term compatibility and client SDK generation.

15. **Frontend UX can improve explainability and trust cues**  
    - Category: **D (Frontend UX), J (Resume/demo)**
    - Evidence: no visible “methodology assumptions / proxy warnings” near charts besides brief text.
    - Benefit: stronger research communication during demos.

16. **Observability is minimal (no structured logging/metrics/tracing)**  
    - Category: **G (Deployment), H (Performance)**
    - Evidence: no logging middleware/monitoring integration.
    - Benefit: faster incident/debug cycle post-deploy.

17. **Pinned dependency strategy is weak for reproducibility**  
    - Category: **G (Deployment), B (Security)**
    - Evidence: `backend/requirements.txt` uses unpinned packages.
    - Benefit: deterministic builds and easier security patch governance.

## Category Summary (A-J)

- **A. Architecture weaknesses:** startup `create_all`, duplicated validation logic, expensive synchronous leaderboard path.
- **B. Security issues:** raw internal error leakage, no request/rate safeguards, unsafe compose credential defaults.
- **C. API design issues:** inconsistent 500 handling, no versioning/error contract standardization.
- **D. Frontend UX issues:** no frontend tests for UX stability, limited inline explanation of methodology caveats.
- **E. Database design limitations:** denormalized `selected_models`, no migration framework, no Postgres integration test coverage.
- **F. Testing gaps:** no frontend tests, no contract tests for `/leaderboard`, no Postgres CI path.
- **G. Deployment risks:** no migration discipline, basic compose hardening missing, minimal observability.
- **H. Performance concerns:** token counting allocates full token lists, leaderboard recomputation per request.
- **I. Research-validity concerns:** silent leaderboard fallback to zero, corrupted multilingual examples in docs.
- **J. Resume/demo weaknesses:** backend README stale/inaccurate, multilingual docs rendering issue hurts credibility.

## Prioritized Next 5 Improvements (Estimated Effort)

1. **Error-handling hardening + safe 500 responses**
   - Effort: **0.5-1 day**
   - Scope: centralized exception mapping, structured logging, user-safe error messages.

2. **Migration foundation with Alembic**
   - Effort: **1-2 days**
   - Scope: baseline migration, remove runtime `create_all` dependency, document upgrade flow.

3. **Leaderboard reliability + caching**
   - Effort: **1-1.5 days**
   - Scope: explicit failure reporting, cached aggregate results, optional refresh endpoint/flag.

4. **Input guardrails + performance limits**
   - Effort: **1 day**
   - Scope: request-size caps, text length validations, faster token counting path.

5. **Documentation/portfolio cleanup + multilingual UTF-8 fix**
   - Effort: **0.5 day**
   - Scope: fix mojibake, align backend README with current capabilities, refresh demo assets.

## Deployment Recommendation
- **Should deployment happen now?**  
  **Not for public production yet.**  
  Recommendation: deploy to a private/staging environment first after Critical items 1-3 are addressed.

- **Should screenshots be created now?**  
  **Yes.**  
  The product is visually demoable now; screenshots help recruiter/research visibility immediately.

- **Should demo video be created now?**  
  **Yes, but after quick doc cleanup.**  
  Fix multilingual text rendering and stale backend README first, then record a stronger 2-3 minute demo.
