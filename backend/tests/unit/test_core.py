"""Unit tests for core helpers."""

from app.core.responses import clamp_pagination, failure, success
from app.core.security import generate_api_key, hash_api_key, verify_api_key
from app.modules.geography.providers.base import haversine_km


def test_clamp_pagination():
    assert clamp_pagination(0, 500) == (1, 100)
    assert clamp_pagination(2, 10) == (2, 10)


def test_success_envelope():
    body = success({"ok": True}, request_id="req_1", page=1, limit=20, total=50)
    assert body["error"] is None
    assert body["meta"]["has_next"] is True


def test_failure_envelope():
    body = failure(code="X", message="Nope", request_id="r1")
    assert body["data"] is None
    assert body["error"]["code"] == "X"


def test_api_key_hash_roundtrip(monkeypatch):
    monkeypatch.setenv("API_KEY_PEPPER", "pepper")
    from app.core.config import get_settings

    get_settings.cache_clear()
    key = generate_api_key()
    h = hash_api_key(key)
    assert verify_api_key(key, h)
    assert not verify_api_key(key + "x", h)
    get_settings.cache_clear()


def test_haversine_zero():
    assert haversine_km(0, 0, 0, 0) == 0
