"""University ingest script (downloads Hipo MIT-licensed list when network allows)."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

try:
    import httpx
except ImportError:
    httpx = None  # type: ignore

SOURCE_URL = (
    "https://raw.githubusercontent.com/Hipo/university-domains-list/"
    "master/world_universities_and_domains.json"
)
OUT = Path(__file__).resolve().parents[2] / "data" / "universities.json"


def slugify(name: str, country_code: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:48]
    digest = hashlib.sha1(f"{name}:{country_code}".encode()).hexdigest()[:6]
    return f"{base}-{digest}" if base else digest


def normalize(raw: list[dict]) -> list[dict]:
    out = []
    for item in raw:
        name = item.get("name") or ""
        code = (item.get("alpha_two_code") or "").upper()
        if not name or not code:
            continue
        domains = item.get("domains") or []
        pages = item.get("web_pages") or []
        out.append(
            {
                "id": slugify(name, code),
                "name": name,
                "country": item.get("country") or "",
                "country_code": code,
                "state": item.get("state-province"),
                "city": None,
                "website": pages[0] if pages else None,
                "domains": domains,
                "programs": [],
                "source": "hipo",
            }
        )
    return out


def main() -> int:
    if httpx is None:
        print("httpx required", file=sys.stderr)
        return 1
    print(f"Fetching {SOURCE_URL}")
    r = httpx.get(SOURCE_URL, timeout=60.0)
    r.raise_for_status()
    data = normalize(r.json())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))
    print(f"Wrote {len(data)} universities to {OUT}")
    print("License: MIT (Hipo/university-domains-list). See docs/DATA-SOURCES.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
