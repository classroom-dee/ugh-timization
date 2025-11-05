from confluent_kafka import Consumer, OFFSET_BEGINNING

c = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "demo-group",
    "auto.offset.reset": "earliest"
})
c.subscribe(["demo"])

try:
    while True:
        msg = c.poll(1.0)
        if msg is None: 
            continue
        if msg.error():
            print("Error:", msg.error())
        else:
            print(f"{msg.topic()}[{msg.partition()}]@{msg.offset()}: {msg.value().decode()}")
except KeyboardInterrupt:
    pass
finally:
    c.close()
