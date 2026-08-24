# Dino documentation

Local-first audit engine for Python pipelines — sealed proofs, export contracts, proof index.

**Website:** https://dinodevcli.github.io/dino/  
**Repo:** https://github.com/DinoDevCli/dino

## Engine

Dino seals each run, exports the bundle (Path / HTTP / S3), writes `proof_index.json`, and compares two proofs. `changed: true/false`.

All proof bundles and indexes are deterministic and reproducible (content-addressed).

- [`PROOF_CONTRACT.md`](PROOF_CONTRACT.md) — what a proof guarantees
- [`PROOF_EXPORT.md`](PROOF_EXPORT.md) — Path / HTTP / S3 envelopes
- [`PROOF_INDEX.md`](PROOF_INDEX.md) — index / compare / metrics / layout
- [`CLI_E2E_REFERENCE.md`](CLI_E2E_REFERENCE.md) — CLI reference

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
pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.1"
dino proof run --help
```

[Open in GitHub Codespaces](https://codespaces.new/DinoDevCli/dino) — clone, install Dino, open a terminal. Then `cd tests/simulation && make demo`.

## Examples

- [`EXAMPLES.md`](EXAMPLES.md) — short commands
- [`INTEGRATION_DASHBOARDS.md`](INTEGRATION_DASHBOARDS.md) — Airflow, MLflow, Superset
- [`examples/superset/`](../examples/superset/) — drift dashboard starter kit (`drift_dashboard.yaml`)
- [`tests/simulation/`](../tests/simulation/) — fraud-score demo

## Early Access

Early Access is open — any team can request a key.

Email [dinodevcli@gmail.com](mailto:dinodevcli@gmail.com) with your team name. 60-day Proof Pack.

## Pricing & Licensing

[`LICENSING.md`](LICENSING.md)

Dino is MIT-licensed. The core engine is free. Advanced audit features (Proof Pack) require a license. After Early Access, Proof Pack will be available as a one-time purchase per seat or team. No subscriptions. No cloud fees.

## Roadmap

[`ROADMAP.md`](ROADMAP.md)

Developer Mode (`dino --dev`) relaxes `EMPTY_SCAN_ROOTS` during development. Production stays fail-closed.

## Support

Questions or issues? [Open an Issue](https://github.com/DinoDevCli/dino/issues/new) or [Discussion](https://github.com/DinoDevCli/dino/discussions) on GitHub.
