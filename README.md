# Dino

**Deterministic Proof for Python Decision Pipelines**

Proof CLI for Python decision logic — research pipelines, backtests, risk systems.
Seals execution, detects ML leakage, classifies drift, emits content-addressed [`proof.json`](docs/PROOF_CONTRACT.md).

Not a secret scanner. Not image provenance.

```bash
dino proof run --command "echo ok" --repo . --scan ./src --output-dir ./proof_out
dino proof verify --proof ./proof_out/proof.json
```

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
dino upgrade --pack proof
dino proof doctor
```

Requires Python ≥ 3.10.

---

## CLI

```bash
dino proof run \
  --command "echo ok" \
  --repo . \
  --scan ./src \
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
| **Free** | €0 | `scan` |
| **Indie** | €49 once | Proof pack |
| **Team** | 20% off (5–10 seats) | Proof pack |

Unlock: `dino upgrade --pack proof`

---

## Docs

| Doc | Role |
|-----|------|
| [`PROOF_CONTRACT.md`](docs/PROOF_CONTRACT.md) | Normative guarantees |
| [`CLI_E2E_REFERENCE.md`](docs/CLI_E2E_REFERENCE.md) | CLI + live outputs |
| [`EXAMPLES.md`](docs/EXAMPLES.md) | Short examples |
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
