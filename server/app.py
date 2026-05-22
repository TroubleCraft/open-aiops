import json
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AIOps Core Ingestion Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared flat-file tracking target relative to root execution space
LOG_FILE = "../aiops_logs.json"

def append_to_log(payload: dict):
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
    logs.append(payload)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

@app.post("/v1/telemetry")
async def receive_telemetry(request: Request):
    try:
        payload = await request.json()
        append_to_log(payload)
        return {"status": "accepted", "trace_id": payload.get("trace_id")}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)