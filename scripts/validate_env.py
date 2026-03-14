#!/usr/bin/env python3
import os
import sys
from zoneinfo import ZoneInfo

def fail(msg):
    print(f"Configuration error: {msg}")
    sys.exit(2)

def require_env(name):
    val = os.getenv(name)
    if val is None or val == "":
        fail(f"{name} is not set or empty")
    return val

def require_int(name, min_value=None):
    val = require_env(name)
    try:
        num = int(val)
    except ValueError:
        fail(f"{name} must be an integer, got {val!r}")
    if min_value is not None and num < min_value:
        fail(f"{name} must be >= {min_value}, got {num}")
    return num

def main():
    # -----------------------------
    # Core capture settings
    # -----------------------------
    image_url = require_env("IMAGE_URL")
    if not image_url.startswith(("http://", "https://")):
        fail(f"IMAGE_URL must start with http:// or https://, got {image_url!r}")

    capture_dir = require_env("CAPTURE_DIR")

    timezone = require_env("CAPTURE_TIMEZONE")
    try:
        ZoneInfo(timezone)
    except Exception:
        fail(f"Invalid CAPTURE_TIMEZONE: {timezone!r}")

    # -----------------------------
    # Retry settings (Python)
    # -----------------------------
    require_int("RETRY_TOTAL", min_value=0)
    require_int("RETRY_TIMEOUT", min_value=1)
    require_int("RETRY_BACKOFF", min_value=0)

    # -----------------------------
    # Loop settings (shell)
    # -----------------------------
    require_int("CAPTURE_REPEATS", min_value=0)
    require_int("BASE_SLEEP", min_value=0)
    require_int("JITTER_RANGE", min_value=0)

    print("Environment validation passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
