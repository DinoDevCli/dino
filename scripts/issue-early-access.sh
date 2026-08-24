#!/usr/bin/env bash
# Issue an Early Access Team Key and write a customer-pack.v1 ZIP.
# Usage: ./scripts/issue-early-access.sh TEAM_NAME [DAYS] [--name NAME] [--out DIR] [--allow-sim]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEAM_RAW=""
DAYS="60"
NAME="there"
OUT="$ROOT/dist/customer-packs"
ALLOW_SIM=0
POSITIONAL=()

usage() {
  cat <<EOF
Usage: $0 TEAM_NAME [DAYS=60] [--name NAME] [--out DIR] [--allow-sim]

Writes:
  dist/customer-packs/dino-ea-<team>-v<version>-<stamp>.zip
  (inner folder: <team>/KEY.txt QUICKSTART.md EMAIL.txt LICENSE VERSION examples/)

Send EMAIL.txt, attach the ZIP, from dinodevcli@gmail.com.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --name)
      NAME="${2:-}"
      shift 2
      ;;
    --name=*)
      NAME="${1#--name=}"
      shift
      ;;
    --out)
      OUT="${2:-}"
      shift 2
      ;;
    --out=*)
      OUT="${1#--out=}"
      shift
      ;;
    --days)
      DAYS="${2:-}"
      shift 2
      ;;
    --days=*)
      DAYS="${1#--days=}"
      shift
      ;;
    --allow-sim)
      ALLOW_SIM=1
      shift
      ;;
    --)
      shift
      POSITIONAL+=("$@")
      break
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;
  esac
done

if [[ ${#POSITIONAL[@]} -ge 1 ]]; then
  TEAM_RAW="${POSITIONAL[0]}"
fi
if [[ ${#POSITIONAL[@]} -ge 2 ]]; then
  DAYS="${POSITIONAL[1]}"
fi
if [[ ${#POSITIONAL[@]} -ge 3 ]]; then
  NAME="${POSITIONAL[2]}"
fi

if [[ -z "$TEAM_RAW" ]]; then
  usage >&2
  exit 2
fi

if ! [[ "$DAYS" =~ ^[0-9]+$ ]]; then
  echo "DAYS must be an integer (got: $DAYS)" >&2
  exit 2
fi

if [[ -z "${DINO_EA_SIGNING_SECRET:-}" ]]; then
  if [[ "$ALLOW_SIM" -eq 0 ]]; then
    echo "Refusing to issue: DINO_EA_SIGNING_SECRET is unset." >&2
    echo "Export the production secret, or pass --allow-sim for a local test pack." >&2
    exit 2
  fi
  echo "Warning: DINO_EA_SIGNING_SECRET unset — sim secret (do not send to customers)." >&2
fi

SLUG="$(printf '%s' "$TEAM_RAW" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//; s/-+/-/g')"
if [[ -z "$SLUG" ]]; then
  echo "TEAM_NAME produced an empty slug" >&2
  exit 2
fi

cd "$ROOT"
if ! command -v dino >/dev/null 2>&1; then
  export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
  DINO=(python3 -m dino.cli)
else
  DINO=(dino)
fi

OUT_JSON="$("${DINO[@]}" --json issue-key --team "$SLUG" --days "$DAYS")"
KEY="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["key"])' <<<"$OUT_JSON")"

PACK_OUT="$(
  python3 "$ROOT/scripts/pack_customer_zip.py" \
    --root "$ROOT" \
    --team "$SLUG" \
    --days "$DAYS" \
    --name "$NAME" \
    --key "$KEY" \
    --out "$OUT"
)"
ZIP_PATH="$(printf '%s\n' "$PACK_OUT" | sed -n '1p')"
EMAIL_PATH="$(printf '%s\n' "$PACK_OUT" | sed -n '2p')"

echo "=== SEND ==="
echo "From:    dinodevcli@gmail.com"
echo "Subject: Dino Early Access — Proof Pack Team Key ($SLUG)"
echo "Attach:  $ZIP_PATH"
echo "Body:    $EMAIL_PATH"
echo
echo "=== EMAIL ==="
echo
cat "$EMAIL_PATH"
echo
echo "=== LEDGER ==="
PREFIX="$(python3 -c 'import sys; k=sys.argv[1]; print(k[:24])' "$KEY")"
echo "team=$SLUG days=$DAYS prefix=$PREFIX zip=$(basename "$ZIP_PATH")"
