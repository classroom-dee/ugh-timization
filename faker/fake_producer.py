import os
import orjson as json
import time
from helpers import generate_row
import numpy as np

from confluent_kafka import Producer
from prometheus_client import start_http_server, Counter, Gauge, Histogram
import socket


BROKERS = os.getenv("BROKERS", "localhost:9092")
TOPIC = os.getenv("TOPIC", "loadtest")
RATE = int(os.getenv("RATE", "5")) # rows per sec
PAYLOAD = int(os.getenv("PAYLOAD", "600")) # the fakegen generates at most ~520-ish bytes per row
METRICS_PORT = int(os.getenv("PROD_METRICS_PORT", "8000"))

# Prom
prod_msgs = Counter("kafka_producer_messages_total", "Total messages produced")
prod_bytes = Counter("kafka_producer_bytes_total", "Total bytes produced")
prod_rate = Gauge("kafka_producer_rate", "Msgs/sec (1s window)")
ack_hist = Histogram(
    "Kafka_producer_ack_latency_seconds",
    "Produce ack latency",
    buckets=(.001, .002, .005, .01, .02, .05, .1, .2, .5, 1, 2, 5)
)

try:
    p = Producer({
        "bootstrap.servers": BROKERS,
        "acks": "all",
        "queue.buffering.max.messages": 200_000,
        "linger.ms": 5,
        "compression.type": "lz4",
        "client.id": socket.gethostname()
    })
except Exception as e:
    print(f"error: {e}")

def dr_cb(err, msg, t0):
    if not err:
        ack_hist.observe(time.time() - t0)

def build_payload(i):
    """Generate a row and add padding to maintain consistent size to facilitate precise throughput measurement"""
    payload = {"t0": time.time(), "i": i, "payload": generate_row()}
    proto = json.dumps(payload, default=lambda o: int(o) if isinstance(o, np.integer) else o) # or maybe just use plain int from the start?
    pad = b"x" * (PAYLOAD - len(proto))
    return proto + pad


if __name__ == "__main__":
    start_http_server(METRICS_PORT)
    print(f"[producer] metrics at: {METRICS_PORT}/metrics")
    start = time.time()
    interval = 1.0
    sent = 0
    window_start = start

    while True:
        now = time.time()
        should_have_sent = int((now - start) * RATE) # throttle
        while sent < should_have_sent:
            t0 = time.time()
            p.produce(TOPIC, build_payload(sent), callback=lambda err, msg, t0=t0: dr_cb(err, msg, t0))
            prod_msgs.inc()
            prod_bytes.inc(PAYLOAD)
            sent += 1
            p.poll(0)

