# API Standards

Conventions for every public API in the Student API Platform.

## Base URL

```
/v1/
```

Future breaking changes use `/v2/`.

## Response Envelope

Success:

```json
{
  "data": {},
  "meta": {},
  "error": null
}
```

Error:

```json
{
  "data": null,
  "meta": {
    "request_id": "req_abc123"
  },
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "University not found",
    "details": null,
    "request_id": "req_abc123"
  }
}
```

Never expose stack traces to consumers.

## HTTP Status Codes

| Code | Usage |
|------|--------|
| 200 | Success |
| 201 | Created (API keys) |
| 204 | Deleted |
| 400 | Validation / bad request |
| 401 | Missing/invalid API key when required |
| 403 | Forbidden |
| 404 | Resource not found |
| 429 | Rate limited |
| 500 | Unexpected server error |
| 503 | Dependency unavailable |

## Pagination

```
?page=1&limit=20
```

- Default `limit`: 20
- Maximum `limit`: 100
- `meta` includes `page`, `limit`, `total`, `has_next`, `has_prev`

## Filtering, Search, Sorting

- Filter: query params matching field names (`country=US`)
- Search: `q` or resource-specific (`name=Carnegie`)
- Sort: `sort=name` / `sort=-created_at` (`-` = descending)

## Authentication

- Anonymous access allowed for most read APIs
- Optional API key via header: `X-API-Key: <key>`
- Never put API keys in URLs
- Keys are hashed (SHA-256) before storage; raw key shown once at creation

## Rate Limits

Configurable via environment:

| Tier | Default |
|------|---------|
| Anonymous | 60 req/min |
| API key | 300 req/min |

Headers:

```
X-RateLimit-Limit
X-RateLimit-Remaining
X-RateLimit-Reset
```

## Error Codes

| Code | Meaning |
|------|---------|
| `VALIDATION_ERROR` | Invalid parameters |
| `RESOURCE_NOT_FOUND` | Missing resource |
| `RATE_LIMIT_EXCEEDED` | Too many requests |
| `UNAUTHORIZED` | Invalid API key |
| `PROVIDER_ERROR` | Upstream provider failure |
| `INTERNAL_ERROR` | Unexpected error |

## Provider Abstraction

API contracts are stable. Providers implement a shared interface; responses are normalized before return. Mock mode (`MOCK_MODE=true`) provides deterministic sample data.

## Versioning & Status

Each API declares status: `experimental` | `beta` | `stable` | `deprecated`.

Breaking changes require a new major version path and CHANGELOG entry.

## Timestamps

ISO 8601 UTC (`2026-09-02T18:30:00Z`).

## Request IDs

Every response includes a `request_id` in `meta` (and in `error` when present) for support and debugging.
