# Dino documentation

Local-first audit engine for Python pipelines — sealed proofs, export contracts, proof index.

**Website:** https://dinodevcli.github.io/dino/  
**Repo:** https://github.com/DinoDevCli/dino  
**Version:** v1.0.0 · Early Access · CLI v1.0

Same story as the site: Problem → How it works → Engine → Demo → Early Access → Pricing & Licensing.

## Engine

Dino seals each run, exports the bundle (Path / HTTP / S3), writes `proof_index.json`, and compares two proofs. `changed: true/false`.

All proof bundles and indexes are deterministic and reproducible (content-addressed).

Dashboards consume artifacts via Path, HTTP, or S3. Dino outputs the data — you choose the visualization.

- [`PROOF_CONTRACT.md`](PROOF_CONTRACT.md) — what a proof guarantees
- [`PROOF_EXPORT.md`](PROOF_EXPORT.md) — Path / HTTP / S3 envelopes
- [`PROOF_INDEX.md`](PROOF_INDEX.md) — index / compare / metrics / layout
- [`CLI_E2E_REFERENCE.md`](CLI_E2E_REFERENCE.md) — CLI reference

## CLI (v1.0)

### Core Workflow

- `dino run` — alias for `proof run` (trailing `--` form)
- `dino proof` — full proof chain
- `dino scan` — grammar + leakage scan

### Pipeline Operations

- `dino capsule` · `dino bundle` · `dino map` · `dino verify` · `dino flight`

### System & Packs

- `dino packs` · `dino status` · `dino upgrade` · `dino version`

### Notable forms

```bash
dino run --scan ./pipeline -- python pipeline/run.py
dino bundle create RUNDATA_PATH OUTPUT_PATH [--repo-root ROOT]
dino proof index compare PATH HASH_A HASH_B
dino map drift PATH --baseline PATH [--tau N]
```

```text
---
Early Access (Proof Pack)
  CI compare gate · S3/HTTP backends · engine contract stability · team mode
  These features are not part of the open-source scan engine.

  Details & instructions:
    https://github.com/DinoDevCli/dino#early-access
    Contact: dinodevcli@gmail.com
```

## Proof Pack

Free: `dino scan leakage` forever.  
Proof Pack: capsule, map, bundle, flight, verify, proof chain + export/index — Early Access Team Key.

## Contracts

| Schema | Role |
|--------|------|
| `dino.proof.bundle.v1` | Sealed proof |
| `dino.proof.export.v1` | Upload envelope |
| `dino.proof.index.v1` | Manifest |
| `dino.proof.index.compare.v1` | Diff two proofs |
| `dino.proof.index.metrics.v1` | Health summary |

## Quickstart

[`QUICKSTART.md`](QUICKSTART.md) · [Install on GitHub](https://github.com/DinoDevCli/dino#install)

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v1.0.0"
dino run --help
```

## Codespaces

[Open in GitHub Codespaces](https://codespaces.new/DinoDevCli/dino) — clones the repo, installs Python and Dino, opens a terminal.

```bash
cd tests/simulation && make demo
```

## Examples

- [`EXAMPLES.md`](EXAMPLES.md) — short commands
- [`INTEGRATION_DASHBOARDS.md`](INTEGRATION_DASHBOARDS.md) — Airflow, MLflow, Superset
- [`tests/simulation/`](../tests/simulation/) — fraud-score demo

## Starter Kit

[`examples/superset/drift_dashboard.yaml`](../examples/superset/drift_dashboard.yaml) maps `proof_index.json` rows into charts you recreate in **your** Apache Superset. Not a Dino product. Not a hosted UI.

## Developer Mode (`--dev`)

Production is fail-closed: `EMPTY_SCAN_ROOTS` prevents silent passes.

`dino --dev` relaxes `EMPTY_SCAN_ROOTS` only. Leakage findings remain fail-closed. Do not use `--dev` for production proofs.

```bash
dino --dev run --scan ./does_not_exist -- echo ok
```

[`ROADMAP.md`](ROADMAP.md) · [`QUICKSTART.md`](QUICKSTART.md)

## Early Access

Open Early Access. Any team can request a key. 60-day Proof Pack trial.

Email [dinodevcli@gmail.com](mailto:dinodevcli@gmail.com) with your team name.

## Pricing & Licensing

[`LICENSING.md`](LICENSING.md)

MIT core. Proof Pack license after Early Access. One-time purchase. No subscriptions. No cloud fees.

Dino is MIT-licensed. The core engine is free. Advanced audit features (Proof Pack) require a license. After Early Access, Proof Pack will be available as a one-time purchase per seat or team.

## Roadmap

[`ROADMAP.md`](ROADMAP.md)

- [#1](https://github.com/DinoDevCli/dino/issues/1) Developer Mode (`--dev`)
- [#2](https://github.com/DinoDevCli/dino/issues/2) Superset starter kit
- [#3](https://github.com/DinoDevCli/dino/issues/3) Proof Pack contract v2
- [#5](https://github.com/DinoDevCli/dino/issues/5) Pipeline runners (container, R, Julia)
- [#4](https://github.com/DinoDevCli/dino/issues/4) Integration examples (Airflow, MLflow, Superset)

Discussions: [Pricing & Licensing](https://github.com/DinoDevCli/dino/discussions/6) · [Developer Mode](https://github.com/DinoDevCli/dino/discussions/7) · [Dashboard patterns](https://github.com/DinoDevCli/dino/discussions/8)

## Support

Questions or issues? [Open an Issue](https://github.com/DinoDevCli/dino/issues/new) or [Discussion](https://github.com/DinoDevCli/dino/discussions) on GitHub.
