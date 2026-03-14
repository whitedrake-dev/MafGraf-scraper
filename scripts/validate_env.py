import os
import sys
from zoneinfo import ZoneInfo

def fail(msg):
    print(f"Configuration error: {msg}")
    sys.exit(2)

def require_int(name, min_value=None):
    val = os.getenv(name)
    if val is None:
        fail(f"{name} is not set")
    try:
        num = int(val)
    except ValueError:
        fail(f"{name} must be an integer, got {val!r}")
    if min_value is not None and num < min_value:
        fail(f"{name} must be >= {min_value}, got {num}")
    return num

def main():
    # Core capture settings
    image_url = os.getenv("IMAGE_URL")
    if not image_url or not image_url.startswith(("http://", "https://")):
        fail(f"Invalid IMAGE_URL: {image_url!r}")

    capture_dir = os.getenv("CAPTURE_DIR")
    if not capture_dir:
        fail("CAPTURE_DIR is empty")

    # Timezone
    tz = os.getenv("CAPTURE_TIMEZONE")
    try:
        ZoneInfo(tz)
    except Exception:
        fail(f"Invalid CAPTURE_TIMEZONE: {tz!r}")

    # Retry settings
    require_int("RETRY_TOTAL", min_value=0)
    require_int("RETRY_TIMEOUT", min_value=1)
    require_int("RETRY_BACKOFF", min_value=0)

    # Loop settings (shell)
    require_int("CAPTURE_REPEATS", min_value=0)
    require_int("BASE_SLEEP", min_value=0)
    require_int("JITTER_RANGE", min_value=0)

    print("Environment validation passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
