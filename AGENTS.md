# AGENTS.md

Lean FastAPI + Next.js starter. One backend, one frontend, Makefile as the sole orchestrator. No monorepo tooling.

## Commands

```bash
make install                              # pnpm install + cd frontend && pnpm install + cd backend && uv sync
make dev                                  # runs backend :8000 and frontend :3000 concurrently
make test                                 # cd frontend && pnpm vitest run + cd backend && uv run pytest
make lint                                 # pnpm biome check frontend/src + cd backend && uv run ruff check app/
make typecheck                            # cd frontend && pnpm tsc --noEmit + cd backend && uv run mypy app/
make gen-client                           # cd frontend && pnpm openapi-ts
make db-migrate MSG="description"         # alembic revision --autogenerate + upgrade head
make db-up                                # docker compose up -d (optional — only needed for PostgreSQL)
```

Unit tests (no DB): `cd backend && uv run pytest tests/unit/ -v`

## Directory Map

```
backend/
  main.py               app factory entry point — create_app() lives here
  openapi.json          committed OpenAPI spec — source of truth for TS codegen
  app/
    core/
      config.py         pydantic-settings — all env vars
      database.py       async engine, session factory, Base, get_db()
      deps.py           DI aliases — DbDep
    models/             SQLAlchemy ORM models — import each into models/__init__.py
    schemas/            Pydantic request/response schemas
    repositories/       async DB access — no business logic, return None on not-found
    services/           business logic — raise HTTPException here, not in repositories
    routers/            thin route handlers — call services, use DI aliases
  tests/
    conftest.py         in-memory SQLite engine, db_session, client fixtures
    unit/               no DB, no HTTP
    integration/        full HTTP via AsyncClient + DI override
  alembic/              migration scripts
  pyproject.toml

frontend/
  src/
    app/                Next.js App Router pages
    components/ui/      shadcn-style components (owned code, not a package)
    lib/
      api.ts            hey-api client setup
      generated/        openapi-ts output — never hand-edit, always regenerate
  openapi-ts.config.ts  reads ../backend/openapi.json
  package.json
```

## Architecture

**Backend layers** (strict order — never skip):
```
router → service → repository → SQLAlchemy session
```

- Routers are thin: validate input, call one service method, return schema
- Services raise `HTTPException`; repositories return `None` on not-found
- Use `DbDep` from `app.core.deps` in routers — never raw `Depends(get_db)`

**DI alias pattern:**
```python
from app.core.deps import DbDep

@router.get("/items")
async def list_items(db: DbDep) -> list[ItemRead]: ...
```

**App factory** — always use `create_app()`, never import `app` directly in tests:
```python
app = create_app()
app.dependency_overrides[get_db] = lambda: db_session
```

**Type-safe API bridge:**
1. FastAPI auto-generates `backend/openapi.json`
2. `make gen-client` runs openapi-ts → writes `frontend/src/lib/generated/`
3. Frontend imports generated types and functions directly

## Adding a Feature

For a new resource (e.g. `post`):

1. `backend/app/models/post.py` — SQLAlchemy model extending `Base`
2. Add import to `backend/app/models/__init__.py`
3. `backend/app/schemas/post.py` — `PostCreate`, `PostUpdate`, `PostRead`
4. `backend/app/repositories/post.py` — async CRUD, return `None` on not-found
5. `backend/app/services/post.py` — business logic, raise `HTTPException`
6. `backend/app/routers/post.py` — route handlers using `DbDep`
7. Register router in `backend/main.py` `create_app()`
8. `make db-migrate MSG="add posts table"`
9. `make gen-client`
10. `frontend/src/app/post/page.tsx` — wire up via `@/lib/generated`

## Commit Messages

Conventional Commits — subject line enforced by the commit-msg hook.

```
<type>(<scope>): <description>
                                        ← blank line if body follows
<why this change was made>              ← optional body: explain WHY, not WHAT
                                        ← blank line before footers
Closes #123                             ← issue reference (auto-closes on merge)
BREAKING CHANGE: <description>          ← breaking change footer if applicable
```

- **Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`, `build`, `perf`, `revert`
- **Scope:** optional — name the module/area, not the ticket (`auth`, `db`, `api`)
- **Description:** imperative mood, max 72 chars, no trailing period
- **Body:** optional but encouraged for non-trivial changes — future readers need the WHY
- **Issue reference:** `Refs #123` on intermediate commits (links without closing); `Closes #123` on the final commit that completes the issue

## Critical Conventions

- Never hand-edit `frontend/src/lib/generated/` — always run `make gen-client`
- Run `make gen-client` after any FastAPI route or schema change
- Run `make db-migrate` after any SQLAlchemy model change
- `backend/openapi.json` is committed — schema drift shows as a diff in PRs
- In `.env`, list fields are JSON arrays: `CORS_ORIGINS=["http://localhost:3000"]`
- SQLite is for development — use PostgreSQL or equivalent for production

## Database

Default: `sqlite+aiosqlite:///./dev.db` (no Docker needed).

To switch to PostgreSQL:
```bash
# backend/.env
DATABASE_URL=postgresql+asyncpg://dev:dev@localhost:5432/app_dev
# then:
cd backend && uv add asyncpg
docker compose up -d
```

Tests use in-memory SQLite (`sqlite+aiosqlite:///:memory:`) with `StaticPool` — no external services needed.

## Key File Locations

| Purpose | Path |
|---|---|
| App entry point | `backend/main.py` |
| Environment config | `backend/app/core/config.py` |
| DB session + Base | `backend/app/core/database.py` |
| DI aliases | `backend/app/core/deps.py` |
| TS client config | `frontend/openapi-ts.config.ts` |
| Generated TS client | `frontend/src/lib/generated/` |
| OpenAPI spec | `backend/openapi.json` |
