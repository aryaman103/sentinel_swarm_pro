<h1 align="center">🛰️ Sentinel-Swarm Pro</h1>

<p align="center">
  <a href="https://github.com/aryaman103/sentinel_swarm_pro/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/aryaman103/sentinel_swarm_pro/ci.yml?label=build" alt="build status">
  </a>
  <a href="https://github.com/aryaman103/sentinel_swarm_pro/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/aryaman103/sentinel_swarm_pro" alt="license">
  </a>
  <img src="https://img.shields.io/github/languages/top/aryaman103/sentinel_swarm_pro" alt="top language">
  <img src="https://img.shields.io/badge/python-3.11-blue.svg" alt="python 3.11">
</p>

> **Mission-critical cyber defense in a box.**  
> Sentinel-Swarm Pro ingests live **Zeek** logs, applies streaming anomaly
> detection, and—when things look shady—launches a disposable **Docker honeypot**
> so autonomous agents can verify or contain the threat.  
> Think of it as a self-healing SOC side-kick built with lightweight,
> resume-ready tech.

---

## ✨ Why it matters
* **Multimodal security pipeline** – log streams, ML, LangGraph agents, and
  reactive honeypots in one repo.  
* **Production-ish infra** – single-node Kafka + FastAPI + Vue dashboard shipped
  via Docker-Compose for instant demos.  
* **Upskilling magnet** – showcases anomaly detection, container orchestration,
  WebSockets, and SQLModel—prime talking points for 2025 security/SWE roles.

---

## 🏗️ Architecture

```mermaid
flowchart LR
  subgraph Log_Pipeline
    Z(Zeek Sensors) -->|JSON logs| K((Kafka))
    K --> C[Stream Consumer<br/>(IsolationForest)]
    C --> DB[(SQLite)]
  end

  C -- anomaly event --> AG[LangGraph Agent]
  AG -- spin-up --> HP{{Ephemeral Honeypot}}
  AG -- websocket --> VUE[Vue Dashboard]

Data flow (30 000 ft)

Zeek publishes raw events ➜ Kafka

Stream Consumer performs incremental IsolationForest scoring

Anomalies hit the LangGraph agent ➜ either log only or
docker run honeypot …

Everything is persisted in SQLite and streamed to the Vue UI"