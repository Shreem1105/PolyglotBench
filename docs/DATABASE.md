# Database Guide

## Current Local Default

PolyglotBench uses SQLite by default for local development:

`DATABASE_URL=sqlite:///./polyglotbench.db`

This keeps onboarding simple and does not require a separate database service.

## Why SQLite for Development

- Zero setup for local contributors
- Works well for MVP and lightweight workflows
- Easy local file-based debugging

## PostgreSQL in Production

The backend is PostgreSQL-ready through `DATABASE_URL`. To use PostgreSQL, set:

`DATABASE_URL=postgresql+psycopg2://user:password@host:5432/polyglotbench`

Both formats are supported by SQLAlchemy:
- `postgresql://...`
- `postgresql+psycopg2://...`

## Docker Compose PostgreSQL Notes

The root `docker-compose.yml` includes an optional `postgres` service:
- Image: `postgres:16-alpine`
- DB: `polyglotbench`
- User: `polyglotbench`
- Password: `polyglotbench`
- Volume: `postgres_data:/var/lib/postgresql/data`

The backend still defaults to SQLite in compose unless you switch the `DATABASE_URL` to the commented PostgreSQL example.

## Current Migration Limitation

The app currently creates tables with SQLAlchemy `Base.metadata.create_all(...)`.
It does not yet use Alembic-managed schema migrations.

## Recommended Future Improvement

Before serious production rollout, add Alembic migrations for versioned schema changes, safer rollbacks, and predictable release workflows.
