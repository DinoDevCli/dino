# Dino — Deterministic Python Runs

## Same code, same data, same environment — different outputs?

Dino detects and explains pipeline drift.

Modern Python pipelines drift in subtle ways:

- nondeterministic imports
- unstable data splits
- hidden state in modules
- accidental leakage
- environment supersession
- silent dependency changes

Dino seals each run, records its structure, and compares runs over time.

---

# Free vs Proof Pack

## Free — Snapshot Mode

Everything that runs **locally, once, without history**.

You can:

- run a sealed proof locally (`dino run`, `dino proof run`)
- scan your code for leakage (`dino scan`)
- replay a capsule locally (`dino capsule run`, `dino capsule replay`)

Free is for testing whether Dino detects drift in your pipeline.

---

## Proof Pack — System Mode

Everything that requires **history, comparison, export, CI, or team metadata**.

You unlock:

- proof index (compare, rebuild, metrics, layout)
- CI compare gate (Exit 1 on drift)
- export (Path + HTTP + S3)
- bundle replay / verify / diff
- map analyze / plan / drift / verify
- verify attest / binary / drift / supersede
- team metadata (`--pipeline`, `--group`, `--tag`)
- retention > 30 days

Proof Pack turns Dino from a snapshot tool into a **pipeline stability system**.

Upgrade: https://dino.dev/upgrade

---

# Quickstart

## Free (Snapshot Mode)

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v1.0.0"
dino scan .
dino run -- python my_pipeline.py
```

> Not on PyPI as `dino` / `dino-cli` (name collision). Install from GitHub only.

## Proof Pack (System Mode)

```bash
dino upgrade --pack proof --key YOUR_KEY
dino proof index compare ./archive <HASH_A> <HASH_B>
dino proof export --proof-dir ./proof_out --to s3://my-bucket/proofs
```

Request a Team Key: [dinodevcli@gmail.com](mailto:dinodevcli@gmail.com)

---

# Why Dino?

Python pipelines drift even when:

- code is identical
- data is identical
- environment is identical

Dino shows you **exactly why**.

It seals:

- imports
- AST structure
- data access
- environment state
- artifacts
- runtime metadata

And compares runs with deterministic deltas.

---

# Documentation

https://dinodevcli.github.io/dino/

---

# License

MIT
