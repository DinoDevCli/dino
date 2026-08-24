# Quickstart

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.1"
dino proof run --help
```

Not on PyPI as `dino` (name collision). Install from GitHub.

No local Python? [Open in GitHub Codespaces](https://codespaces.new/DinoDevCli/dino).

## First seal

```bash
dino proof run \
  --command "python your_pipeline.py" \
  --scan ./src \
  --pipeline fraud_score_v1 \
  --export ./archive
```

Compare two runs:

```bash
dino proof index compare ./archive <hash_a> <hash_b>
```

Leakage scan is free forever (no key):

```bash
dino scan leakage ./your_pipeline
```

Proof Pack (capsule, export, index, compare) needs an Early Access Team Key:

```bash
dino upgrade --pack proof --key YOUR_TEAM_KEY
dino proof doctor
```

Email [dinodevcli@gmail.com](mailto:dinodevcli@gmail.com) with your team name.

## Developer Mode

Production is fail-closed: missing scan roots (`EMPTY_SCAN_ROOTS`) fail the run.

During local iteration:

```bash
dino --dev proof run --command "echo ok" --scan ./does_not_exist
```

`--dev` relaxes `EMPTY_SCAN_ROOTS` only. Real leakage findings still fail. Do not use for production proofs.

## Dashboards

Dino outputs `proof_index.json` and `compare.json`. Starter mapping: [`examples/superset/drift_dashboard.yaml`](../examples/superset/drift_dashboard.yaml).

More: [`INTEGRATION_DASHBOARDS.md`](INTEGRATION_DASHBOARDS.md)
