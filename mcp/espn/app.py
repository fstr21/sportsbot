"""Simple ESPN MCP app for Railway deployment."""

from fastapi import FastAPI

app = FastAPI(title="ESPN NFL MCP", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "ESPN MCP is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# Test endpoint to verify deployment
@app.get("/test")
async def test():
    return {"test": "ESPN MCP deployment successful"}