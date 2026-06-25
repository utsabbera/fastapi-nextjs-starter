# Agent Guide

A lean FastAPI + Next.js starter for small-to-medium projects. One backend, one frontend, wired by a Makefile.

## Quick Start

```bash
make install                              # install all deps (pnpm + uv)
cd backend && uv run alembic upgrade head # apply migrations
make dev                                  # backend :8000, frontend :3000
```

The default database is SQLite (`backend/dev.db`) — no Docker required.
To switch to PostgreSQL: update `DATABASE_URL` in `backend/.env` and run `uv add asyncpg`.

## Directory Map

```
backend/            FastAPI (Python 3.13, uv)
  app/
    core/           config, database, deps
    models/         SQLAlchemy ORM models (add yours here)
    schemas/        Pydantic request/response schemas
    repositories/   async DB access (no business logic)
    services/       business logic (raises HTTPException)
    routers/        thin route handlers
  tests/
  main.py           app factory entry point
  openapi.json      committed spec — source of truth

frontend/           Next.js 15 App Router (pnpm)
  src/
    app/            routes
    components/ui/  shadcn components (owned code)
    lib/
      api.ts        hey-api client setup
      generated/    openapi-ts output — never hand-edit
```

## Key Commands

| Task | Command |
|---|---|
| Regenerate TS client | `make gen-client` or `/gen-client` |
| New migration | `make db-migrate MSG="add posts table"` or `/db-migrate` |
| Scaffold feature | `/add-feature` |
| Lint all | `make lint` |
| Typecheck all | `make typecheck` |
| Run all tests | `make test` |
| Start PostgreSQL | `make db-up` (optional — only needed if using Postgres) |

## Architecture

- **FastAPI patterns**: `create_app()` factory, `DbDep` DI alias, router → service → repository layers
- **Type-safe bridge**: FastAPI exports `backend/openapi.json` → `make gen-client` → `frontend/src/lib/generated/`
- **Migrations**: Alembic autogenerate — always review generated files before applying
- **Database**: SQLite by default (zero-config); swap to PostgreSQL, MySQL, or any SQLAlchemy-compatible DB via `DATABASE_URL`

## Critical Conventions

- Never hand-edit `frontend/src/lib/generated/` — always regenerate via `make gen-client`
- Run `make gen-client` after any FastAPI route or schema change
- Run `/db-migrate` after any SQLAlchemy model change
- `backend/openapi.json` is committed — schema drift shows as a visible diff in PRs
- SQLite is for development; use PostgreSQL or equivalent for production
