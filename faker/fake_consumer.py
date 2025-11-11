import os
import time
import orjson as json
from confluent_kafka import Consumer
from prometheus_client import start_http_server, Gauge, Counter, Histogram

BROKERS = os.getenv("BROKERS", "localhost:9092")
TOPIC = os.getenv("TOPIC", "loadtest")
GROUP = os.getenv("GROUP", "loadtest-g")
METRICS_PORT = int(os.getenv("CONS_METRICS_PORT", "8001"))

cons_rate = Gauge("kafka_consumer_rate", "Msgs/sec (1s window)")
cons_msgs = Counter("kafka_consumer_messages_total", "Total messages consumed")
lag_gauge = Gauge("kafka_consumer_lag", "Sum lag across assigned partitions")
e2e_hist = Histogram(
    "kafka_end_to_end_latency_seconds",
    "End-to-end latency (produce -> consume)",
    buckets=(.001, .002, .005, .01, .02, .05, .1, .2, .5, 1, 2, 5, 10, 20)
)

c = Consumer({
    "bootstrap.servers": BROKERS,
    "group.id": GROUP,
    "auto.offset.reset": "earliest",
    "enable.auto.commit": True,
})

def get_lag():
    parts = c.assignment()
    if not parts:
        return 0
    end_offsets = c.end_offsets(parts) # dict
    lag = 0
    for tp in parts:
        pos = c.position([tp])[0]
        pos_off = pos.offset if pos and pos.offset >= 0 else 0
        end_off = end_offsets.get(tp, 0)
        lag += max(0, end_off - pos_off)
    return lag

if __name__ == "__main__":
    start_http_server(METRICS_PORT)
    print(f"[consumer] metrics at: {METRICS_PORT}/metrics")
    c.subscribe([TOPIC])

    count = 0
    window = 1.0
    errors = 0
    last = time.time()

    while True:
        msg = c.poll(0.1)
        now = time.time()

        if msg is None:
            pass
        elif msg.error():
            errors += 1
        else:
            cons_msgs.inc()
            count += 1
            try:
                t0 = json.loads(msg.value())["t0"]
                e2e_hist.observe(now - t0)
            except Exception as e:
                print(f"error: {e}")
                pass
        
        if now - last >= window:
            cons_rate.set(count / (now - last))
            try:
                lag_gauge.set(get_lag())
            except Exception:
                print("Assignment stabilizing...")
                pass

            count = 0
            last = now