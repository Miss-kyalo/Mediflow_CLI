from __future__ import annotations
import os
import re
from datetime import datetime

def clear_screen() -> None:
    """Clear the terminal screen based on the operating system."""
    os.system("cls" if os.name == "nt" else "clear")


def validate_phone(phone: str) -> bool:
    """
    Validate standard phone number format (e.g., 0712345678, +254712345678, or 10-15 digits).
    """
    pattern = r"^\+?[0-9]{10,15}$"
    return bool(re.match(pattern, phone.strip()))


def validate_age(age_str: str) -> bool:
    """Verify age is a positive integer within a realistic human range."""
    if not age_str.isdigit():
        return False
    age = int(age_str)
    return 0 < age <= 120


def format_timestamp(dt: datetime | None = None) -> str:
    """Return a clean human-readable date and time string."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def sanitize_input(text: str) -> str:
    """Remove trailing whitespace and potential control characters."""
    return text.strip()