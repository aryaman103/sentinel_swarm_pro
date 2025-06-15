#!/bin/bash
# Inject sample Zeek logs into Kafka
KAFKA_CONTAINER=$(docker-compose ps -q kafka)
docker cp ../docs/sample_logs/ $KAFKA_CONTAINER:/tmp/
docker exec $KAFKA_CONTAINER bash -c "cat /tmp/sample_logs/*.json | kafka-console-producer.sh --broker-list localhost:9092 --topic zeek-logs"
