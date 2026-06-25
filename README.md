# FastAPI Next.js Starter

A lean starter for small-to-medium projects: one FastAPI backend, one Next.js frontend, wired by a Makefile. No monorepo tooling.

## Stack

| Layer | Tech |
|---|---|
| Backend | Python 3.13, FastAPI, SQLAlchemy 2, Alembic, uv |
| Frontend | Next.js 16, React 19, TypeScript 6, Tailwind CSS 4 |
| Database | SQLite by default — swap to any SQLAlchemy-compatible DB via `DATABASE_URL` |
| Linting | Ruff + mypy (backend), Biome (frontend) |
| Git hooks | Lefthook |

## Prerequisites

- Python 3.13+ (`pyenv` or `.python-version`)
- Node 22+ (`nvm` or `.nvmrc`)
- pnpm 9+
- uv

## Quick Start

```bash
make install
cp backend/.env.example backend/.env
cd backend && uv run alembic upgrade head
make dev
```

Backend runs at `http://localhost:8000`, frontend at `http://localhost:3000`.

## Switching Databases

SQLite is the default (no Docker needed). To use PostgreSQL:

```bash
# backend/.env
DATABASE_URL=postgresql+asyncpg://dev:dev@localhost:5432/app_dev

# install the postgres driver
cd backend && uv add asyncpg

# start postgres
docker compose up -d
```

## Key Commands

```bash
make install       # install all deps
make dev           # run backend + frontend concurrently
make test          # run all tests
make lint          # biome + ruff
make typecheck     # tsc + mypy
make gen-client    # regenerate TS client from backend OpenAPI spec
make db-migrate MSG="add posts table"  # create + apply Alembic migration
make db-up         # start optional PostgreSQL via Docker
```

## Project Structure

```
backend/    FastAPI app (Python)
frontend/   Next.js app (TypeScript)
Makefile    sole orchestrator
```

See `AGENTS.md` for detailed architecture and conventions.
