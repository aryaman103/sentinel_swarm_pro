from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import SQLModel, Session, create_engine, select
from models import Event
import asyncio
import os
from datetime import datetime

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./events.db")
engine = create_engine(DATABASE_URL, echo=False)
SQLModel.metadata.create_all(engine)

class ZeekLog(BaseModel):
    ts: float
    src_ip: str
    payload: str
    # ... add more fields as needed

@app.post("/ingest")
async def ingest_log(log: ZeekLog):
    # Simulate anomaly detection (for demo purposes)
    severity = 0.9  # Always high for demo
    event = Event(
        ts=log.ts,
        src_ip=log.src_ip,
        severity=severity,
        raw=log.model_dump_json()
    )
    with Session(engine) as session:
        session.add(event)
        session.commit()
    # Broadcast to WebSocket clients (dashboard)
    await manager.broadcast({
        "ts": log.ts,
        "src_ip": log.src_ip,
        "severity": severity,
        "raw": log.model_dump_json()
    })
    return JSONResponse({"status": "received"})

@app.post("/demo")
async def demo_event():
    # Create a fake event
    event_data = {
        "ts": datetime.now().timestamp(),
        "src_ip": "192.168.1.100",
        "severity": 0.95,
        "raw": '{"ts": %s, "src_ip": "192.168.1.100", "payload": "deadbeef"}' % datetime.now().timestamp()
    }
    # Optionally store in DB
    event = Event(
        ts=event_data["ts"],
        src_ip=event_data["src_ip"],
        severity=event_data["severity"],
        raw=event_data["raw"]
    )
    with Session(engine) as session:
        session.add(event)
        session.commit()
    # Broadcast to dashboard
    await manager.broadcast(event_data)
    return {"status": "demo event sent"}

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(60)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
