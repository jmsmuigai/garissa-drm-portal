#!/usr/bin/env bash
set -e
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$ROOT_DIR/OUTPUT"

echo "Running setup (installing Python deps)..."
bash "$ROOT_DIR/setup.sh"

# Activate venv for the scan
source "$ROOT_DIR/.venv/bin/activate"

echo "Scanning workspace for GIS layers..."
python3 "$ROOT_DIR/scan_layers.py" -i "$ROOT_DIR" -o "$ROOT_DIR/OUTPUT/scan_layers.csv"

echo "Scan complete: OUTPUT/scan_layers.csv"
