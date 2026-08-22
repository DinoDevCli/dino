#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 -m pip install -e ".[dev]" -q
pyinstaller --onefile --name dino \
  --paths "$ROOT" \
  --hidden-import=dino.cli \
  --collect-submodules=dino \
  "$ROOT/dino/cli.py"

echo "Binary: $ROOT/dist/dino"
