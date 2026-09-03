# Infrastructure

Deployment helpers and target architecture for public hosting.

## Target architecture

```
GitHub Actions → build & test
       │
       ├─ Backend (container) → public API URL + HTTPS
       ├─ Frontend (container / static) → developer portal
       ├─ PostgreSQL (managed)
       └─ Redis (managed)
```

## Environment

Configure via host secrets (never commit):

- `DATABASE_URL`
- `REDIS_URL`
- `CORS_ORIGINS` (portal origin)
- `API_BASE_URL` / `FRONTEND_URL`
- `API_KEY_PEPPER` / `SECRET_KEY`
- `MOCK_MODE=false` for production with live providers
- Provider keys only when required (`WEATHER_API_KEY`, etc.)

## Domain plan

```
api.<domain>     → backend
docs.<domain>    → portal /docs routes or docs subdomain
status.<domain>  → /status
```

Until a custom domain is available, use the hosting provider's assigned HTTPS URL.

## Status

**Public deployment: pending.**

No cloud credentials / Docker runtime were available in the bootstrap environment.
When you deploy (Railway, Fly.io, Render, Cloud Run, etc.), update the root README
with the real URLs and verify each public endpoint.
