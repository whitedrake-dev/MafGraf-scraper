import requests
from requests.adapters import HTTPAdapter, Retry
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import os

IMAGE_URL = "https://mafie.podsveti.cz/graf/"

os.makedirs("captures", exist_ok=True)

now = datetime.now(ZoneInfo("Europe/Prague"))
timestamp = now.strftime("%Y%m%d-%H%M%S")

# Browser-like headers
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

session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET"]
)
session.mount("https://", HTTPAdapter(max_retries=retries))

content = None
hash_value = None

try:
    response = session.get(IMAGE_URL, headers=headers, timeout=60)
    response.raise_for_status()
    content = response.content
    hash_value = hashlib.sha256(content).hexdigest()
except Exception as e:
    print("Download failed:", e)
    content = b""
    hash_value = "FAILED"

png_filename = f"captures/{timestamp}.png"
with open(png_filename, "wb") as f:
    f.write(content)

log_filename = "captures/hashes.txt"
with open(log_filename, "a", encoding="utf-8") as log:
    log.write(f"{timestamp}  {hash_value}\n")

print(f"Saved {png_filename}")
print(f"Logged hash: {hash_value}")
