"""Redis-backed sliding-window rate limiting."""

from __future__ import annotations

import time
from dataclasses import dataclass

from redis.asyncio import Redis

from app.core.config import Settings


@dataclass
class RateLimitResult:
    allowed: bool
    limit: int
    remaining: int
    reset_at: int


async def check_rate_limit(
    redis: Redis | None,
    *,
    key: str,
    limit: int,
    window_seconds: int,
) -> RateLimitResult:
    """Increment counter for key; allow if under limit.

    If Redis is unavailable, fail open (allow) so local/demo stays usable.
    """
    now = int(time.time())
    reset_at = now + window_seconds

    if redis is None:
        return RateLimitResult(
            allowed=True, limit=limit, remaining=limit - 1, reset_at=reset_at
        )

    bucket = f"rl:{key}:{now // window_seconds}"
    try:
        count = await redis.incr(bucket)
        if count == 1:
            await redis.expire(bucket, window_seconds)
        remaining = max(0, limit - int(count))
        allowed = int(count) <= limit
        return RateLimitResult(
            allowed=allowed,
            limit=limit,
            remaining=remaining,
            reset_at=reset_at,
        )
    except Exception:
        return RateLimitResult(
            allowed=True, limit=limit, remaining=limit - 1, reset_at=reset_at
        )


def resolve_limit(settings: Settings, authenticated: bool) -> int:
    if authenticated:
        return settings.rate_limit_authenticated
    return settings.rate_limit_anonymous
