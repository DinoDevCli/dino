# Proof export (uploader)

Dino is a **local audit engine**. It does **not** ship a dashboard, SaaS, or hosted control plane.

It emits sealed `proof.json` plus an optional **export contract** so teams drop proofs into *their* path / HTTP / S3 consumers.

Schema: **`dino.proof.export.v1`**

## CLI

Always pair export with index labels:

```bash
dino run \
  --scan ./tests/e2e/pipe.py \
  --output-dir ./proof_out \
  --pipeline fraud_score_v4 \
  --group risk-team \
  --tag prod --tag v4 \
  --export ./archive \
  -- echo ok

dino run ... --export https://internal-dashboard/api/proofs \
  --pipeline fraud_score_v4 --group risk-team --tag prod \
  -- echo ok

dino run ... --export s3://team-bucket/proofs \
  --pipeline fraud_score_v4 --group risk-team --tag prod \
  -- echo ok

dino proof export --proof-dir ./proof_out --to ./archive \
  --pipeline fraud_score_v4 --group risk-team --tag prod
```

Auth for HTTP: `DINO_EXPORT_HTTP_TOKEN` → `Authorization: Bearer …`.

S3: `boto3` **or** AWS CLI with credentials.

## Layout (file / S3)

```
<archive>/<hash16>/
  proof.json
  export.json          # envelope + index_entry
  capsule/…
  scan.json
<archive>/proof_index.json
<archive>/pipelines/<pipeline>/<hash16>/
<archive>/groups/<group>/<hash16>/
<archive>/tags/<tag>/<hash16>/
```

## HTTP contract

`POST` JSON (`dino.proof.export.v1`):

```json
{
  "schema": "dino.proof.export.v1",
  "proof_hash": "…",
  "proof": {},
  "artifacts": {},
  "index_entry": {
    "hash": "…",
    "pipeline": "fraud_score_v4",
    "group": "risk-team",
    "tags": ["prod", "v4"],
    "drift": "none",
    "leakage": "none"
  }
}
```

Headers: `Content-Type`, `X-Dino-Proof-Hash`, `X-Dino-Export-Schema`, optional `Authorization`.

## Integration model

| You provide | Dino provides |
|-------------|----------------|
| Dashboard / alerts / storage | Sealed proofs + export envelope |
| HTTP ingest or S3 bucket | `dino.proof.export.v1` POST / upload |
| Compliance renderers | `proof_index.json` updates |

See [`PROOF_INDEX.md`](PROOF_INDEX.md) for listing, metrics, compare, layout.
