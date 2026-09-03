# Student APIs — Developer Portal

Next.js (App Router) developer portal for the Student API Platform.

## Stack

- Next.js 15 + React 19 + TypeScript
- Tailwind CSS 3
- Fetches live examples from the FastAPI backend (`NEXT_PUBLIC_API_BASE_URL`)

## Getting started

```bash
cp .env.example .env.local
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

Ensure the backend is running at the configured base URL (default `http://localhost:8000`).

## Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Development server |
| `npm run build` | Production build |
| `npm start` | Serve production build |
| `npm run lint` | ESLint |

## Environment

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_BASE_URL` | `http://localhost:8000` | Backend API origin (no trailing slash) |
| `NEXT_PUBLIC_GITHUB_URL` | repo URL | GitHub CTA target |

## Docker

```bash
docker build -t student-apis-portal .
docker run --rm -p 3000:3000 \
  -e NEXT_PUBLIC_API_BASE_URL=http://host.docker.internal:8000 \
  student-apis-portal
```

The image uses a multi-stage Node Alpine build, runs as a non-root user, and exposes port 3000.

## Pages

- `/` — Homepage
- `/apis` — API catalog with search & filters
- `/apis/[slug]` — Per-API documentation + Try It explorer
- `/getting-started` — 5-minute onboarding
- `/status` — Service status
- `/docs` — Documentation index

## Notes

- The interactive explorer never asks for or stores secrets in URLs.
- Optional API keys (when used) should be sent via the `X-API-Key` header only.
- Catalog metadata lives in `src/lib/apis.ts`.
