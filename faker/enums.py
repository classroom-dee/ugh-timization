from enum import Enum
class FakeTypes(Enum):
    EVENT_TYPES = [
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
    EVENT_TYPES_PROB = [0.3, 0.2, 0.05, 0.05, 0.05, 0.05, 0.05, 0.15, 0.1]
    DEVICES = ["mobile_app", "mobile_web", "desktop", "tablet"]
    BROWSERS = ["Chrome", "Safari", "Firefox", "Edge", "Opera"]
    CHANNELS = ["direct", "seo", "sem", "email", "social", "affiliate"]
    SEX = ["male", "female"]
    FUNNEL_STAGES = [
        "landing",
        "view_category",
        "view_product",
        "add_to_cart",
        "begin_checkout",
        "add_shipping",
        "add_payment",
        "place_order",
    ]
    PAGES = ["/product", "/me", "/cart", "/landing", "/search_result"]
    