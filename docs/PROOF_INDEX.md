# Proof index manifest

Schema: **`dino.proof.index.v1`** · File: **`proof_index.json`**

No dashboard. No UI. A single JSON contract so teams can list, compare, version, tag, group, and historize proofs in **their** systems.

## Example

```json
{
  "schema": "dino.proof.index.v1",
  "updated_at": "2026-08-23T12:00:00Z",
  "proofs": [
    {
      "hash": "abc123…full proof_hash",
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

| Field | Meaning |
|-------|---------|
| `drift` | `none` when aligned; else drift bucket from map |
| `leakage` | `none` (clean), `failed`, or `skipped` |
| `path` | Bundle folder under archive (`<hash16>/`) |
| `group` / `tags` | Optional — set via CLI |

## CLI

```bash
# Auto-update index on export
dino proof run ... \
  --export ./proofs_archive \
  --pipeline fraud_score_v4 \
  --group risk-team \
  --tag prod --tag v4

dino proof export --proof-dir ./proof_out --to ./proofs_archive \
  --pipeline fraud_score_v4

# Read / rebuild
dino proof index show ./proofs_archive
dino proof index rebuild ./proofs_archive
```

## Where it lives

| Export target | Index behavior |
|---------------|----------------|
| **Local path** | `<archive>/proof_index.json` (merge by `hash`) |
| **S3** | `s3://bucket/prefix/proof_index.json` |
| **HTTP** | `index_entry` inside export POST body |

HTTP ingest: merge `index_entry` into your DB — Dino does not host the index.

## Why this is enough

Companies feed `proof_index.json` into:

- compliance reports
- drift charts
- audit pipelines
- governance UIs

Dino stays the **local audit motor** + **uploader** + **manifest**. You keep the dashboard.

See also: [`PROOF_EXPORT.md`](PROOF_EXPORT.md)
