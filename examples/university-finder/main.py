"""University Finder example — search universities by name."""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")


def search(name: str) -> dict:
    url = f"{API_BASE}/v1/universities?name={urllib.parse.quote(name)}"
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read().decode())


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "Carnegie"
    result = search(query)
    for uni in result.get("data") or []:
        print(f"{uni['name']} ({uni['country_code']}) — {uni.get('website')}")
