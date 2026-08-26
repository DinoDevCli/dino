# Dino — Deterministic Python Runs

## Same code, same data, same environment — different outputs?

Dino detects and explains pipeline drift.

Python pipelines drift for reasons that are hard to see:
unstable imports, hidden state, nondeterministic splits, silent dependency changes.
Dino seals each run and compares them over time.

---

# Two Tiers

## Free — Snapshot Mode

Local, single-run, no history.

Includes:

- `dino scan`
- `dino run` / `dino proof run` (local)
- `dino capsule run` / `replay` (local)

Use Free to test whether Dino detects drift in your pipeline.

---

## Proof Pack — System Mode

History, comparison, export, CI, team metadata.

Includes:

- proof index (compare, rebuild, metrics, layout)
- CI compare gate
- export (Path/HTTP/S3)
- bundle / map / verify / flight
- team metadata (`--pipeline`, `--group`, `--tag`)
- retention > 30 days

Upgrade: https://dino.dev/upgrade

---

# Quickstart

## Free

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v1.0.0"
dino scan .
dino run -- python my_pipeline.py
```

## Proof Pack

```bash
dino upgrade --pack proof --key YOUR_KEY
dino proof index compare ./archive <HASH_A> <HASH_B>
```

Team Key: [dinodevcli@gmail.com](mailto:dinodevcli@gmail.com)

---

# Documentation

All commands, schemas, and examples:  
https://dinodevcli.github.io/dino/

Repo docs: [`PROOF_CONTRACT.md`](PROOF_CONTRACT.md) · [`PROOF_INDEX.md`](PROOF_INDEX.md) · [`PROOF_EXPORT.md`](PROOF_EXPORT.md) · [`QUICKSTART.md`](QUICKSTART.md)
