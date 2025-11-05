from faker import Faker
import pandas as pd
import numpy as np
import uuid
from datetime import datetime, timezone

async def generate():
    ...

fake = Faker()
num_rows = 10

event_types = [
    "page_view",
    "click",
    "login",
    "logout",
    "purchase",
    "add_to_cart",
    "checkout",
    "discard_from_cart",
    "cancel_purchase",
]
devices = ["mobile_app", "mobile_web", "desktop", "tablet"]
browsers = ["Chrome", "Safari", "Firefox", "Edge", "Opera"]
channels = ["direct", "seo", "sem", "email", "social", "affiliate"]
sex = ["male", "female"]
funnel_stages = [
    "landing",
    "view_category",
    "view_product",
    "add_to_cart",
    "begin_checkout",
    "add_shipping",
    "add_payment",
    "place_order",
]
pages = ["/product", "/me", "/cart", "/landing", "/search_result"]
countries = [fake.country_code() for _ in range(50)]

data = []

for _ in range(num_rows):
    e = {
        "event_id": uuid.uuid4().hex,
        "event_time": datetime.now(timezone.utc).isoformat(),
        "user_id": f"{fake.user_name()}_{fake.random_int(10, 9999)}",
        "is_logged_in": np.random.choice([True, False]),
        "event_type": np.random.choice(
            event_types, p=[0.3, 0.2, 0.05, 0.05, 0.05, 0.05, 0.05, 0.15, 0.1]
        ),
        "funnel_stage": np.random.choice(funnel_stages),
        "session_id": uuid.uuid4().hex,
        "sex": np.random.choice(sex),
        "channel": np.random.choice(channels),
        "ab_variant": np.random.choice(["A", "B"]),
        "device": np.random.choice(devices),
        "browser": np.random.choice(browsers),
        "geo_country": np.random.choice(countries),
        "ip_address": fake.ipv4_public(),
        "url": fake.url(),
        "page": np.random.choice(pages),
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

    data.append(e)

df = pd.DataFrame(data)

print(df[["event_type", "amount", "product_id"]].head(50))
