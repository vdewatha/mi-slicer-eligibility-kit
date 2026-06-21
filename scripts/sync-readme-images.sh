#!/usr/bin/env bash
# Copy portfolio figure assets into docs/images for GitHub README rendering.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/docs/images"
cp "$ROOT/portfolio/assets/"*.png "$ROOT/docs/images/" 2>/dev/null || true
echo "Synced PNG assets to docs/images/"
