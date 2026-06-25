# Claude Code Guide

## Permitted Operations (pre-approved)

- `pnpm *` — frontend and root package management
- `uv run *`, `uv sync *` — Python environment and task runner
- `docker compose *` — local infra
- `alembic *` — migrations (run from `backend/`)
- `git status`, `git diff *`, `git log *`, `git worktree *`
- `curl http://localhost:*` — local API testing
- `make *` — orchestration

## File Locations

| Purpose | Path |
|---|---|
| FastAPI entry point | `backend/main.py` |
| App config | `backend/app/core/config.py` |
| DB session | `backend/app/core/database.py` |
| DI aliases | `backend/app/core/deps.py` |
| Generated TS client | `frontend/src/lib/generated/` (never hand-edit) |
| OpenAPI spec | `backend/openapi.json` (committed) |

## FastAPI Patterns

**DI aliases** — use `DbDep` in routers, never raw `Depends()`:
```python
from app.core.deps import DbDep

@router.get("/items")
async def list_items(db: DbDep) -> list[ItemRead]: ...
```

**App factory** — always use `create_app()`, never import `app` directly in tests:
```python
# tests/conftest.py
app = create_app()
app.dependency_overrides[get_db] = lambda: db_session
```

**Service raises, repository doesn't** — services raise `HTTPException`; repositories return `None` on not-found.

## pydantic-settings List Fields

In `.env`, list fields must be JSON arrays:
```
CORS_ORIGINS=["http://localhost:3000","https://example.com"]
```

## Test Patterns

- Unit tests in `backend/tests/unit/` — no DB, no HTTP
- Integration tests in `backend/tests/integration/` — use in-memory SQLite, no external services needed
- Run unit tests: `cd backend && uv run pytest tests/unit/ -v`
- Run all tests: `cd backend && uv run pytest`

## Worktree Workflow

For isolated agent tasks: `git worktree add _worktrees/<task-name> -b <task-name>`
