# Student API Platform

**Open-source APIs for student developers.**

Build your project instead of rebuilding the infrastructure.

This repository provides a CAMARA-inspired platform: **standardized API contracts**, open-source reference implementations, mock mode for classrooms, and a developer portal — so students can find a simple, free API and start building in minutes.

> **Public deployment:** pending. Local URLs below work today. When deployed, this section will list the real HTTPS endpoints (no placeholder domains).

---

## How students can use this

You do **not** need to understand the whole repo to use the APIs. Most students only need to **call the HTTP endpoints** from their own app, homework, or hackathon project.

### Typical student workflow (under 5 minutes)

1. **Start the API** on your machine (or use a shared classroom URL when your instructor provides one).
2. **Open** http://localhost:8000/docs — interactive docs where you can try requests in the browser.
3. **Pick an API** you need (weather, universities, books, currency, etc.).
4. **Copy a request** into your project (cURL, Python, or JavaScript — examples below).
5. **Read `data`** from the JSON response and build your UI / notebook / mobile screen.

No account is required for basic use. Signup is optional and only needed if you want a higher rate limit via an API key.

### What you can build with each API

| If your project needs… | Use this API | Example student apps |
|------------------------|--------------|----------------------|
| List or search schools | **Universities** | University finder, admissions compare page, campus directory |
| Country info, capitals, currencies | **Countries** | Geography quiz, travel checklist, world facts card |
| Lat/long, place search, distance | **Geography** | Map pin demo, “distance between cities” tool |
| Current weather / forecast | **Weather** | Weather dashboard, trip packing helper, IoT display mock |
| Title / author / ISBN lookup | **Books** | Reading list app, library search, book club site |
| Exchange rates / convert money | **Currency** | FX converter, budget-in-another-currency calculator |
| Clocks & timezone conversion | **Time** | World clock, “what time is it for my teammate?” widget |

### Three ways students usually consume the APIs

**A. From your frontend (React, Next.js, plain HTML/JS)**

```javascript
const res = await fetch("http://localhost:8000/v1/weather?lat=40.44&lon=-79.99");
const { data, error } = await res.json();
if (error) {
  console.error(error.message);
} else {
  console.log(data.temperature, data.conditions);
}
```

**B. From a Python homework / Jupyter notebook**

```python
import requests

response = requests.get(
    "http://localhost:8000/v1/books/search",
    params={"q": "Clean Code"},
)
payload = response.json()
for book in payload["data"]:
    print(book["title"], "-", ", ".join(book["authors"]))
```

**C. Quick terminal check (no code yet)**

```bash
curl "http://localhost:8000/v1/countries/IN"
curl "http://localhost:8000/v1/convert?from=USD&to=INR&amount=50"
curl "http://localhost:8000/v1/universities?name=Carnegie"
```

### Classroom / offline friendly

- Run with **`MOCK_MODE=true`** so everything works **without** OpenWeather, Google, or other paid keys.
- Responses are stable sample data — great for grading, demos, and CI.
- Fair-use rate limits apply (about **60 requests/minute** anonymously; higher with an optional API key).

### Tips for assignments

- Always check `error` in the JSON before using `data`.
- Prefer query params documented in `/docs` (`page`, `limit`, `q`, `country`, etc.).
- Point your app at `http://localhost:8000` locally; change only the base URL when a public server is available.
- Explore sample apps under [`examples/`](examples/) (university finder, weather, currency, books).
- Use the portal at http://localhost:3000 for browsing APIs and a **Try It** explorer.

