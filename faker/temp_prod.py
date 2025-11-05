from confluent_kafka import Producer
import socket

try:
    p = Producer({"bootstrap.servers": "localhost:9092", "client.id": socket.gethostname()})
except Exception:
    print("yap")
topic = "demo"

for i in range(5):
    p.produce(topic, f"msg-{i}".encode("utf-8"))
p.flush()  # wait for delivery
