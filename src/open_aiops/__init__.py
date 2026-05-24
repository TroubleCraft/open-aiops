

__all__ = ["AIOpsClient", "track_agent"]

import time
import functools
import json
import uuid
import requests
from typing import Dict, Any, Callable

class AIOpsClient:
    def __init__(self, api_key: str, endpoint: str = "http://127.0.0.1:8000/v1/telemetry"):
        self.api_key = api_key
        self.endpoint = endpoint

    def send_trace(self, payload: Dict[str, Any]):
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            # Fired synchronously for prototype; will use async handlers in production
            requests.post(self.endpoint, json=payload, headers=headers, timeout=2)
        except Exception as e:
            print(f"⚠️ [AIOps SDK] Telemetry delivery bottleneck encountered: {e}")

def track_agent(client: AIOpsClient, agent_name: str):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            run_id = str(uuid.uuid4())
            start_time = time.time()
            input_data = {"args": [str(a) for a in args], "kwargs": {k: str(v) for k, v in kwargs.items()}}
            
            trace_payload = {
                "trace_id": run_id,
                "agent_name": agent_name,
                "status": "RUNNING",
                "timestamp": time.time(),
                "inputs": input_data
            }

            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                trace_payload.update({
                    "status": "SUCCESS",
                    "outputs": str(result),
                    "latency_seconds": round(execution_time, 3),
                    "metrics": {
                        "prompt_tokens": len(str(input_data)) // 4,
                        "completion_tokens": len(str(result)) // 4,
                        "total_tokens": (len(str(input_data)) + len(str(result))) // 4
                    }
                })
                client.send_trace(trace_payload)
                return result

            except Exception as e:
                execution_time = time.time() - start_time
                trace_payload.update({
                    "status": "FAILED",
                    "latency_seconds": round(execution_time, 3),
                    "error": {"type": e.__class__.__name__, "message": str(e)},
                    "metrics": {
                        "prompt_tokens": len(str(input_data)) // 4,
                        "completion_tokens": 0,
                        "total_tokens": len(str(input_data)) // 4
                    }
                })
                client.send_trace(trace_payload)
                raise e
        return wrapper
    return decorator