Step-by-step setup continues in [How to use](#how-to-use) below.

---

## Where this is useful

Use this platform whenever you need reliable, documented HTTP APIs for academic or portfolio work — without standing up databases, scraping sites, or wiring multiple vendor SDKs.

| Situation | How Student APIs helps |
|-----------|------------------------|
| **Course assignments** | Drop-in endpoints for homework (weather dashboard, country quiz, book search) with consistent JSON |
| **Hackathons** | Ship a demo in hours; mock mode works offline with no vendor API keys |
| **Portfolio / personal projects** | Focus on UI and product ideas instead of rebuilding university/geo/FX backends |
| **Mobile & web apps** | Same `/v1` contracts for React, Flutter, Swift, Android, or plain `fetch` / `requests` |
| **ML / data-science demos** | Clean sample payloads for notebooks, ETL practice, and API-consumption labs |
| **Teaching & workshops** | Instructors get a free, rate-limited teaching API; students clone and run locally |
| **Prototyping before production** | Stable response envelope (`data` / `meta` / `error`) you can later swap for your own backend |
| **Open-source learning** | Study FastAPI modules, provider abstraction, rate limits, and a Next.js developer portal |

### Example project ideas

- University finder / campus explorer
- Travel planner (countries + weather + currency + timezones)
- Book club or library search UI
- FX converter widget
- World clock / meeting scheduler across timezones
- Geocoding + distance tools for maps demos

---

## Available APIs (Phase 0)

| API | Status | Methods | Example |
|-----|--------|---------|---------|
| Universities | stable | `GET` | `/v1/universities?country=US&name=Carnegie` |
| Countries | stable | `GET` | `/v1/countries/US` |
| Geography | stable | `GET` | `/v1/geocode?q=pittsburgh` |
| Weather | stable | `GET` | `/v1/weather?lat=40.44&lon=-79.99` |
| Books | stable | `GET` | `/v1/books/search?q=Pride` |
| Currency | stable | `GET` | `/v1/convert?from=USD&to=EUR&amount=100` |
| Time | stable | `GET` | `/v1/time/convert?from=America/New_York&to=Asia/Kolkata` |
| Auth (API keys) | stable | `GET`, `POST`, `DELETE` | `/v1/auth/api-keys` |
| Catalog | stable | `GET` | `/v1/catalog` |

Anonymous access is enabled for read APIs. Optional API keys unlock higher rate limits.

**Dataset sizes (mock / offline mode):** universities ≈ 10,000 · countries = 250 · books = 25.  
List endpoints paginate by default (`page=1`, `limit=20`, max `limit=100`). Use `meta.total` and `has_next` to fetch the full set.

Full method matrix and paths: see [docs/API-STANDARDS.md](docs/API-STANDARDS.md) and Swagger at `/docs`.

---

## How to use

### 1. Run the platform locally

**Option A — Docker (recommended)**

```bash
git clone https://github.com/nagh2312/Student_APIs.git
cd Student_APIs
cp .env.example .env
docker compose up --build
```

**Option B — Backend only (Python 3.12)**

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export MOCK_MODE=true
uvicorn app.main:app --reload --port 8000
```

**Option C — Frontend portal**

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

| Service | URL |
|---------|-----|
| Developer portal | http://localhost:3000 |
| API docs (Swagger) | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Health | http://localhost:8000/health |

### 2. Call an API (no signup required)

**cURL**

```bash
curl "http://localhost:8000/v1/universities?country=US&name=Carnegie"
```

**Python**

```python
import requests

r = requests.get(
    "http://localhost:8000/v1/universities",
    params={"country": "US", "name": "Carnegie"},
)
print(r.json())
```

**JavaScript**

```javascript
const res = await fetch(
  "http://localhost:8000/v1/universities?country=US&name=Carnegie"
);
const body = await res.json();
console.log(body.data);
```

### 3. Understand the response envelope

Every endpoint returns:

```json
{
  "data": {},
  "meta": { "request_id": "req_...", "page": 1, "limit": 20, "total": 1 },
  "error": null
}
```

On failure, `data` is `null` and `error` includes `code`, `message`, and `request_id`.

### 4. Common query patterns

| Need | Pattern |
|------|---------|
| Pagination | `?page=1&limit=20` (max `limit` = 100) |
| Filter | `?country=US` |
| Search | `?name=Carnegie` or `?q=pittsburgh` |
| Sort | `?sort=name` or `?sort=-name` |

### 5. Optional API key (higher rate limits)

Default anonymous limit: **60 requests/minute**. With a key: **300 requests/minute**.

```bash
# Create a key (raw key is shown only once)
curl -X POST http://localhost:8000/v1/auth/api-keys \
  -H "Content-Type: application/json" \
  -d '{"name":"my-homework-app"}'

# Use it on subsequent requests
curl http://localhost:8000/v1/countries \
  -H "X-API-Key: sap_your_key_here"
```

Never put API keys in URLs. Keys are hashed before storage.

### 6. Try it in the portal

1. Open http://localhost:3000  
2. Browse **APIs** → pick a card (e.g. Weather)  
3. Use **Try It** with parameters  
4. Copy cURL / Python / JavaScript examples into your project  

Getting started guide: http://localhost:3000/getting-started  

### 7. Example response

```bash
curl "http://localhost:8000/v1/universities?country=US&name=Carnegie"
```

```json
{
  "data": [
    {
      "id": "cmu",
      "name": "Carnegie Mellon University",
      "country": "United States",
      "country_code": "US",
      "state": "Pennsylvania",
      "city": "Pittsburgh",
      "website": "https://www.cmu.edu",
      "domains": ["cmu.edu"]
    }
  ],
  "meta": { "page": 1, "limit": 20, "total": 1, "has_next": false },
  "error": null
}
```

More consumer samples live under [`examples/`](examples/).

---

## Mock mode

`MOCK_MODE=true` (default in Compose and local backend) returns deterministic sample data — no external API keys required for classrooms, hackathons, or CI.

Set `MOCK_MODE=false` only when PostgreSQL/Redis and provider access are configured (see `.env.example` and [docs/DATA-SOURCES.md](docs/DATA-SOURCES.md)).

---

## Architecture

```
specs/        API contracts (OpenAPI)
backend/      FastAPI reference implementation + providers
frontend/     Next.js developer portal
docs/         Roadmap, standards, architecture, data sources
examples/     Sample consumer apps
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Documentation

- [API Roadmap](docs/API-ROADMAP.md) — prioritization of 30+ API ideas
- [API Standards](docs/API-STANDARDS.md) — envelopes, pagination, errors, auth
- [Data Sources](docs/DATA-SOURCES.md) — licenses and attribution
- [Contributing](CONTRIBUTING.md) · [Governance](GOVERNANCE.md) · [Security](SECURITY.md)

## Make targets

```bash
make dev      # docker compose up --build
make test     # backend pytest
make lint
make seed
make build
```

## License

Apache License 2.0 — see [LICENSE](LICENSE).

Individual datasets retain their own licenses; see [docs/DATA-SOURCES.md](docs/DATA-SOURCES.md).
