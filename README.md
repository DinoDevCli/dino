# Dino

**Deterministic Proof for Python Decision Pipelines**

Dino ist ein Proof-CLI für Python-Entscheidungslogik — Research-Pipelines, Backtests und Risk-Systeme. Es versiegelt Ausführung, erkennt ML-Leakage, klassifiziert Drift und erzeugt ein auditierbares [`proof.json`](docs/PROOF_CONTRACT.md).

Dino ist kein Secret-Scanner und kein Image-Provenance-Tool.

```bash
dino proof run --command "echo ok" --repo . --scan ./src --output-dir ./proof_out
dino proof verify --proof ./proof_out/proof.json
```

---

## Installation

**Free Pack** (Leakage-Scan):

```bash
pip install "git+https://github.com/ArdentCrab/devsecops.git"
dino scan leakage ./my_pipeline.py
```

**Proof Pack** (Capsule, Map, Bundle, Flight, Verify, Proof):

```bash
pip install "git+https://github.com/ArdentCrab/devsecops.git"
dino upgrade --pack proof
dino proof doctor
```

Voraussetzung: Python ≥ 3.10

---

## CLI

```bash
# Proof-Kette
dino proof run \
  --command "echo ok" \
  --repo . \
  --scan ./src \
  --output-dir ./proof_out

dino proof verify --proof ./proof_out/proof.json

# Leakage (Free)
dino scan leakage my_pipeline.py
```

Vollständige Referenz: [`docs/CLI_E2E_REFERENCE.md`](docs/CLI_E2E_REFERENCE.md)

---

## Module

| Modul | Pack | Rolle |
|-------|------|--------|
| **Scan** | Free | 7 ML-Leakage-Regeln + Grammar |
| **Capsule** | Proof | Deterministische Ausführung + Replay |
| **Map** | Proof | AST-Graph, Drift, Plan |
| **Bundle** | Proof | Regression (`true_delta`, `endpoint_ratio`) |
| **Flight** | Proof | Canary-Summary |
| **Verify** | Proof | Drift, Supersession, Attest, Binary |
| **Proof** | Proof | `proof.json` · `PROOF_PASSED` / `PROOF_VERIFY_PASSED` |

---

## Proof-Contract

Wenn ein Proof `passed` / `partial` ist und Verify gelingt, garantiert Dino:

- deterministische Ausführung und Wiederholung
- content-addressed Artefakte (`proof_hash`)
- Leakage-Regeln für Research-Code
- Drift-Klassifikation
- Regression- und Governance-Signale

Grenzen und Schemas: [`docs/PROOF_CONTRACT.md`](docs/PROOF_CONTRACT.md)

---

## Pricing

| Pack | Preis | Inhalt |
|------|-------|--------|
| **Free** | 0 € | `scan` |
| **Indie** | 49 € einmalig | Proof Pack |
| **Team** | 20 % Rabatt (5–10 Sitze) | Proof Pack |

Unlock: `dino upgrade --pack proof`

---

## Dokumentation

| Doc | Inhalt |
|-----|--------|
| [`PROOF_CONTRACT.md`](docs/PROOF_CONTRACT.md) | Normative Garantien |
| [`CLI_E2E_REFERENCE.md`](docs/CLI_E2E_REFERENCE.md) | CLI + Live-Outputs |
| [`EXAMPLES.md`](docs/EXAMPLES.md) | Kurzbeispiele |
| [`TECH_STATUS_NOW.md`](docs/TECH_STATUS_NOW.md) | Technischer Stand |
| [`website/`](website/) | Landing Page |

---

## Entwicklung

```bash
git clone https://github.com/ArdentCrab/devsecops.git
cd dino
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/dino -q
```

Website lokal:

```bash
cd website
cp .env.example .env.local
npm install && npm run dev
```

---

## Lizenz

MIT · [ArdentCrab](https://github.com/ArdentCrab)
