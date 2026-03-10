import requests
from datetime import datetime
import hashlib
import os
from zoneinfo import ZoneInfo  # Python 3.9+

IMAGE_URL = "<some_URL>"  # replace with actual PNG URL

# Ensure directories exist
os.makedirs("captures", exist_ok=True)

# Timestamp in Prague timezone
now = datetime.now(ZoneInfo("Europe/Prague"))
timestamp = now.strftime("%Y%m%d-%H%M%S")

# Download image
response = requests.get(IMAGE_URL, timeout=20)
response.raise_for_status()
content = response.content

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
