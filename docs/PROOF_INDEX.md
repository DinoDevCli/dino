# Proof index manifest

Schema: **`dino.proof.index.v1`** · File: **`proof_index.json`**

Engine contract for listing, comparing, tagging, grouping, and historizing proofs — **without** a Dino UI or SaaS.

## Example entry

```json
{
  "schema": "dino.proof.index.v1",
  "updated_at": "2026-08-23T12:00:00Z",
  "proofs": [
    {
      "hash": "abc123…",
      "timestamp": "2026-08-23T12:00:00Z",
      "pipeline": "fraud_score_v4",
      "group": "risk-team",
      "tags": ["prod", "v4"],
      "drift": "none",
      "leakage": "none",
      "supersede": false,
      "status": "passed",
      "verdict": "PROOF_PASSED",
      "artifacts": ["proof.json", "scan.json", "capsule/capsule.json"],
      "path": "abc123def4567890"
    }
  ]
}
```

## CLI (engine → consumer)

```bash
dino run \
  --scan ./tests/e2e/pipe.py \
  --output-dir ./proof_out \
  --pipeline fraud_score_v4 \
  --group risk-team \
  --tag prod --tag v4 \
  --export ./archive \
  -- echo ok

dino proof index show ./archive
dino proof index metrics ./archive
dino proof index compare ./archive <HASH_A> <HASH_B>
dino proof index layout ./archive
dino proof index rebuild ./archive
```

### Compare — `dino.proof.index.compare.v1`

Drift / leakage / supersede / artifacts / pipeline / verdict / tags deltas.  
Exit **1** when `changed` (CI-friendly).

### Metrics — `dino.proof.index.metrics.v1`

```json
{
  "schema": "dino.proof.index.metrics.v1",
  "total": 128,
  "passed": 120,
  "failed": 8,
  "drift_none": 110,
  "drift_minor": 12,
  "drift_severe": 6,
  "leakage_detected": 3,
  "pipelines": ["fraud_score_v4", "risk_model_v2"]
}
```

### Layout contract

```
<archive>/<hash16>/
<archive>/proof_index.json
<archive>/pipelines/<pipeline>/<hash16>/
<archive>/groups/<group>/<hash16>/
<archive>/tags/<tag>/<hash16>/
```

Symlinks when possible; otherwise `.dino_layout_ref` pointers.

## Dashboard consumption

Your systems:

1. Watch `proof_index.json` or HTTP `index_entry`
2. Call / parse `metrics` for health tiles
3. Call / parse `compare` for regression gates
4. Browse `pipelines/` · `groups/` · `tags/` for folder-based audits

Dino does not host the index. Dino is the motor.

See [`PROOF_EXPORT.md`](PROOF_EXPORT.md).
