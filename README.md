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
