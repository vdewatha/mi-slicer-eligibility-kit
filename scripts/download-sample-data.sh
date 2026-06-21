#!/usr/bin/env bash
# Download MSD Task09 Spleen subset or create synthetic fallback.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATA="$ROOT/data"
RAW="$DATA/raw/Task09_Spleen"

mkdir -p "$RAW/imagesTr" "$RAW/labelsTr"

if [[ -f "$RAW/imagesTr/spleen_2.nii.gz" ]]; then
  echo "MSD Task09 data already present."
  exit 0
fi

echo "Attempting MSD Task09 download (requires network)..."
ARCHIVE_URL="https://msd-for-monai.s3-us-west-2.amazonaws.com/Task09_Spleen.tar"
TMP="$(mktemp -d)"

if curl -fsSL "$ARCHIVE_URL" -o "$TMP/Task09_Spleen.tar" 2>/dev/null; then
  tar -xf "$TMP/Task09_Spleen.tar" -C "$TMP"
  # Copy first 3 training cases only (smaller subset for portfolio)
  for i in 2 10 31; do
    if [[ -f "$TMP/Task09_Spleen/imagesTr/spleen_${i}.nii.gz" ]]; then
      cp "$TMP/Task09_Spleen/imagesTr/spleen_${i}.nii.gz" "$RAW/imagesTr/"
      cp "$TMP/Task09_Spleen/labelsTr/spleen_${i}.nii.gz" "$RAW/labelsTr/"
    fi
  done
  rm -rf "$TMP"
  echo "Downloaded MSD Task09 subset ($(ls "$RAW/imagesTr" | wc -l | tr -d ' ') cases)."
else
  echo "Download failed — generating synthetic case for offline demo."
  python3 -m venv "$ROOT/.venv" 2>/dev/null || true
  if [[ ! -d "$ROOT/.venv" ]]; then
  python3 -m medasset.synthetic --output-dir "$DATA" 2>/dev/null || \
    PYTHONPATH="$ROOT/pipeline" python3 "$ROOT/pipeline/medasset/synthetic.py" --output-dir "$DATA"
  else
    "$ROOT/.venv/bin/pip" install -q -e "$ROOT/pipeline" 2>/dev/null || true
    "$ROOT/.venv/bin/python" -m medasset.synthetic --output-dir "$DATA"
  fi
fi
