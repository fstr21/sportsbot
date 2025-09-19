"""Utility helpers for exercising the CollegeFootballData MCP deployment."""

from __future__ import annotations

import os
from dataclasses import dataclass

import requests

DEFAULT_BASE_URL = "https://collegefootballdatamcp-production.up.railway.app"


@dataclass
class MCPClient:
    base_url: str = DEFAULT_BASE_URL

    def _url(self, path: str) -> str:
        return f"{self.base_url.rstrip('/')}{path}"

    def health(self) -> requests.Response:
        return requests.get(self._url("/health"), timeout=30)

    def list_tools(self) -> requests.Response:
        return requests.get(self._url("/tools"), timeout=30)

    def invoke(self, tool: str, params: dict | None = None) -> requests.Response:
        payload = {"params": params or {}}
        return requests.post(self._url(f"/tools/{tool}/invoke"), json=payload, timeout=60)


def client() -> MCPClient:
    return MCPClient(base_url=os.getenv("CFBD_MCP_BASE_URL", DEFAULT_BASE_URL))
