# Integrating Dino into your dashboards

Dino is an **audit engine**, not a UI. You consume **export contracts** and **proof index** JSON from your own tools.

Schemas: [`PROOF_EXPORT.md`](PROOF_EXPORT.md) · [`PROOF_INDEX.md`](PROOF_INDEX.md)

---

## Pattern (all integrations)

```bash
dino run \
  --scan ./your_pipeline.py \
  --output-dir ./proof_out \
  --pipeline YOUR_PIPELINE_NAME \
  --group YOUR_TEAM \
  --tag prod \
  --export ./archive \
  -- echo ok
# or: --export s3://… / https://…
```

Then consume:

| Artifact | Use |
|----------|-----|
| `./archive/proof_index.json` | Listing, filters, history |
| `dino proof index metrics ./archive` | Health tiles, alerts |
| `dino proof index compare …` | CI gates, regression |
| `./archive/pipelines/…/` | Browse by pipeline |

---

## Apache Airflow

Post-task hook or `@task`:

```python
import subprocess

def dino_proof(**context):
    subprocess.run([
        "dino", "proof", "run",
        "--command", "python", "train.py",
        "--scan", "/opt/dags/pipeline/",
        "--output-dir", f"/tmp/proof/{context['run_id']}",
        "--pipeline", "fraud_score_v4",
        "--group", "risk-team",
        "--tag", "prod",
        "--export", "s3://team-bucket/dino-proofs",
    ], check=True)
```

Alert on compare in a downstream task:

```bash
dino proof index compare s3://…/local-mirror "$PREV_HASH" "$CURR_HASH" || exit 1
```

---

## Prefect

```python
from prefect import flow, task
import subprocess

@task
def seal_proof():
    subprocess.run([
        "dino", "proof", "run",
        "--command", "python", "flow_step.py",
        "--scan", "./src",
        "--pipeline", "prefect_flow_v1",
        "--export", "/data/dino/archive",
    ], check=True)

@flow
def my_flow():
    seal_proof()
```

Schedule `dino proof index metrics /data/dino/archive` on a cron Prefect deployment for dashboard feed.

---

## MLflow

After a run, export proof and log index metrics as tags:

```bash
dino run ... --export ./mlflow_proofs/$RUN_ID --pipeline $MLFLOW_RUN_NAME
METRICS=$(dino proof index metrics ./mlflow_proofs --json 2>/dev/null || dino --json proof index metrics ./mlflow_proofs)
# Parse JSON → mlflow.set_tag("dino.proof_hash", …)
```

Store `proof_hash` on MLflow run; link to `./archive/<hash16>/proof.json` in artifact store.

---

## Superset / Metabase

Starter kit (not a Dino UI): [`examples/superset/drift_dashboard.yaml`](../examples/superset/drift_dashboard.yaml)

1. Mount or sync `./archive/proof_index.json` to a database (ETL script below).
2. Build charts from flattened index rows — or import the starter YAML mapping.

Minimal ETL (Python):

```python
import json, sqlite3
from pathlib import Path

index = json.loads(Path("archive/proof_index.json").read_text())
rows = index["proofs"]
# INSERT INTO dino_proofs (hash, pipeline, drift, leakage, verdict, ts) …
```

Metabase: connect to SQLite/Postgres table · Superset: same.

Metrics dashboard: cron `dino proof index metrics ./archive` → push JSON to statsd/Prometheus via small adapter.

---

## Custom internal dashboard

**HTTP export** — your API receives:

```json
{
  "schema": "dino.proof.export.v1",
  "proof_hash": "…",
  "proof": { },
  "artifacts": { },
  "index_entry": { "pipeline": "…", "drift": "none", "leakage": "none" }
}
```

Merge `index_entry` into your DB. Render history from your schema — Dino never hosts it.

**Path export** — watch `proof_index.json` with inotify / S3 event → refresh cache.

---

## CI gate (GitHub Actions)

```yaml
- run: |
    dino run -- echo ok --scan ./tests/e2e/pipe.py \
      --export ./archive --pipeline ci --group eng --tag ci
    dino proof index compare ./archive "${{ env.PREV_HASH }}" "$(jq -r '.proofs[0].hash' archive/proof_index.json)"
  env:
    PREV_HASH: ${{ vars.DINO_BASELINE_HASH }}
```

Exit 1 on compare → block merge when drift/leakage/pipeline changes.

---

## What you build vs what Dino ships

| Dino ships | You build |
|------------|-----------|
| `proof.json`, export envelope | UI charts |
| `proof_index.json` | Alerts |
| compare / metrics CLI JSON | Auth, multi-tenant |
| layout folders | Hosting |

No Dino dashboard. No Dino SaaS. Engine only.
