"""Rate limiting middleware using Redis."""

import time
from typing import Callable
from fastapi import Request, HTTPException, status
from redis.asyncio import Redis


class RateLimiter:
    """Rate limiter using Redis for distributed rate limiting."""

    def __init__(self, redis: Redis):
        """Initialize rate limiter with Redis client.

        Args:
            redis: Redis client instance
        """
        self.redis = redis

    async def check_rate_limit(
        self,
        key: str,
        max_requests: int,
        window_seconds: int = 60,
    ) -> tuple[bool, dict[str, int]]:
        """Check if rate limit is exceeded.

        Args:
            key: Unique identifier for the rate limit (e.g., API key + endpoint)
            max_requests: Maximum number of requests allowed in the window
            window_seconds: Time window in seconds

        Returns:
            Tuple of (is_allowed, metadata) where metadata contains:
            - current: current request count
            - limit: maximum allowed requests
            - remaining: remaining requests
            - reset: timestamp when the limit resets
        """
        now = int(time.time())
        window_start = now - window_seconds

        # Redis key for this rate limit
        redis_key = f"rate_limit:{key}"

        # Remove old entries outside the window
        await self.redis.zremrangebyscore(redis_key, 0, window_start)

        # Count requests in current window
        current_count = await self.redis.zcard(redis_key)

        # Calculate metadata
        remaining = max(0, max_requests - current_count)
        reset_at = now + window_seconds

        if current_count >= max_requests:
            return False, {
                "current": current_count,
                "limit": max_requests,
                "remaining": 0,
                "reset": reset_at,
            }

        # Add current request
        await self.redis.zadd(redis_key, {str(now): now})
        await self.redis.expire(redis_key, window_seconds)

        return True, {
            "current": current_count + 1,
            "limit": max_requests,
            "remaining": remaining - 1,
            "reset": reset_at,
        }


def create_rate_limit_dependency(
    redis_getter: Callable,
    max_requests: int,
    window_seconds: int = 60,
    endpoint_name: str = "default",
):
    """Create a FastAPI dependency for rate limiting.

    Args:
        redis_getter: Function to get Redis client
        max_requests: Maximum requests allowed in window
        window_seconds: Time window in seconds
        endpoint_name: Name of the endpoint for rate limit key

    Returns:
        Async dependency function
    """

    async def rate_limit_dependency(request: Request, api_key: str):
        """Check rate limit for this request."""
        redis = redis_getter()
        limiter = RateLimiter(redis)

        # Create unique key based on API key and endpoint
        rate_key = f"{api_key}:{endpoint_name}"

        is_allowed, metadata = await limiter.check_rate_limit(
            rate_key, max_requests, window_seconds
        )

        # Add rate limit headers to response
        request.state.rate_limit_headers = {
            "X-RateLimit-Limit": str(metadata["limit"]),
            "X-RateLimit-Remaining": str(metadata["remaining"]),
            "X-RateLimit-Reset": str(metadata["reset"]),
        }

        if not is_allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "RATE_LIMIT_EXCEEDED",
                    "message": f"Rate limit exceeded. Try again in {metadata['reset'] - int(time.time())} seconds.",
                    "limit": metadata["limit"],
                    "reset": metadata["reset"],
                },
                headers={
                    "X-RateLimit-Limit": str(metadata["limit"]),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(metadata["reset"]),
                    "Retry-After": str(metadata["reset"] - int(time.time())),
                },
            )

        return api_key

    return rate_limit_dependency
