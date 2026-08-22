# Dino CLI

**Deterministic Proof & Governance Platform** — seals *logic & data integrity*, not images or secrets.

| Doc | Role |
|-----|------|
| [`docs/PROOF_CONTRACT.md`](docs/PROOF_CONTRACT.md) | What we guarantee |
| [`docs/TECH_STATUS_NOW.md`](docs/TECH_STATUS_NOW.md) | Technical status |
| [`docs/CLI_E2E_REFERENCE.md`](docs/CLI_E2E_REFERENCE.md) | CLI + live E2E outputs |
| [`docs/ICP_TEST.md`](docs/ICP_TEST.md) | **Official ICP / pricing market test** |
| [`website/`](website/) | Marketing landing page (Vercel-ready) |

## Primary ICPs (under test)

1. **Quant Research** (banks / funds) — lookahead, non-repro backtests  
2. **Fraud / Scoring FinTech** — audit-ready decision evidence  

## Unique product

`dino proof run` → sealed execution + leakage scan + structural map → content-addressed `proof.json`.

## Installation

From GitHub (Free Pack — `scan`):

```bash
pip install "git+https://github.com/noahp/dino.git"
dino scan leakage ./my_pipeline.py
```

Proof Pack (all domains):

```bash
pip install "git+https://github.com/noahp/dino.git[dev]"
dino upgrade --pack proof
dino proof doctor
dino proof run --command "echo ok" --repo . --scan ./src --output-dir ./proof_out
dino proof verify --proof ./proof_out/proof.json
```

Local development:

```bash
git clone https://github.com/noahp/dino.git
cd dino
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/dino -q
```

## Website

```bash
cd website
cp .env.example .env.local   # set NEXT_PUBLIC_GITHUB_OWNER/REPO
npm install && npm run dev
```

Deploy on Vercel with root directory `website`.

## Packs

| Tier | Price | Domains |
|------|-------|---------|
| Free | €0 | `scan` |
| Indie | €49 once | proof pack |
| Team | 20% off (5–10 seats) | proof pack |

## Tests

```bash
pytest tests/dino -q
```
