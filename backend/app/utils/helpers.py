"""
Helper utilities — slugify, order number generation, etc.
"""

import random
import string
from datetime import datetime, timezone

from slugify import slugify as _slugify


def generate_slug(text: str) -> str:
    """Generate a URL-safe slug from text"""
    return _slugify(text, lowercase=True, max_length=100)


def generate_order_number() -> str:
    """Generate a unique order number: PFS + date + random"""
    now = datetime.now(timezone.utc)
    date_part = now.strftime("%Y%m%d")
    random_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"PFS{date_part}{random_part}"


def generate_random_code(length: int = 8) -> str:
    """Generate a random alphanumeric code"""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def format_price(amount: float, currency: str = "TWD") -> str:
    """Format price for display"""
    if currency == "TWD":
        return f"NT${amount:,.0f}"
    return f"${amount:,.2f}"
