# /db-migrate

Create and apply an Alembic migration after SQLAlchemy model changes.

## Steps

1. Generate the migration (replace `$ARGS` with a short description):
   ```bash
   cd backend && uv run alembic revision --autogenerate -m "$ARGS"
   ```

2. Show the generated migration file for review.

3. Ask the user to confirm before applying.

4. Apply:
   ```bash
   cd backend && uv run alembic upgrade head
   ```

## Notes

- Always review the generated diff — autogenerate misses some changes (e.g. server defaults)
- Requires `docker compose up -d postgres` (dev DB on :5432)
- Migration files in `backend/alembic/versions/` are committed to git
