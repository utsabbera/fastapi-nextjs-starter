# /add-feature

Scaffold a full vertical slice for a new resource (e.g. `post`, `comment`).

## Checklist

Given resource name `$ARGS` (e.g. "post"):

### Backend

- [ ] `backend/app/models/$ARGS.py` — SQLAlchemy model extending `Base`
- [ ] Add import to `backend/app/models/__init__.py`
- [ ] `backend/app/schemas/$ARGS.py` — `{Name}Create`, `{Name}Update`, `{Name}Read`
- [ ] `backend/app/repositories/$ARGS.py` — `{Name}Repository` with async CRUD
- [ ] `backend/app/services/$ARGS.py` — `{Name}Service` with business logic
- [ ] `backend/app/routers/$ARGS.py` — route handlers using `DbDep`, `CurrentUserDep`
- [ ] Register router in `backend/main.py` `create_app()`
- [ ] `backend/tests/unit/test_$ARGS.py` — unit tests (no DB)
- [ ] `backend/tests/integration/test_$ARGS.py` — integration tests

### Database

- [ ] Run `/db-migrate` to create and apply the migration

### Frontend

- [ ] Run `/gen-client` to regenerate the TS client
- [ ] `frontend/src/app/$ARGS/page.tsx` — route page
- [ ] Wire up API calls via `@/lib/generated`

## Conventions

- Services raise `HTTPException`, repositories return `None` on not-found
- Response schemas never expose `hashed_password` or internal fields
- Use `DbDep` and `CurrentUserDep` from `app.core.deps` in routers
