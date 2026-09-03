# Architecture

CAMARA-inspired standardized API platform for student developers.

## High-Level View

```
                 API Specification (specs/)
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
        Provider A    Provider B    MockProvider
            │             │             │
            └─────────────┼─────────────┘
                          ▼
                 Normalized Service Layer
                          │
                          ▼
                    REST /v1/* APIs
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
        Developer Portal          Direct consumers
           (frontend)            (apps, SDKs, curl)
```

## Repository Layout

```
backend/          FastAPI reference implementation
frontend/         Next.js developer portal
docs/             Architecture, roadmap, standards, data sources
specs/            Versioned OpenAPI specs (contract-first artifacts)
examples/         Sample consumer projects
infrastructure/   Deployment / IaC helpers
scripts/          Cross-cutting tooling
packages/         Future official SDKs
.github/          CI/CD and contribution templates
```

## Backend Layers

1. **API routers** (`app/api/v1`, module `router.py`) — HTTP only
2. **Services** — business logic, provider selection
3. **Repositories** — SQLAlchemy persistence
4. **Providers** — external APIs / open datasets / mock
5. **Core** — config, security, rate limit, logging, dependencies

Each domain module is self-contained:

```
modules/weather/
  router.py
  service.py
  schemas.py
  providers/
```

## Data Flow (dataset-backed APIs)

```
Source → Ingest → Validate → Normalize → PostgreSQL → API
```

Scripts live under `backend/scripts/{ingest,validate,seed}`.

## Caching

Redis caches expensive provider responses (weather, FX rates) with configurable TTLs. Sensitive data is not cached.

## Auth & Rate Limiting

- Optional API keys (hashed at rest)
- Redis-backed sliding window rate limits
- Higher quotas for authenticated keys

## Observability

- `GET /health`, `/health/live`, `/health/ready`
- `GET /metrics` (Prometheus-compatible counters)
- Structured logging with request IDs

## Frontend

Next.js App Router portal. Talks only to backend HTTP APIs — never to PostgreSQL/Redis directly.

## Deployment Target

```
GitHub Actions → Backend + Frontend
                     │
              PostgreSQL + Redis
```

Public URLs are configured via environment variables (`API_BASE_URL`, `FRONTEND_URL`). No fake domains are hard-coded.

## Security Principles

- Secrets only in env / secret stores
- Non-root containers
- Input validation (Pydantic)
- CORS allowlist
- Secure headers middleware
- Dependency pinning

## Extensibility

New APIs:

1. Propose via GitHub issue template
2. Add `specs/<api>/v1/openapi.yaml`
3. Implement `backend/app/modules/<api>/`
4. Register router in `api/v1`
5. Document data sources
6. Add tests + portal catalog entry
