#!/usr/bin/env bash
# Create DinoDevCli/dino on GitHub and push main.
set -euo pipefail
cd "$(dirname "$0")/.."

if ! gh auth status >/dev/null 2>&1; then
  echo "Run first: gh auth login"
  exit 1
fi

if git remote get-url origin >/dev/null 2>&1; then
  echo "Remote origin already set:"
  git remote -v
else
  gh repo create DinoDevCli/dino \
    --public \
    --description "Deterministic Proof & Governance CLI for Python decision pipelines" \
    --source=. \
    --remote=origin
fi

git push -u origin main
echo "Done: https://github.com/DinoDevCli/dino"
