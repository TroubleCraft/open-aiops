# open-aiops (Prototype)

A lightweight, local-first engine built to capture traces, audit token burn, and catch infinite loops across multi-agent workflows. 

Traditional observability tools treat LLM applications like single-turn API endpoints. `open-aiops` is built differently—it isolates parent-child execution graphs to monitor exactly how autonomous agents plan, select tools, and manage state transitions in real time.

---

## Core Features

*   **Zero-Config Decorator Loop:** Instrument any agent workflow using a single `@track_agent` Python hook.
*   **Loop Detection Circuit-Breaker:** Automatically identifies when an agent gets caught executing repetitive tool loops before running up a massive token bill.
*   **Asynchronous Dual-Plane Telemetry:** Captures operational metrics without injecting blocking latency into your agent's execution thread.
*   **Live Stream Terminal Dashboard:** A local, auto-refreshing Streamlit frontend mapping token expenses, execution statuses, and parent-span latency timelines side by side.

---

## Architecture Overview

The system runs a split-plane architecture locally on your machine to ensure high throughput:

## Development — Setup

Use the included `setup_env.sh` to create and activate a Python virtual environment and install dependencies.

Run these commands in your VS Code Bash terminal from the repository root:

```bash
# make the script executable (optional)
chmod +x setup_env.sh

# recommended: source the script so the venv remains active in your shell
source setup_env.sh

# or run non-interactively (creates venv and installs packages, but activation won't persist)
./setup_env.sh
```

Notes:
- The script dynamically locates the repository root, prefers `.venv` but will create one if missing.
- It attempts to source the activation script using a forward-slash path (`.venv/Scripts/activate`) for Windows Git Bash compatibility, and falls back to Unix-style `bin/activate` when appropriate.
- If `requirements.txt` exists, packages will be upgraded/installed automatically.

