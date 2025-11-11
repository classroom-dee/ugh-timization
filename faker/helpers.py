from faker import Faker
import numpy as np
import uuid
import orjson as json
from datetime import datetime, timezone
from enums import FakeTypes

fake = Faker()

COUNTRIES = [fake.country_code() for _ in range(50)]

def generate_row():
    e = {
            "event_id": uuid.uuid4().hex,
            "event_time": datetime.now(timezone.utc).isoformat(),
            "user_id": f"{fake.user_name()}_{fake.random_int(10, 9999)}",
            "is_logged_in": np.random.choice([0, 1]),
            "event_type": np.random.choice(
                FakeTypes.EVENT_TYPES.value, p=FakeTypes.EVENT_TYPES_PROB.value
            ),
            "funnel_stage": np.random.choice(FakeTypes.FUNNEL_STAGES.value),
            "session_id": uuid.uuid4().hex,
            "sex": np.random.choice(FakeTypes.SEX.value),
            "channel": np.random.choice(FakeTypes.CHANNELS.value),
            "ab_variant": np.random.choice(["A", "B"]),
            "device": np.random.choice(FakeTypes.DEVICES.value),
            "browser": np.random.choice(FakeTypes.BROWSERS.value),
            "geo_country": np.random.choice(COUNTRIES),
            "ip_address": fake.ipv4_public(),
            "url": fake.url(),
            "page": np.random.choice(FakeTypes.PAGES.value),
            "referrer": fake.url(),
            "amount": None,
            # "amount": np.where(
            #     np.random.rand(num_rows) < 0.1,
            #     np.round(np.random.uniform(10, 500, num_rows), 2),
            #     np.nan,
            # ),
            "product_id": None,
        }
    if e["event_type"] not in ["login", "logout"]:
        e["product_id"] = np.random.randint(1, 10000)
        e["amount"] = np.random.randint(500, 10000000)

    return e

if __name__ == "__main__":
    # For testing
    for _ in range(5):
        print("----byte length for this row:----")
        print(len(json.dumps(generate_row(), default=lambda o: int(o) if isinstance(o, np.integer) else o)))