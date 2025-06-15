import asyncio
from confluent_kafka import Consumer
import json
import numpy as np
from sklearn.ensemble import IsolationForest
from sqlmodel import Session, create_engine
from models import Event
import os
import random

print("stream_consumer.py started")

# Kafka config
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "zeek-logs")
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./events.db")
engine = create_engine(DATABASE_URL, echo=False)

print("Creating Kafka consumer...")
consumer = Consumer({
    "bootstrap.servers": KAFKA_BOOTSTRAP,
    "group.id": "sentinel-swarm",
    "auto.offset.reset": "earliest"
})
print("Kafka consumer created.")

# IsolationForest (fit incrementally)
isoforest = IsolationForest(warm_start=True, n_estimators=100, contamination=0.01)

def hex_to_vec(payload_hex: str):
    # TODO: Replace with Tiny-ViT embedding
    # For now, stub: random vector
    return np.random.rand(384)

async def consume_loop():
    print("Starting consume_loop()")
    consumer.subscribe([KAFKA_TOPIC])
    X = []
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            await asyncio.sleep(0.1)
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        try:
            log = json.loads(msg.value().decode())
            vec = hex_to_vec(log.get("payload", ""))
            X.append(vec)
            if len(X) > 100:
                X = X[-100:]
            isoforest.fit(X)
            score = -isoforest.decision_function([vec])[0]
            if score > 0.8:
                # Anomaly detected
                event = Event(
                    ts=log.get("ts"),
                    src_ip=log.get("src_ip"),
                    severity=score,
                    raw=json.dumps(log)
                )
                with Session(engine) as session:
                    session.add(event)
                    session.commit()
                # TODO: Notify websocket/UI
        except Exception as e:
            print(f"Error processing log: {e}")
        await asyncio.sleep(0.01)

if __name__ == "__main__":
    try:
        import asyncio
        asyncio.run(consume_loop())
    except Exception as e:
        print(f"Top-level exception: {e}")


