"""Load bundled open seed datasets for mock / offline mode."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent


@lru_cache
def load_json(name: str) -> list[dict]:
    path = DATA_DIR / name
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON list in {path}")
    return data


def universities() -> list[dict]:
    return load_json("universities.json")


def countries() -> list[dict]:
    return load_json("countries.json")


def books() -> list[dict]:
    return load_json("books.json")
