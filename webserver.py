from fastapi import FastAPI, Request, HTTPException
import os, subprocess, json

app = FastAPI()

API_KEY = os.environ.get("API_KEY")

@app.get("/")
async def root():
    return {"message": "Canvas MCP server proxy is alive."}

@app.post("/")
async def handle_request(request: Request):
    if API_KEY and request.headers.get("x-api-key") != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: invalid API key")

    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Run the actual canvas-mcp-server CLI command
    proc = subprocess.run(
        ["canvas-mcp-server"],
        input=json.dumps(data),
        text=True,
        capture_output=True,
    )

    return {
        "jsonrpc": "2.0",
        "result": proc.stdout or proc.stderr,
        "id": data.get("id"),
    }
