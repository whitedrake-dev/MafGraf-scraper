#!/usr/bin/env bash
set -euo pipefail

# CAPTURE_REPEATS: how many captures to perform *after* the first successful probe
# BASE_SLEEP: base delay between captures (seconds)
# JITTER_RANGE: jitter range in seconds; actual jitter is uniformly chosen from [-JITTER_RANGE, +JITTER_RANGE]

echo "Starting probe capture…"

if ! python capture_image.py; then
  echo "Probe capture failed — aborting workflow."
  exit 1
fi

echo "Probe succeeded — performing $CAPTURE_REPEATS additional captures."

for i in $(seq 1 "$CAPTURE_REPEATS")
do
  # Compute jitter in range [-JITTER_RANGE, +JITTER_RANGE]
  jitter=$(( (RANDOM % (2 * JITTER_RANGE + 1)) - JITTER_RANGE ))
  sleep_time=$(( BASE_SLEEP + jitter ))

  # Ensure sleep time is never negative
  if [ "$sleep_time" -lt 0 ]; then
    sleep_time=0
  fi

  echo "Iteration $i: sleeping for ${sleep_time}s (base=$BASE_SLEEP, jitter=$jitter)…"
  sleep "$sleep_time"

  python capture_image.py
done

echo "All captures completed."
exit 0
