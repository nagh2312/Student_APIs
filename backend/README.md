# Student API Platform — Backend

FastAPI reference implementation of standardized student APIs.

## Quick start (mock mode)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
export MOCK_MODE=true
uvicorn app.main:app --reload --port 8000
```

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI: http://localhost:8000/openapi.json

## APIs (v1)

| API | Paths |
|-----|-------|
| Universities | `/v1/universities` |
| Countries | `/v1/countries` |
| Geography | `/v1/geocode`, `/v1/reverse-geocode`, `/v1/distance`, `/v1/coordinates/{place}` |
| Weather | `/v1/weather`, `/forecast`, `/historical` |
| Books | `/v1/books`, `/search`, `/isbn/{isbn}` |
| Currency | `/v1/currencies`, `/v1/rates`, `/v1/convert` |
| Time | `/v1/time`, `/v1/timezones`, `/v1/time/convert` |
| Auth | `/v1/auth/api-keys` |

## Tests

```bash
MOCK_MODE=true pytest -q
```

## Docker

Built from the repository root via `docker compose up`.
