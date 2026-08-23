# Dino Early Access — Quickstart

**Contact:** dinodevcli@gmail.com  
**Site:** https://dinodevcli.github.io/dino/

## Packs

| Pack | What you get | Key? |
|------|----------------|------|
| Free | Leakage scan | No |
| Proof | Seal → export → index → compare (+ capsule, map, …) | Yes (Team Key below) |

Dino outputs artifacts. Your dashboards render them.

## Install

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.1"
dino version
dino packs
```

## Unlock Proof

```bash
dino upgrade --pack proof --key 'YOUR_TEAM_KEY'
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

Reproduce the website demo locally:

```bash
cd tests/simulation && make demo
```

Golden excerpts live in `tests/simulation/golden/`.
