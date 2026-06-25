# /gen-client

Regenerate the TypeScript API client from the committed OpenAPI spec.

## Steps

1. Start the backend dev server (if not running):
   ```bash
   cd backend && uv run fastapi dev main.py &
   sleep 3
   ```

2. Export the live OpenAPI spec:
   ```bash
   curl http://localhost:8000/openapi.json > backend/openapi.json
   ```

3. Run codegen:
   ```bash
   cd frontend && pnpm openapi-ts
   ```

4. Typecheck the frontend to confirm no type errors:
   ```bash
   cd frontend && pnpm tsc --noEmit
   ```

5. Stage the generated files:
   ```bash
   git add backend/openapi.json frontend/src/lib/generated/
   ```

## When to Run

Run after any FastAPI route, schema, or response model change.
The committed `backend/openapi.json` is the source of truth — schema drift shows as a visible diff in PRs.
