import sys
import os
import random
import time

# Append root src layer to local scope execution parameters
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
# Assuming your class is in a file named client.py or similar inside the src directory
from open_aiops import AIOpsClient, track_agent
# (Adjust 'client' to match whatever the actual filename is where AIOpsClient lives)

client = AIOpsClient(api_key="local_sandbox_dev_token")

@track_agent(client=client, agent_name="Routing_Agent_v1")
def execute_routing_task(query: str):
    time.sleep(random.uniform(0.2, 0.8)) # Simulate LLM round-trip delay
    if "break" in query.lower():
        raise RuntimeError("Agent recursion limit exceeded: Loop break tripped.")
    return f"Query parsed successfully: Routing execution target to main server frame."

if __name__ == "__main__":
    print("🚀 Triggering simulated agent workloads...")
    
    # 1. Simulate a success vector
    try:
        execute_routing_task(query="Process accounting balances for account #8490")
    except Exception:
        pass
        
    # 2. Simulate a break vector
    try:
        execute_routing_task(query="Force break execution thread logic loops")
    except Exception:
        print("❌ Handled sample application failure state gracefully.")