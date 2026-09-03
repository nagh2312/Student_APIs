"""University seed data — Hipo open list (MIT) bundled for mock/offline use."""

from __future__ import annotations

from app.data import universities as load_universities

# Loaded once; ~10k entries from docs/DATA-SOURCES.md (Hipo university-domains-list).
MOCK_UNIVERSITIES: list[dict] = load_universities()
