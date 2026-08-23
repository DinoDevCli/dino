# Dino — Local-First Audit Engine (Early Access)

[![CI](https://github.com/DinoDevCli/dino/actions/workflows/ci.yml/badge.svg)](https://github.com/DinoDevCli/dino/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)
[![Local-First](https://img.shields.io/badge/Local--First-audit%20engine-0a0a0a)](docs/PROOF_INDEX.md)

Dino is currently in **Early Access**.  
We're onboarding 5–10 teams (risk, fraud, ML governance, research) to test the engine,
integrate the export/index artifacts into their dashboards, and provide feedback.

During Early Access:

- Dino is fully functional (proof engine, export contracts, proof index)
- Team Keys are **free**
- No checkout, no SaaS, no dashboard
- We collect feedback + integration examples

**Deterministic proofs · export contracts · universal proof index — for your dashboards.**

> Dino is a local-first audit engine that produces sealed proofs, export envelopes, and a universal proof index for your dashboards.  
> Dino outputs audit artifacts — dashboards render them. No hosted UI. No SaaS. No cloud product.

```bash
dino proof run \
  --command echo ok \
  --scan ./tests/e2e/pipe.py \
  --output-dir ./proof_out \
  --pipeline fraud_score_v4 \
  --group risk-team \
  --tag prod --tag v4 \
  --export ./archive

dino proof index metrics ./archive
dino proof index compare ./archive <hash_a> <hash_b>
dino proof index layout ./archive
```

### Request Early Access

Open an issue: https://github.com/DinoDevCli/dino/issues/new?title=Early%20Access%20Request  
Or email: [dinodevcli@gmail.com](mailto:dinodevcli@gmail.com)

---

## What is Dino?

| Capability | Role |
|------------|------|
| **Local audit engine** | Runs offline in CI and on laptops |
| **Deterministic proofs** | `proof.json` + `proof_hash` + capsule replay |
| **Export contracts** | Path / HTTP / S3 (`dino.proof.export.v1`) |
| **Proof index** | `proof_index.json` + compare / metrics / layout |

Not a general SAST suite, secret scanner, SBOM tool, or image provenance product.

---

## Why Dino?

- **No dashboard** — you render compliance charts yourself
- **No SaaS** — artifacts stay in your store
- **No cloud** — optional S3/HTTP is *your* infrastructure
- Fits **Risk, Fraud, Research, Compliance** teams that already have governance tooling

---

## Core contracts

| Schema | Purpose |
|--------|---------|
| [`dino.proof.bundle.v1`](docs/PROOF_CONTRACT.md) | Sealed proof chain |
| [`dino.proof.export.v1`](docs/PROOF_EXPORT.md) | Upload envelope |
| [`dino.proof.index.v1`](docs/PROOF_INDEX.md) | Manifest listing |
| `dino.proof.index.compare.v1` | Diff two proofs |
| `dino.proof.index.metrics.v1` | Health summary |

---

## Quickstart

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.1"
dino scan leakage ./tests/e2e/pipe.py          # Free pack

# Proof pack (Early Access — request a free Team Key):
dino upgrade --pack proof --key YOUR_TEAM_KEY
dino proof doctor

# Maintainers: issue Early Access keys
dino issue-key --team risk-lab --days 90

dino proof run \
  --command echo ok \
  --scan ./tests/e2e/pipe.py \
  --output-dir ./proof_out \
  --pipeline fraud_score_v4 \
  --group risk-team \
  --tag prod --tag v4 \
  --export ./archive

dino proof verify --proof ./proof_out/proof.json
dino proof index show ./archive
dino proof index metrics ./archive
```

`--command` takes argv tokens (`echo ok`) or one quoted string when the program needs `--flags`.
`--scan` must resolve to at least one `.py` file.

> Not on PyPI under `dino` (name collision). Install only via GitHub.

Requires Python ≥ 3.10.

---

## Integrating Dino

### Path

```bash
dino proof run ... --export ./archive \
  --pipeline fraud_score_v4 --group risk-team --tag prod
```

Consumers read `./archive/proof_index.json` and `./archive/<hash16>/`.

### HTTP

```bash
export DINO_EXPORT_HTTP_TOKEN=…
dino proof run ... --export https://internal.example/api/proofs \
  --pipeline fraud_score_v4 --group risk-team --tag prod
```

POST body: `dino.proof.export.v1` including `index_entry`.

### S3

```bash
dino proof run ... --export s3://team-bucket/proofs \
  --pipeline fraud_score_v4 --group risk-team --tag prod
```

Needs `boto3` or AWS CLI credentials.

### Index consumption

```bash
dino proof index metrics ./archive
dino proof index compare ./archive <hash_a> <hash_b>   # exit 1 if changed
dino proof index layout ./archive
dino proof index rebuild ./archive
```

Feed JSON into your alerts, drift charts, and compliance reports.

---

## Proof index layout

```
<archive>/<proof_hash16>/
  proof.json
  export.json
  scan.json …
<archive>/proof_index.json
<archive>/pipelines/<pipeline>/<proof_hash16>/
<archive>/groups/<group>/<proof_hash16>/
<archive>/tags/<tag>/<proof_hash16>/
```

Canonical bundles are content-addressed. Browse folders are symlinks (or `.dino_layout_ref` pointers).

---

## Modules

| Module | Pack | Role |
|--------|------|------|
| **Scan** | Free | Research leakage rules |
| **Capsule** | Proof | Sealed subprocess + replay |
| **Map** | Proof | AST graph, drift, plan |
| **Bundle** | Proof | Regression signals |
| **Flight** | Proof | Canary summary |
| **Verify** | Proof | Drift, supersession, attest |
| **Proof** | Proof | Chain + export + index |

## Packs

| Pack | Access | Role |
|------|--------|------|
| **Free** | Forever | Leakage scan (`dino scan leakage`) |
| **Proof** | Early Access Team Key | Capsule, map, bundle, flight, verify, proof chain + export/index |

Request a free Team Key: [issue](https://github.com/DinoDevCli/dino/issues/new?title=Early%20Access%20Request) · [dinodevcli@gmail.com](mailto:dinodevcli@gmail.com)

Engine only — dashboards are external.

Maintainer: issue keys + customer email pack → [`docs/internal/EARLY_ACCESS_OPS.md`](docs/internal/EARLY_ACCESS_OPS.md)

---

## Docs

| Doc | Role |
|-----|------|
| [`PROOF_CONTRACT.md`](docs/PROOF_CONTRACT.md) | Normative guarantees |
| [`PROOF_EXPORT.md`](docs/PROOF_EXPORT.md) | Export contracts |
| [`PROOF_INDEX.md`](docs/PROOF_INDEX.md) | Index / compare / metrics / layout |
| [`CLI_E2E_REFERENCE.md`](docs/CLI_E2E_REFERENCE.md) | CLI reference |
| [`EXAMPLES.md`](docs/EXAMPLES.md) | Short examples |
| [`INTEGRATION_DASHBOARDS.md`](docs/INTEGRATION_DASHBOARDS.md) | Airflow, MLflow, Superset, etc. |
| [`tests/simulation/`](tests/simulation/) | Production-grade team E2E simulation |
| [`website/`](website/) | Landing page |

---

## Development

```bash
git clone https://github.com/DinoDevCli/dino.git
cd dino
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/dino tests/e2e -q
```

---

## No UI. No SaaS. No Cloud.

Dino is the **engine**. Your dashboard consumes the **contracts**.

MIT · [DinoDevCli](https://github.com/DinoDevCli)
