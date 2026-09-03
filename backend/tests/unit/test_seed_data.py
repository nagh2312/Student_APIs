"""Seed dataset completeness checks."""

from app.modules.books.router import MOCK_BOOKS
from app.modules.countries.schemas import MOCK_COUNTRIES
from app.modules.universities.mock_data import MOCK_UNIVERSITIES


def test_university_seed_is_substantial():
    assert len(MOCK_UNIVERSITIES) >= 50
    ids = {u["id"] for u in MOCK_UNIVERSITIES}
    assert "cmu" in ids
    assert "mit" in ids


def test_country_seed_is_substantial():
    assert len(MOCK_COUNTRIES) >= 50
    codes = {c["code"] for c in MOCK_COUNTRIES}
    assert {"US", "IN", "GB", "JP", "DE"} <= codes


def test_books_seed_is_substantial():
    assert len(MOCK_BOOKS) >= 20
