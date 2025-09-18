"""Async HTTP client for CollegeFootballData."""

from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional

import httpx

try:  # pragma: no cover - allow package/local execution
    from .config import get_settings
except ImportError:  # pragma: no cover
    from config import get_settings  # type: ignore


class CFBDClientError(RuntimeError):
    """Raised when the upstream CollegeFootballData API returns an error."""


class CFBDClient:
    """Lightweight async client wrapping the CollegeFootballData REST API."""

    def __init__(self) -> None:
        settings = get_settings()
        headers = {
            "Authorization": f"Bearer {settings.api_key}",
            "Accept": "application/json",
            "User-Agent": "sportsbot-cfbd-mcp/1.0",
        }
        self._client = httpx.AsyncClient(
            base_url=settings.base_url,
            headers=headers,
            timeout=settings.request_timeout,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        response = await self._client.request(method, endpoint, params=params or {})
        if response.status_code >= 400:
            raise CFBDClientError(
                f"CFBD request failed ({response.status_code}): {response.text}"
            )
        if response.status_code == 204 or not response.content:
            return None
        return response.json()

    async def __aenter__(self) -> "CFBDClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()


_client_lock = asyncio.Lock()
_client: Optional[CFBDClient] = None


async def get_client() -> CFBDClient:
    """Return a shared CFBD client instance."""

    global _client  # noqa: PLW0603
    async with _client_lock:
        if _client is None:
            _client = CFBDClient()
    return _client


async def shutdown_client() -> None:
    """Dispose of the shared client (used during FastAPI shutdown)."""

    global _client  # noqa: PLW0603
    async with _client_lock:
        if _client is not None:
            await _client.close()
            _client = None
