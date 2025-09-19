"""Configuration helpers for the CollegeFootballData MCP service."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, ConfigDict


class Settings(BaseModel):
    """Runtime configuration derived from environment variables."""

    api_key: str = Field(..., alias="COLLEGE_FOOTBALL_DATA_API_KEY")
    base_url: str = Field(
        default="https://api.collegefootballdata.com",
        alias="COLLEGE_FOOTBALL_DATA_BASE_URL",
    )
    request_timeout: float = Field(default=30.0, alias="CFBD_REQUEST_TIMEOUT")

    model_config = ConfigDict(populate_by_name=True)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings, raising a helpful error if invalid."""

    try:
        return Settings(**os.environ)
    except ValidationError as exc:  # pragma: no cover - exercised at runtime
        fields = ", ".join(sorted(err["loc"][0] for err in exc.errors()))
        raise RuntimeError(
            f"Invalid CollegeFootballData MCP configuration; check environment variables: {fields}"
        ) from exc


def require_api_key() -> str:
    """Convenience accessor that fails fast when no API key is present."""

    return get_settings().api_key
