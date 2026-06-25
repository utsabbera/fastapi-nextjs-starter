# AGENTS.md

Lean FastAPI + Next.js starter. One backend, one frontend, Makefile as sole orchestrator.
See `backend/AGENTS.md` and `frontend/AGENTS.md` for area-specific patterns.

## Commands

```bash
make install                          # install all deps (pnpm + uv)
make dev                              # backend :8000 + frontend :3000 concurrently
make test                             # run all tests
make lint                             # biome (frontend) + ruff (backend)
make typecheck                        # tsc (frontend) + mypy (backend)
make gen-client                       # regenerate TS client from OpenAPI spec
make db-migrate MSG="add posts table" # create + apply Alembic migration
make db-up                            # start optional PostgreSQL via Docker
```

## Directory Map

```
backend/      FastAPI app — see backend/AGENTS.md
frontend/     Next.js app — see frontend/AGENTS.md
docs/
  decisions/  Architecture Decision Records
Makefile      sole orchestrator
biome.json    JS/TS linter + formatter
lefthook.yml  git hooks
```

## Commit Messages

Conventional Commits — subject line enforced by the commit-msg hook.

```
<type>(<scope>): <description>

<why this change was made — optional body for non-trivial commits>

Refs #123       ← ongoing work on an issue
Closes #123     ← final commit that completes the issue
BREAKING CHANGE: <description>
```

Types: `feat` `fix` `docs` `style` `refactor` `test` `chore` `ci` `build` `perf` `revert`
Scope: module/area (`auth`, `db`, `api`) — not the ticket number
Description: imperative mood, max 72 chars, no trailing period

## Database

Default: `sqlite+aiosqlite:///./dev.db` — no Docker required.

To switch to PostgreSQL:
```bash
# backend/.env
DATABASE_URL=postgresql+asyncpg://dev:dev@localhost:5432/app_dev
cd backend && uv add asyncpg && make db-up
```

Tests use in-memory SQLite — no external services needed.

## Critical Constraints

- Never hand-edit `frontend/src/lib/generated/` — run `make gen-client`
- Run `make gen-client` after any FastAPI route or schema change
- Run `make db-migrate` after any SQLAlchemy model change
- `backend/openapi.json` is committed — schema drift is visible as a diff in PRs
