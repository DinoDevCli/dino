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
# Auto-update index + browse layout on export
dino proof run ... \
  --export ./proofs_archive \
  --pipeline fraud_score_v4 \
  --group risk-team \
  --tag prod --tag v4

dino proof export --proof-dir ./proof_out --to ./proofs_archive \
  --pipeline fraud_score_v4

# Read / rebuild / layout
dino proof index show ./proofs_archive
dino proof index rebuild ./proofs_archive
dino proof index layout ./proofs_archive

# Compare two proofs (exit 1 if changed)
dino proof index compare ./proofs_archive abc123 def456

# Health summary JSON
dino proof index metrics ./proofs_archive
```

## Compare contract (`dino.proof.index.compare.v1`)

```bash
dino proof index compare ./proofs_archive <hash_a> <hash_b>
```

JSON includes: `drift_delta`, `leakage_delta`, `supersede_status`, `artifacts_diff`,
`pipeline_version_diff`, `verdict_diff`, `status_diff`, `tags_diff`, `changed`.

Hashes may be full, prefix, or `path` slug. Exit **1** when `changed` is true (handy for CI).

## Metrics contract (`dino.proof.index.metrics.v1`)

```bash
dino proof index metrics ./proofs_archive
```

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

## Archive layout contract

Canonical bundles stay content-addressed:

```
<archive>/<proof_hash16>/
<archive>/proof_index.json
```

Browse views (symlinks when the OS allows, else `.dino_layout_ref` pointers):

```
<archive>/pipelines/<pipeline>/<proof_hash16>/
<archive>/groups/<group>/<proof_hash16>/
<archive>/tags/<tag>/<proof_hash16>/
```

Updated on every local `--export` and via `dino proof index layout|rebuild`.

## Where it lives

| Export target | Index behavior |
|---------------|----------------|
| **Local path** | `<archive>/proof_index.json` + layout links |
| **S3** | `s3://bucket/prefix/proof_index.json` |
| **HTTP** | `index_entry` inside export POST body |

HTTP ingest: merge `index_entry` into your DB — Dino does not host the index.

## Why this is enough

Companies feed `proof_index.json` + compare/metrics into:

- compliance reports
- drift charts
- audit pipelines
- governance UIs / alerts

Dino stays the **local audit motor** + **uploader** + **manifest**. You keep the dashboard.

See also: [`PROOF_EXPORT.md`](PROOF_EXPORT.md)
