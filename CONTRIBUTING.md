# Contributing to Student API Platform

Thank you for contributing. This project aims to be a **standardized, open-source API ecosystem** for student developers — not a random collection of endpoints.

## Quick start

```bash
git clone <repository-url>
cd Student_APIs
cp .env.example .env
docker compose up --build
```

- API: http://localhost:8000/docs  
- Portal: http://localhost:3000  

Backend-only (mock mode, no Docker DB required):

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export MOCK_MODE=true
uvicorn app.main:app --reload
```

## Development workflow

1. Open an issue first for new APIs or large features (use the **New API Proposal** template).
2. Fork and create a branch: `feature/<name>` or `fix/<name>`.
3. Follow `docs/API-STANDARDS.md` and `docs/ARCHITECTURE.md`.
4. Add tests for every module change.
5. Document data sources in `docs/DATA-SOURCES.md`.
6. Open a pull request; CI must pass.

## Adding a new API

1. Score and justify via the roadmap criteria (`docs/API-ROADMAP.md`).
2. Add OpenAPI under `specs/<api>/v1/`.
3. Implement `backend/app/modules/<api>/` with mock provider.
4. Register the router in `app/api/v1/router.py`.
5. Add portal catalog entry and docs page.
6. Complete the API quality checklist in `docs/API-STANDARDS.md` / project README.

## Code style

- Python: Ruff + type hints; pytest for tests
- Frontend: TypeScript strict; ESLint
- No secrets in git; use `.env.example` placeholders only

## Code of conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
