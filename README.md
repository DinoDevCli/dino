# Dino

[![CI](https://github.com/DinoDevCli/dino/actions/workflows/ci.yml/badge.svg)](https://github.com/DinoDevCli/dino/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)

**Deterministic Proof for Python Decision Pipelines**

Proof CLI for Python decision logic — research pipelines, backtests, risk systems.
Seals execution, detects ML leakage, classifies drift, emits content-addressed [`proof.json`](docs/PROOF_CONTRACT.md).

**Scope (intentional):** sealed runs + replay + `proof_hash` for decision pipelines.
Not a general SAST/DAST suite, secret scanner, SBOM tool, or container/image provenance product.

```bash
dino proof run --command echo ok --repo . --scan ./path/to/pipeline.py --output-dir ./proof_out
dino proof verify --proof ./proof_out/proof.json
```

`--command` takes argv tokens (`echo ok`). A single quoted string (`"echo ok"`) is also accepted — required when the program itself takes `--flags` (e.g. `--command "python3 train.py --seed 0"`).
`--scan` must resolve to at least one `.py` file or the scan fails.

---

## Install

Free pack (`scan`):

```bash
pip install "git+https://github.com/DinoDevCli/dino.git"
dino scan leakage ./my_pipeline.py
```

Proof pack (`capsule`, `map`, `bundle`, `flight`, `verify`, `proof`):

```bash
pip install "git+https://github.com/DinoDevCli/dino.git"
# After Lemon Squeezy purchase (license key in receipt email):
dino upgrade --pack proof --key YOUR_LICENSE_KEY
dino proof doctor
```

Requires Python ≥ 3.10.

---

## CLI

```bash
dino proof run \
  --command echo ok \
  --repo . \
  --scan ./path/to/pipeline.py \
  --output-dir ./proof_out

dino proof verify --proof ./proof_out/proof.json

dino scan leakage my_pipeline.py
```

Full reference: [`docs/CLI_E2E_REFERENCE.md`](docs/CLI_E2E_REFERENCE.md)

---

## Modules

| Module | Pack | Role |
|--------|------|------|
| **Scan** | Free | 7 ML leakage rules + grammar |
| **Capsule** | Proof | Sealed subprocess + replay |
| **Map** | Proof | AST graph, drift, plan |
| **Bundle** | Proof | Regression (`true_delta`, `endpoint_ratio`) |
| **Flight** | Proof | Canary summary |
| **Verify** | Proof | Drift, supersession, attest, binary |
| **Proof** | Proof | `proof.json` · `PROOF_PASSED` / `PROOF_VERIFY_PASSED` |

---

## Proof contract

When status is `passed` / `partial` and verify succeeds, Dino guarantees:

- deterministic execution and replay
- content-addressed artifacts (`proof_hash`)
- research leakage rules
- drift classification
- regression and governance signals

Schemas and limits: [`docs/PROOF_CONTRACT.md`](docs/PROOF_CONTRACT.md)

---

## Pricing

| Pack | Price | Includes |
|------|-------|----------|
| **Free** | €0 | Leakage Scan |
| **Indie** | €49 one-time | Full Proof Pack |
| **Team** | €39 per seat (20% off) | Full Proof Pack |
| **Large Teams** | Custom | 20+ seats, invoicing on request |

**Rules**

- Team pricing starts at **3 seats**
- Team pricing applies up to **20 seats**
- Above 20 seats → contact us
- No Enterprise tier, no subscriptions, no lock-in
- Checkout via **Lemon Squeezy**; unlock with license key (see [`docs/LEMON_SQUEEZY.md`](docs/LEMON_SQUEEZY.md))

Unlock:

```bash
dino upgrade --pack proof --key YOUR_LICENSE_KEY
```

> Not on PyPI under `dino` (name collision). Install only via the GitHub URL above.

Contact: [noahpeitz95@gmail.com](mailto:noahpeitz95@gmail.com)

---

## Docs

| Doc | Role |
|-----|------|
| [`PROOF_CONTRACT.md`](docs/PROOF_CONTRACT.md) | Normative guarantees |
| [`CLI_E2E_REFERENCE.md`](docs/CLI_E2E_REFERENCE.md) | CLI + live outputs |
| [`EXAMPLES.md`](docs/EXAMPLES.md) | Short examples |
| [`LEMON_SQUEEZY.md`](docs/LEMON_SQUEEZY.md) | Checkout + license keys |
| [`TECH_STATUS_NOW.md`](docs/TECH_STATUS_NOW.md) | Technical status |
| [`website/`](website/) | Landing page |

---

## Development

```bash
git clone https://github.com/DinoDevCli/dino.git
cd dino
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/dino -q
```

Website:

```bash
cd website
cp .env.example .env.local
npm install && npm run dev
```

---

## License

MIT · [DinoDevCli](https://github.com/DinoDevCli)
