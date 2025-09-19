"""Async HTTP client for ESPN endpoints."""

from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional

import httpx

from .config import get_settings


class ESPNClientError(RuntimeError):
    """Raised when ESPN endpoints return an error."""


class ESPNClient:
    def __init__(self) -> None:
        settings = get_settings()
        headers = {
            "Accept": "application/json",
            "User-Agent": "sportsbot-espn-mcp/1.0",
        }
        self._settings = settings
        self._client = httpx.AsyncClient(
            headers=headers,
            timeout=settings.request_timeout,
        )

    @property
    def site_base(self) -> str:
        return self._settings.site_base_url.rstrip("/")

    @property
    def core_base(self) -> str:
        return self._settings.core_base_url.rstrip("/")

    async def get_json(self, url: str, **kwargs: Any) -> Dict[str, Any]:
        resp = await self._client.get(url, **kwargs)
        if resp.status_code >= 400:
            raise ESPNClientError(
                f"ESPN request failed ({resp.status_code}): {resp.text[:200]}"
            )
        return resp.json()

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "ESPNClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()


_client_lock = asyncio.Lock()
_client: Optional[ESPNClient] = None


async def get_client() -> ESPNClient:
    global _client  # noqa: PLW0603
    async with _client_lock:
        if _client is None:
            _client = ESPNClient()
    return _client


async def shutdown_client() -> None:
    global _client  # noqa: PLW0603
    async with _client_lock:
        if _client is not None:
            await _client.close()
            _client = None
