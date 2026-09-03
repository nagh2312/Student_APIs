# University Finder (example)

Minimal example that calls the Universities API.

## Setup

```bash
# Ensure the platform API is running on :8000
export API_BASE_URL=http://localhost:8000
python main.py
```

## Architecture

```
main.py  →  GET /v1/universities?name=...
```

See `main.py` for the full request.
