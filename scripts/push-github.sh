#!/usr/bin/env bash
# Create DinoDevCli/dino on GitHub and push main.
set -euo pipefail
cd "$(dirname "$0")/.."

if ! gh auth status >/dev/null 2>&1; then
  echo "Run first: gh auth login"
  exit 1
fi

REPO="DinoDevCli/dino"
URL="https://github.com/${REPO}.git"

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$URL"
else
  git remote add origin "$URL"
fi

if ! gh repo view "$REPO" >/dev/null 2>&1; then
  gh repo create "$REPO" \
    --public \
    --description "Dino — Deterministic Proof for Python Decision Pipelines" \
    --source=. \
    --remote=origin
fi

git push -u origin main
echo "Done: https://github.com/${REPO}"
