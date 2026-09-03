"""Security helpers — API key hashing and generation."""

from __future__ import annotations

import hashlib
import secrets

from app.core.config import get_settings


def generate_api_key() -> str:
    """Generate a URL-safe API key with a recognizable prefix."""
    return f"sap_{secrets.token_urlsafe(32)}"


def hash_api_key(raw_key: str) -> str:
    """Hash an API key with pepper. Never store raw keys."""
    pepper = get_settings().api_key_pepper
    return hashlib.sha256(f"{pepper}:{raw_key}".encode()).hexdigest()


def verify_api_key(raw_key: str, key_hash: str) -> bool:
    return secrets.compare_digest(hash_api_key(raw_key), key_hash)
