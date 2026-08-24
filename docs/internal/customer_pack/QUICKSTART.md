# Dino Early Access — Quickstart

**Contact:** dinodevcli@gmail.com  
**Site:** https://dinodevcli.github.io/dino/  
**Release:** v{VERSION}

Early Access is open — your team can start immediately.

## Packs

| Pack | What you get | Key? |
|------|----------------|------|
| Free | Leakage scan | No |
| Proof | Seal → export → index → compare (+ capsule, map, …) | Yes (`KEY.txt`) |

Dino outputs artifacts. Your dashboards render them.

## Install

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v{VERSION}"
dino proof run --help
```

Not on PyPI as `dino` (name collision). Install from GitHub.

## Unlock Proof

```bash
dino upgrade --pack proof --key '{KEY}'
dino proof doctor
```

Or from this pack:

```bash
dino upgrade --pack proof --key "$(cat KEY.txt)"
dino proof doctor
```

## First seal + compare

```bash
dino proof run \
  --command "python your_pipeline.py" \
  --scan ./src \
  --pipeline fraud_score_v1 \
  --export ./archive

# second run with a different pipeline label / seed, then:
dino proof index compare ./archive <hash_a> <hash_b>
dino proof index metrics ./archive
```

`examples/proof_index.json` and `examples/compare.json` show the dashboard payload shape. Wire your UI to **your** `./archive/` files, not the examples.

Reproduce the website demo locally (from the git checkout):

```bash
cd tests/simulation && make demo
```
