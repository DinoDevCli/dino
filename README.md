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
| **Free** | €0 | Leakage Scan |
| **Indie** | €49 one-time | Full Proof Pack |
| **Team** | €39 per seat (20% off) | Full Proof Pack |
| **Large Teams** | Custom | 20+ seats, invoicing on request |

**Rules**

- Team pricing starts at **3 seats**
- Team pricing applies up to **20 seats**
- Above 20 seats → contact us
- No Enterprise tier, no subscriptions, no lock-in

Unlock:

```bash
dino upgrade --pack proof
```

Contact: [noahpeitz95@gmail.com](mailto:noahpeitz95@gmail.com)

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
