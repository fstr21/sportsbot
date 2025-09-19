"""Configuration helpers for the SportsGameOdds MCP service."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from pydantic import BaseModel, Field, ValidationError


class Settings(BaseModel):
    api_key: str = Field(..., alias="SPORTSGAMEODDS_API_KEY")
    base_url: str = Field(
        default="https://api.sportsgameodds.com/v2",
        alias="SPORTSGAMEODDS_BASE_URL",
    )
    request_timeout: float = Field(default=30.0, alias="SPORTSGAMEODDS_TIMEOUT")

    class Config:
        allow_population_by_field_name = True


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    try:
        return Settings(**os.environ)
    except ValidationError as exc:  # pragma: no cover
        fields = ", ".join(sorted(err["loc"][0] for err in exc.errors()))
        raise RuntimeError(
            "Invalid SportsGameOdds MCP configuration; missing env vars: "
            f"{fields}"
        ) from exc


def require_api_key() -> str:
    return get_settings().api_key
