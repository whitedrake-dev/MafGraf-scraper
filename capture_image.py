#!/usr/bin/env python3
import os
import sys
import requests
from requests.adapters import HTTPAdapter, Retry
from datetime import datetime
from zoneinfo import ZoneInfo

# -----------------------------
# Read configuration from environment
# -----------------------------
IMAGE_URL = os.getenv("IMAGE_URL", "https://mafie.podsveti.cz/graf/")
CAPTURE_DIR = os.getenv("CAPTURE_DIR", "captures")
CAPTURE_TIMEZONE = os.getenv("CAPTURE_TIMEZONE", "Europe/Prague")

retry_total = int(os.getenv("RETRY_TOTAL", 5))
retry_timeout = int(os.getenv("RETRY_TIMEOUT", 20))
retry_backoff = float(os.getenv("RETRY_BACKOFF", 1.0))

# -----------------------------
# Ensure output directory exists
# -----------------------------
os.makedirs(CAPTURE_DIR, exist_ok=True)

# -----------------------------
# HTTP headers (kept in code)
# -----------------------------
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Language": "cs-CZ,cs;q=0.9,en;q=0.8",
    "Referer": "https://mafie.podsveti.cz/",
    "Connection": "keep-alive",
}

# -----------------------------
# Capture logic
# -----------------------------
def attempt_capture():
    session = requests.Session()

    retries = Retry(
        total=retry_total,
        backoff_factor=retry_backoff,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )

    session.mount("https://", HTTPAdapter(max_retries=retries))

    try:
        response = session.get(IMAGE_URL, headers=headers, timeout=retry_timeout)
        response.raise_for_status()

        now = datetime.now(ZoneInfo(CAPTURE_TIMEZONE))
        timestamp = now.strftime("%Y%m%d-%H%M%S")
        filename = f"{CAPTURE_DIR}/{timestamp}.png"

        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"Saved {filename}")
        return True

    except Exception as e:
        print("Download failed:", e)
        return False


if __name__ == "__main__":
    sys.exit(0 if attempt_capture() else 1)
