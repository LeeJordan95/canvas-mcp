from fastapi import FastAPI, Request, HTTPException
import os, subprocess, json

app = FastAPI()

API_KEY = os.environ.get("API_KEY")

@app.get("/")
async def root():
    # simple health-check endpoint
    return {"message": "Canvas MCP server is alive."}

@app.post("/")
async def mcp_entrypoint(request: Request):
    # check x-api-key header
    if API_KEY and request.headers.get("x-api-key") != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: invalid API key")

    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON.")

    # basic MCP handshake
    if data.get("method") == "ping":
        return {"jsonrpc": "2.0", "result": "pong", "id": data.get("id")}
    if data.get("method") == "get_tools":
        return {
            "jsonrpc": "2.0",
            "result": {
                "tools": [
                    {"name": "canvas_query", "description": "Query your Canvas data."},
                ]
            },
            "id": data.get("id"),
        }

    # default: proxy everything else to the canvas-mcp-server
    proc = subprocess.run(
        ["canvas-mcp-server"],
        input=json.dumps(data),
        text=True,
        capture_output=True,
    )
    return {"jsonrpc": "2.0", "result": proc.stdout, "id": data.get("id")}
