"""Configuration helpers for the ESPN MCP service."""

from __future__ import annotations

import os
from functools import lru_cache

from pydantic import BaseModel, Field


class Settings(BaseModel):
    site_base_url: str = Field(
        default="https://site.api.espn.com/apis/site/v2/sports/football/nfl",
        alias="ESPN_SITE_BASE_URL",
    )
    core_base_url: str = Field(
        default="https://sports.core.api.espn.com/v2/sports/football/leagues/nfl",
        alias="ESPN_CORE_BASE_URL",
    )
    request_timeout: float = Field(default=30.0, alias="ESPN_REQUEST_TIMEOUT")

    class Config:
        populate_by_name = True


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(**os.environ)
