import os
import sys
import requests
from requests.adapters import HTTPAdapter, Retry
from datetime import datetime
from zoneinfo import ZoneInfo

IMAGE_URL = "https://mafie.podsveti.cz/graf/"

# Read configuration from environment variables
retry_total = int(os.getenv("RETRY_TOTAL", 5))
retry_timeout = int(os.getenv("RETRY_TIMEOUT", 20))
retry_backoff = float(os.getenv("RETRY_BACKOFF", 1.0))

# Ensure output directory exists
os.makedirs("captures", exist_ok=True)

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

        now = datetime.now(ZoneInfo("Europe/Prague"))
        timestamp = now.strftime("%Y%m%d-%H%M%S")
        filename = f"captures/{timestamp}.png"

        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"Saved {filename}")
        return True

    except Exception as e:
        print("Download failed:", e)
        return False


if __name__ == "__main__":
    sys.exit(0 if attempt_capture() else 1)
