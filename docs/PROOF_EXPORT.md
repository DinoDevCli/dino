# Proof export (uploader)

Dino does **not** ship a dashboard. It ships a sealed `proof.json` and an optional **export** so teams can drop proofs into their own store / API / bucket.

Schema: `dino.proof.export.v1`

## CLI

```bash
# During seal
dino proof run \
  --command echo ok \
  --scan ./path/to/pipeline.py \
  --output-dir ./proof_out \
  --export ./proofs_archive

dino proof run ... --export https://internal-dashboard/api/proofs
dino proof run ... --export s3://team-bucket/proofs

# After the fact
dino proof export --proof-dir ./proof_out --to ./proofs_archive
dino proof export --proof ./proof_out/proof.json --to https://internal-dashboard/api/proofs
```

Auth for HTTP: set `DINO_EXPORT_HTTP_TOKEN` (sent as `Authorization: Bearer …`).

S3: needs `boto3` **or** AWS CLI (`aws s3 sync`) with credentials.

## Layout (file / S3)

Content-addressed subfolder: `<dest>/<proof_hash[:16]>/`

```
<dest>/<hash16>/
  proof.json
  export.json          # full envelope
  capsule/capsule.json
  capsule/replay.json
  scan.json            # if present
  map_verify.json      # if present
```

## HTTP contract

`POST` JSON:

```json
{
  "schema": "dino.proof.export.v1",
  "proof_hash": "…",
  "proof": { "...": "proof.json body" },
  "artifacts": {
    "capsule/capsule.json": {},
    "scan.json": {}
  }
}
```

Headers:

- `Content-Type: application/json`
- `X-Dino-Proof-Hash: <proof_hash>`
- `X-Dino-Export-Schema: dino.proof.export.v1`
- `Authorization: Bearer <token>` (optional)

Expected response: `2xx`. Body ignored except for diagnostics.

## Why this matters

Export turns Dino into the **local audit motor** that companies wire into existing dashboards — without Dino becoming SaaS.

Each export also maintains **`proof_index.json`** (schema `dino.proof.index.v1`) at the archive root — list/compare/tag proofs without a Dino UI. See [`PROOF_INDEX.md`](PROOF_INDEX.md).
