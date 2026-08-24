# Dino

[![CI](https://github.com/DinoDevCli/dino/actions/workflows/ci.yml/badge.svg)](https://github.com/DinoDevCli/dino/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)

## Version

**Local-First Audit Engine for Python Pipelines**

Dino is a local-first audit engine that produces sealed proofs, export envelopes, and a universal proof index for your dashboards.

All proof bundles and indexes are deterministic and reproducible (content-addressed).

v0.3.1 · Early Access

## Install

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.1"
dino proof run --help
```

Not on PyPI as `dino` (name collision). Install from GitHub.

## Problem

Two fraud-score runs — v1 and v2.

You do not know what differs. Drift is invisible: no sealed artifacts, no machine-readable delta.

CI cannot decide if a run changed. Audits stay manual and inconsistent.

## How it works

Seal. Export. Index. Compare.

Dino seals each run into a proof bundle (capsule + scan + hash), exports the bundle (Path / HTTP / S3), builds a proof index (`proof_index.json`), and compares two proofs deterministically. The verdict is `changed: true/false`.

## Engine

`pipeline → seal → export → index → compare → dashboard`

All proof bundles and indexes are deterministic and reproducible (content-addressed).

| Step | Artifact |
|------|----------|
| Seal | `proof.json` — capsule + scan + hash |
| Export | Path / HTTP / S3 — `export.v1` envelope |
| Index | `proof_index.json` — metadata · metrics · layout |
| Compare | `changed: true` — `pipeline_version_diff` |

### Dashboard integration

Dashboards consume Dino's artifacts (`proof_index.json`, `compare.json`) via Path, HTTP, or S3.

Superset, Airflow, MLflow, or your own UI can render drift, verdicts, and metrics.

Dino outputs the data — you choose the visualization.

See [`docs/INTEGRATION_DASHBOARDS.md`](docs/INTEGRATION_DASHBOARDS.md).

## Demo: Audit Log

We audit a fraud-score pipeline. Two runs — v1 and v2. Dino seals both, exports them, builds a proof index, and compares them.

```bash
dino proof run \
  --command "python pipeline/run.py --seed seed-42" \
  --scan ./pipeline \
  --pipeline fraud_score_v1 \
  --export ./archive

dino proof run \
  --command "python pipeline/run.py --seed seed-123" \
  --scan ./pipeline \
  --pipeline fraud_score_v2 \
  --export ./archive

dino proof index compare ./archive <hash_v1> <hash_v2>
```

Fail-closed: Dino refuses to pass a run with missing scan roots (`EMPTY_SCAN_ROOTS`).

```bash
dino proof run --command "echo ok" --scan ./does_not_exist
```

Reproduce locally: `cd tests/simulation && make demo`  
All demo artifacts come from [`tests/simulation/golden`](tests/simulation/golden) in this repository.

## Early Access

Early Access is open — any team can request a key.

Free Mode. Proof Pack. 60 Days.

- Leakage scan — free forever
- Proof pack — free Team Key, 60 days
- Email [dinodevcli@gmail.com](mailto:dinodevcli@gmail.com) — name your team or project

Engine only — dashboards are external.

[Open an issue](https://github.com/DinoDevCli/dino/issues/new?title=Early%20Access%20Request) · [dinodevcli@gmail.com](mailto:dinodevcli@gmail.com)

```bash
dino upgrade --pack proof --key YOUR_TEAM_KEY
dino proof doctor
```

Maintainer: issue keys + customer ZIP → [`docs/internal/EARLY_ACCESS_OPS.md`](docs/internal/EARLY_ACCESS_OPS.md)

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

## Development

```bash
git clone https://github.com/DinoDevCli/dino.git
cd dino
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/dino tests/e2e -q
```

MIT · [DinoDevCli](https://github.com/DinoDevCli)
