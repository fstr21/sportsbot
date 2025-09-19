"""FastAPI application exposing ESPN MCP tools."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .espn_client import shutdown_client
from .tools import ToolSpec, invoke_tool, list_tools

app = FastAPI(title="ESPN NFL MCP", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ToolDescriptor(BaseModel):
    name: str
    method: str
    description: str

    @classmethod
    def from_spec(cls, spec: ToolSpec) -> "ToolDescriptor":
        return cls(**spec.__dict__)


class InvokeRequest(BaseModel):
    params: Dict[str, Any] = Field(default_factory=dict)


class InvokeResponse(BaseModel):
    tool: str
    params: Dict[str, Any]
    data: Any


@app.get("/health")
async def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/tools", response_model=list[ToolDescriptor])
async def list_available_tools() -> list[ToolDescriptor]:
    return [ToolDescriptor.from_spec(spec) for spec in list_tools()]


@app.post("/tools/{tool_name}/invoke", response_model=InvokeResponse)
async def invoke(tool_name: str, request: InvokeRequest) -> InvokeResponse:
    try:
        payload = await invoke_tool(tool_name, request.params)
    except HTTPException as exc:
        raise exc
    return InvokeResponse(**payload)


@app.on_event("shutdown")
async def cleanup_clients() -> None:
    await shutdown_client()
