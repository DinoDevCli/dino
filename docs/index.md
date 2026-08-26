# Dino — Deterministic Python Runs

**Early Access · v1.0.0**

## Same code, same data, same environment — different outputs?

Dino seals every Python pipeline run into a proof, then tells you — deterministically — whether anything actually changed.

Two runs of the same pipeline. Same code, same data, same environment. Different outputs — and no way to prove why. Dino seals each run and compares them over time.

---

## Free vs Proof Pack

### Free — Snapshot Mode

Everything that runs **locally, once, without history**.

- Run a sealed proof locally (`dino run`, `dino proof run`)
- Scan your code for leakage (`dino scan`)
- Replay a capsule locally (`dino capsule run`, `dino capsule replay`)

Free is for testing whether Dino detects drift in your pipeline.

### Proof Pack — System Mode

Everything that requires **history, comparison, export, CI, or team metadata**.

- Proof index (compare, rebuild, metrics, layout)
- CI compare gate (exit 1 on drift)
- Export (Path + HTTP + S3)
- Bundle replay / verify / diff
- Map analyze / plan / drift / verify
- Team metadata (`--pipeline`, `--group`, `--tag`)
- Retention beyond 30 days

Proof Pack turns Dino from a snapshot tool into a pipeline stability system.

**Request a Team Key:** [dinodevcli@gmail.com](mailto:dinodevcli@gmail.com)

---

## Quickstart

### Free (Snapshot Mode)

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v1.0.0"
dino scan .
dino run -- python my_pipeline.py
```

> Not on PyPI as `dino` / `dino-cli` (name collision). Install from GitHub only.

### Proof Pack (System Mode)

```bash
dino upgrade --pack proof --key YOUR_KEY
dino proof index compare ./archive <HASH_A> <HASH_B>
```

Request a Team Key: [dinodevcli@gmail.com](mailto:dinodevcli@gmail.com)

---

## Why Dino?

Python pipelines drift even when code, data, and the environment are identical.  
Dino seals each run and shows exactly what changed.

It captures: Imports, AST structure, Data access, Environment state, Artifacts, Runtime metadata — then compares sealed runs with deterministic deltas so you can see **why** two runs differ, not just that they differ.

---

## Documentation

Site: https://dinodevcli.github.io/dino/

Repo docs: [`PROOF_CONTRACT.md`](PROOF_CONTRACT.md) · [`PROOF_INDEX.md`](PROOF_INDEX.md) · [`PROOF_EXPORT.md`](PROOF_EXPORT.md) · [`QUICKSTART.md`](QUICKSTART.md) · [`LICENSING.md`](LICENSING.md)
