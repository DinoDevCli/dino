#!/usr/bin/env bash
# Issue an Early Access Team Key and print a ready-to-send customer pack.
# Usage: ./scripts/issue-early-access.sh TEAM_NAME [DAYS]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEAM="${1:-}"
DAYS="${2:-60}"

if [[ -z "$TEAM" ]]; then
  echo "Usage: $0 TEAM_NAME [DAYS=60]" >&2
  exit 2
fi

if [[ -z "${DINO_EA_SIGNING_SECRET:-}" ]]; then
  echo "Warning: DINO_EA_SIGNING_SECRET unset — using sim secret (not for production)." >&2
fi

cd "$ROOT"
if ! command -v dino >/dev/null 2>&1; then
  export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
  DINO=(python3 -m dino.cli)
else
  DINO=(dino)
fi

OUT="$("${DINO[@]}" --json issue-key --team "$TEAM" --days "$DAYS")"
KEY="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["key"])' <<<"$OUT")"

echo "=== KEY ==="
echo "$KEY"
echo
echo "=== EMAIL (paste) ==="
echo
sed \
  -e "s/{TEAM}/$TEAM/g" \
  -e "s/{DAYS}/$DAYS/g" \
  -e "s/{NAME}/there/g" \
  -e "s|{KEY}|$KEY|g" \
  "$ROOT/docs/internal/customer_pack/EMAIL_TEMPLATE.md"
echo
echo "=== Attach also ==="
echo "docs/internal/customer_pack/QUICKSTART.md"
echo "Contact: dinodevcli@gmail.com"
