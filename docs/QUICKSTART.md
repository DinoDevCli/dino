# Quickstart

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v1.0.0"
dino run --help
```

Not on PyPI as `dino` (name collision). Install from GitHub.

No local Python? [Open in GitHub Codespaces](https://codespaces.new/DinoDevCli/dino).

## First seal

Trailing command form (primary):

```bash
# Basic
dino run -- python your_pipeline.py

# With scan
dino run --scan ./src -- python your_pipeline.py

# With export
dino run \
  --scan ./src \
  --pipeline fraud_score_v1 \
  --export ./archive \
  -- python your_pipeline.py
```

Compare two runs:

```bash
dino proof index compare ./archive <HASH_A> <HASH_B>
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

```text
---
Early Access (Proof Pack)
  CI compare gate · S3/HTTP backends · engine contract stability · team mode
  These features are not part of the open-source scan engine.

  Details & instructions:
    https://github.com/DinoDevCli/dino#early-access
    Contact: dinodevcli@gmail.com
```

## Developer Mode

Production is fail-closed: missing scan roots (`EMPTY_SCAN_ROOTS`) fail the run.

During local iteration:

```bash
dino --dev run --scan ./does_not_exist -- echo ok
```

`--dev` relaxes `EMPTY_SCAN_ROOTS` only. Real leakage findings still fail. Do not use for production proofs.

## Dashboards

Dino outputs `proof_index.json` and `compare.json`. Starter mapping: [`examples/superset/drift_dashboard.yaml`](../examples/superset/drift_dashboard.yaml).

More: [`INTEGRATION_DASHBOARDS.md`](INTEGRATION_DASHBOARDS.md)
