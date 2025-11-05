from fastapi import FastAPI, Request, HTTPException
import os
from canvas_mcp import CanvasMCPServer

app = FastAPI()

# 1️⃣  Environment variables (from Render)
API_KEY = os.environ.get("API_KEY")
CANVAS_API_TOKEN = os.environ.get("CANVAS_API_TOKEN")
CANVAS_API_URL = os.environ.get("CANVAS_API_URL")

# 2️⃣  Initialize the real Canvas MCP server
canvas_server = CanvasMCPServer(api_url=CANVAS_API_URL, api_token=CANVAS_API_TOKEN)

@app.get("/")
async def root():
    return {"message": "Canvas MCP is alive and registered."}

@app.post("/")
async def mcp_endpoint(request: Request):
    # 3️⃣  Optional: secure with your x-api-key
    if API_KEY and request.headers.get("x-api-key") != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: invalid API key")

    # 4️⃣  Pass the request directly to the Canvas MCP handler
    try:
        data = await request.json()
        response = await canvas_server.handle_request(data)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
