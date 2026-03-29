# Coffee Machine Execution Plan

## Scope
- Build a Next.js frontend and FastAPI backend that implement the coffee machine flow.
- Persist machine resources and money in SQLite.
- Package backend + static frontend in one Docker container.

## Milestones
1. Foundation: create project structure and minimal docs.
2. Backend: implement resource checks, coin processing, transactions, and report API.
3. Frontend: wire command-driven UI to backend APIs and required color palette.
4. AI integration: add OpenRouter endpoint using `openai/gpt-oss-120b`.
5. Runtime: add Dockerfile and start/stop scripts for macOS, Linux, and Windows.
6. Validation: add tests for machine logic and API flow.

## Risks
- Missing `OPENROUTER_API_KEY` should not break the app.
- Frontend static build must exist for FastAPI to serve at `/`.

## Acceptance Checks
- Drink orders enforce resources and money rules.
- `report` returns current machine state.
- Overpayment returns change rounded to 2 decimals.
- State changes persist across API requests.
- Docker container serves API and frontend from one process.
