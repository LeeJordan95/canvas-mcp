from fastapi import FastAPI, Request
import subprocess
import json

app = FastAPI()

@app.post("/")
async def mcp_proxy(request: Request):
    data = await request.json()
    proc = subprocess.run(
        ["canvas-mcp-server"], input=json.dumps(data),
        text=True, capture_output=True
    )
    return {"stdout": proc.stdout, "stderr": proc.stderr}