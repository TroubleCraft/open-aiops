import json
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

DB_URL = "postgresql://postgres:wHBB7+&gKBSAQMj@db.yjlwxzqkjjwfyfjgblkp.supabase.co:5432/postgres"

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
    
    metrics = data.get("metrics", {})
    error_obj = data.get("error") or {}
    
    try:
        # Establish connection to Supabase
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO telemetry_logs (trace_id, agent_name, status, timestamp, latency_seconds, total_tokens, error_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (
            data.get("trace_id"),
            data.get("agent_name"),
            data.get("status"),
            data.get("timestamp"),
            data.get("latency_seconds", 0.0),
            metrics.get("total_tokens", 0),
            error_obj.get("type", "None") if error_obj else "None"
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Database insertion failed: {e}")
        return {"status": "error", "message": str(e)}

    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)