# Screenshot plan — one CLI capture that converts

Goal: **one** image above the Install section. Not a collage. Not a dashboard.

## The winning shot

**Story in one frame:** seal two runs → compare → `changed: true` with `pipeline_version_diff`.

### Commands (real product — do not invent)

```bash
dino proof run \
  --command "python pipeline/run.py --seed seed-42" \
  --scan ./pipeline \
  --pipeline fraud_score_v1 \
  --export ./archive

dino proof run \
  --command "python pipeline/run.py --seed seed-123" \
  --scan ./pipeline \
  --pipeline fraud_score_v2 \
  --export ./archive

dino proof index compare ./archive <hash_v1> <hash_v2>
```

Or one-shot: `cd tests/simulation && make demo`

### What must be visible

1. Prompt `$` + real `dino proof …` commands (not `dino run` / `dino diff` / `dino why`)
2. JSON (or excerpt) with **`"changed": true`** in accent orange `#FF6B00`
3. `pipeline_version_diff`: `fraud_score_v1` → `fraud_score_v2`
4. Dark chrome `#0A0A0F` / `#111118` — matches the site

### What must not appear

- `pip install dino-cli` / PyPI `dino`
- Fake hashes presented as sealed production proofs (use `<hash_v1>` / `<hash_v2>` or golden excerpts)
- Marketing badges, purple glow, fake SaaS UI

## Assets (shipped)

| File | Role |
|------|------|
| [`docs/assets/cli-compare.png`](../assets/cli-compare.png) | Primary README screenshot |
| [`docs/assets/demo-compare.gif`](../assets/demo-compare.gif) | 3s loop: run → diff → done (Issue #13) |

## Capture recipe (refresh)

1. Codespaces or local: https://codespaces.new/DinoDevCli/dino  
2. `cd tests/simulation && make demo`  
3. Screenshot the compare JSON (or regenerate GIF via Pillow frames in `docs/assets/`)  
4. Keep width ≤ 1200px, PNG &lt; ~300KB when possible  

## Placement

README: immediately under the one-line value prop, **before** Install.

```markdown
![dino proof index compare — changed: true](docs/assets/cli-compare.png)
```
