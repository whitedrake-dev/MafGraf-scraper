import requests
from requests.adapters import HTTPAdapter, Retry
from datetime import datetime
import hashlib
import os
from zoneinfo import ZoneInfo  # Python 3.9+

IMAGE_URL = "https://mafie.podsveti.cz/graf/"

# Ensure directories exist
os.makedirs("captures", exist_ok=True)

# Timestamp in Prague timezone
now = datetime.now(ZoneInfo("Europe/Prague"))
timestamp = now.strftime("%Y%m%d-%H%M%S")

# Download image
session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET"]
)
session.mount("https://", HTTPAdapter(max_retries=retries))

try:
    response = session.get(IMAGE_URL, timeout=60)
    response.raise_for_status()
    content = response.content
except Exception as e:
    print("Download failed:", e)
    content = b""  # empty content so hash still logs

# Compute SHA-256 hash
sha256 = hashlib.sha256(content).hexdigest()

# Save PNG
png_filename = f"captures/{timestamp}.png"
with open(png_filename, "wb") as f:
    f.write(content)

# Append to hash log
log_line = f"{timestamp}  {sha256}\n"
log_filename = "captures/hashes.txt"
with open(log_filename, "a", encoding="utf-8") as log:
    log.write(log_line)

print(f"Saved {png_filename}")
print(f"Logged hash: {sha256}")
