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
LOG_FILE = "/workspaces/open-aiops/aiops_logs.json"

def append_to_log(payload: dict):
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                     existing_data = []
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

    # Append the new data we got from the request
        existing_data.append(data)

        with open(LOG_FILE, "w") as f:
            json.dump(existing_data, f, indent=4)

@app.post("/v1/telemetry")
async def receive_telemetry(request: Request):
    data = await request.json()
    print(data)
    
    try:
        with open(LOG_FILE, "r") as f:
            existing_data = json.load(f)
            if not isinstance(existing_data, list):
                existing_data = []
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    # 1. Add the new packet to the array
    existing_data.append(data)

    # 2. Save the array to disk (aligned with the try statement)
    with open(LOG_FILE, "w") as f:
        json.dump(existing_data, f, indent=4)

    # 3. Final return at the absolute end
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)