# Sentinel-Swarm Pro

This repository is a hands-on exploration of automated incident-response pipelines. The goal was to integrate network telemetry, real-time anomaly detection, lightweight agent logic, and disposable containment, entirely on a developer workstation.

---

## Motivation

Most academic labs stop at offline log analysis. I wanted to push further:

* **Stream-oriented ingestion** instead of batch files.  
* **Online unsupervised learning** (IsolationForest) to flag deviations immediately.  
* **Decision automation** via a deterministic agent (LangGraph FSM).  
* **Ephemeral containment** using on-demand Docker honeypots to limit blast radius.

---

## System Overview

1. **Zeek sensors** (or sample PCAP replay) generate structured JSON events.  
2. Events are buffered in a single-broker **Kafka** topic for fault-tolerant fan-out.  
3. The **stream-consumer service** featurises payloads, updates an incremental IsolationForest, and emits a severity score.  
4. A **LangGraph agent** evaluates the score:  
   * **< threshold** → persist and forward to UI.  
   * **≥ threshold** → append the source IP to a blocklist **and** spawn a new Alpine-based honeypot container with isolated networking for traffic capture.  
5. All events are stored in **SQLite** and broadcast over WebSocket to a **Vue 3 dashboard** for live monitoring.

---

## Technical Takeaways

* Built a **stateful streaming pipeline** that can keep ML models warm without full retraining cycles.  
* Implemented **container-level network isolation** and automatic teardown to safely observe malicious traffic.  
* Leveraged **LangGraph** for explicit, testable agent state transitions (log → quarantine → containment).  
* Delivered a responsive, WebSocket-driven front-end for SOC-style visibility.

---

## Repository Layout
Backend/ FastAPI + SQLModel + IsolationForest + LangGraph agent
Frontend/ Vite + Vue + Tailwind real-time dashboard
Honeypot/ Dockerfile for disposable trap container
Infra/ docker-compose, devcontainer, bootstrap scripts
Tests/ pytest (async) unit/integration tests
Docs/ sample Zeek logs, design notes
