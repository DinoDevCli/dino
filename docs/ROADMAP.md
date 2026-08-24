# Roadmap

Shipped (v0.3.1): local-first proof engine, export contracts, proof index, Early Access Team Keys, fail-closed leakage scan, Codespaces, Superset starter kit.

Tracking issues: [#1](https://github.com/DinoDevCli/dino/issues/1) Developer Mode · [#2](https://github.com/DinoDevCli/dino/issues/2) Superset kit · [#3](https://github.com/DinoDevCli/dino/issues/3) contract v2 · [#5](https://github.com/DinoDevCli/dino/issues/5) runners · [#4](https://github.com/DinoDevCli/dino/issues/4) integration examples.

## Developer Mode (`--dev`)

Shipped: `dino --dev` relaxes `EMPTY_SCAN_ROOTS` so local iteration is not blocked by a missing scan root. Other leakage rules still fail. Production (no `--dev`) stays fail-closed.

Further relaxations stay out of the default path. Feedback: GitHub Discussions.

## Proof Pack contract v2

Plan the next schema version for proof bundles and indexes (`dino.proof.bundle.v2` / `dino.proof.index.v2`). Add versioning rules and deterministic replay constraints. Current contracts stay `v1`.

## Pipeline runners

Document future support for containerized runners and optional R/Julia via reticulate or PyCall. Python remains the native path. Roadmap only — no promises.

## Integration examples

Minimal Airflow DAG, MLflow callback, and Superset dashboard examples beyond the current integration guide and [`examples/superset/drift_dashboard.yaml`](../examples/superset/drift_dashboard.yaml).

## Later

- One-time Proof Pack license after Early Access ([`LICENSING.md`](LICENSING.md))
- More dashboard starter kits (Metabase / Grafana)
