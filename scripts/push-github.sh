#!/usr/bin/env bash
# Create ArdentCrab/devsecops on GitHub and push main.
set -euo pipefail
cd "$(dirname "$0")/.."

if ! gh auth status >/dev/null 2>&1; then
  echo "Run first: gh auth login"
  exit 1
fi

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin git@github.com:ArdentCrab/devsecops.git
else
  git remote add origin git@github.com:ArdentCrab/devsecops.git
fi

if ! gh repo view ArdentCrab/devsecops >/dev/null 2>&1; then
  gh repo create ArdentCrab/devsecops \
    --public \
    --description "Dino — Deterministic Proof for Python Decision Pipelines" \
    --source=. \
    --remote=origin
fi

# Prefer HTTPS with gh credentials if SSH key is a different account
if ! git ls-remote git@github.com:ArdentCrab/devsecops.git >/dev/null 2>&1; then
  git remote set-url origin https://github.com/ArdentCrab/devsecops.git
fi

git push -u origin main
echo "Done: https://github.com/ArdentCrab/devsecops"
