from confluent_kafka import Producer

p = Producer({'bootstrap.servers': 'localhost:9092'})
with open('docs/sample_logs/sample1.json', 'r') as f:
    for line in f:
        p.produce('zeek-logs', line.encode('utf-8'))
        p.flush()
print("Sample log sent to Kafka!")
