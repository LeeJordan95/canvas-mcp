from fastapi import FastAPI, Request, HTTPException
import subprocess
import json
import os

app = FastAPI()

# 1  Secret key stored in Render environment variables
API_KEY = os.environ.get("API_KEY")

@app.post("/")
async def mcp_proxy(request: Request):
    # 2  Check for correct x-api-key header
    client_key = request.headers.get("x-api-key")
    if API_KEY and client_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: invalid API key")

    # 3  Run your original MCP command
    data = await request.json()
    proc = subprocess.run(
        ["canvas-mcp-server"], input=json.dumps(data),
        text=True, capture_output=True
    )
    return {"stdout": proc.stdout, "stderr": proc.stderr}
