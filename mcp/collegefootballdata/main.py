"""FastAPI application exposing CollegeFootballData MCP tools."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

try:  # pragma: no cover - allow module execution both packaged and standalone
    from .cfbd_client import CFBDClientError, get_client, shutdown_client
    from .config import get_settings, require_api_key
    from .tools import ToolSpec, get_tool, list_tools
except ImportError:  # pragma: no cover
    from cfbd_client import CFBDClientError, get_client, shutdown_client  # type: ignore
    from config import get_settings, require_api_key  # type: ignore
    from tools import ToolSpec, get_tool, list_tools  # type: ignore

app = FastAPI(title="CollegeFootballData MCP", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InvokeRequest(BaseModel):
    """Body for tool invocation requests."""

    params: Dict[str, Any] = Field(default_factory=dict)


class InvokeResponse(BaseModel):
    """Structured response for tool invocations."""

    tool: str
    params: Dict[str, Any]
    data: Any


class ToolDescriptor(BaseModel):
    name: str
    method: str
    endpoint: str
    description: str

    @classmethod
    def from_spec(cls, spec: ToolSpec) -> "ToolDescriptor":
        return cls(**asdict(spec))


@app.on_event("startup")
async def ensure_configuration() -> None:
    # Force-load settings to fail fast if variables are missing
    get_settings()
    require_api_key()


@app.on_event("shutdown")
async def cleanup_clients() -> None:
    await shutdown_client()


@app.get("/health")
async def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/tools", response_model=list[ToolDescriptor])
async def list_available_tools() -> list[ToolDescriptor]:
    return [ToolDescriptor.from_spec(spec) for spec in list_tools()]


@app.post("/tools/{tool_name}/invoke", response_model=InvokeResponse)
async def invoke_tool(tool_name: str, request: InvokeRequest) -> InvokeResponse:
    try:
        spec = get_tool(tool_name)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    client = await get_client()
    try:
        data = await client.request(spec.method, spec.endpoint, params=request.params)
    except CFBDClientError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return InvokeResponse(tool=spec.name, params=request.params, data=data)
