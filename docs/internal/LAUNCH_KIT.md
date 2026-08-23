# Launch kit — Dino public announcement

**Story (repeat everywhere):**

> **Dino — Local-First Audit Engine for Python Pipelines**  
> Deterministic proofs, export contracts, and a universal proof index for your dashboards.  
> Dino is a local audit motor — not a platform. No UI. No SaaS. No cloud.

**Links:** GitHub https://github.com/DinoDevCli/dino · Release https://github.com/DinoDevCli/dino/releases/tag/v0.3.1 · Website https://dinodevcli.github.io/dino/

---

## Checklist (7 steps)

| # | Action | Status |
|---|--------|--------|
| 01 | GitHub Release v0.3.1 | Done — https://github.com/DinoDevCli/dino/releases/tag/v0.3.1 |
| 02 | Website live | **https://dinodevcli.github.io/dino/** (Vercel optional for custom domain) |
| 03 | Post X / LinkedIn / Reddit / HN (copy below) | Manual |
| 04 | DM 5–10 teams (Risk, Fraud, ML, Research) — template below | Manual |
| 05 | Share integration doc with teams using Superset/Airflow/etc. | [`INTEGRATION_DASHBOARDS.md`](../INTEGRATION_DASHBOARDS.md) |
| 06 | Collect 3–5 case studies — template below | Ongoing |
| 07 | Pitch newsletters — templates below | Manual |

**Early Access (current):** Free scan forever · Proof pack via free Team Key ·  
[early@dinodevcli.dev](mailto:early@dinodevcli.dev) · no checkout · dashboards external.

---

## GitHub Release notes (paste into v0.3.1)

```markdown
## Early Access

Dino v0.3.1 enters **Early Access**.
Team Keys are free. No checkout.

**Request Early Access:** [Open an issue](https://github.com/DinoDevCli/dino/issues/new?title=Early%20Access%20Request) · [early@dinodevcli.dev](mailto:early@dinodevcli.dev)

---

## Dino v0.3.1 — Local-First Audit Engine

**Dino — Local-First Audit Engine for Python Pipelines**  
Deterministic proofs, export envelopes, and a universal proof index for your dashboards.

Dino outputs audit artifacts — dashboards render them. Engine only.

### What's new since v0.3.0

- **Export contracts** — path / HTTP / S3 (`dino.proof.export.v1`)
- **Proof index** — `proof_index.json` (`dino.proof.index.v1`)
- **Compare / Metrics / Layout** — governance JSON for your dashboards
- **Archive layout** — `pipelines/` · `groups/` · `tags/` browse links
- **Full E2E test suite** — `tests/e2e/`
- **Early Access Team Keys** — free unlock for Proof pack

### Quickstart

pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.1"
dino scan leakage ./tests/e2e/pipe.py          # free forever

# Early Access — request a free Team Key:
dino upgrade --pack proof --key YOUR_TEAM_KEY

dino proof run \
  --command echo ok \
  --scan ./tests/e2e/pipe.py \
  --output-dir ./proof_out \
  --pipeline fraud_score_v4 \
  --group risk-team \
  --tag prod --tag v4 \
  --export ./archive

dino proof index metrics ./archive

### Docs

- [README](https://github.com/DinoDevCli/dino#readme)
- [PROOF_EXPORT](https://github.com/DinoDevCli/dino/blob/main/docs/PROOF_EXPORT.md)
- [PROOF_INDEX](https://github.com/DinoDevCli/dino/blob/main/docs/PROOF_INDEX.md)
- [Dashboard integration](https://github.com/DinoDevCli/dino/blob/main/docs/INTEGRATION_DASHBOARDS.md)
- [Website](https://dinodevcli.github.io/dino/)

### Packs

Free scan forever · Proof pack via Early Access Team Key · Engine only — dashboards external.
```

---

## X (Twitter) — short

```
Shipped: Dino — local-first audit engine for Python pipelines.

Seal runs → export to path/HTTP/S3 → proof_index.json
Compare · metrics · layout — for YOUR dashboard.

Not SaaS. Not a platform. An engine.

https://github.com/DinoDevCli/dino
```

## LinkedIn — longer

```
We built Dino because risk and ML teams don't need another hosted control plane.

They need a local audit motor that emits:
• deterministic proof.json
• export contracts (path / HTTP / S3)
• proof_index.json + compare / metrics / layout

Your team keeps Superset, Airflow, MLflow, internal dashboards.
Dino feeds the artifacts.

Local-first. MIT. Python pipelines. No cloud product.

Try it: https://github.com/DinoDevCli/dino
Looking for 5–10 early-adopter teams (risk, fraud, research, ML governance) — reply or DM.
```

## Hacker News — Show HN title + post

**Title:** Show HN: Dino – local-first audit engine for Python pipelines (proofs + export contracts)

**Post:**

```
Hi HN — we open-sourced Dino, a CLI that seals Python pipeline runs and exports deterministic proof artifacts for your own dashboards.

Problem: teams need audit evidence (repro, leakage, drift) but don't want another SaaS control plane.

Dino runs locally/CI, produces content-addressed proof.json, and optionally exports to:
- filesystem archive + proof_index.json
- HTTP POST (your ingest API)
- S3 prefix

Index CLI gives compare/metrics/layout JSON — no Dino UI.

Stack: Python 3.10+, MIT, ~110 tests including full E2E.

Quickstart:
  pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.1"
  dino proof run --command echo ok --scan ./pipe.py --export ./archive --pipeline my_pipe

Looking for feedback from risk/fraud/ML teams integrating this into existing tooling.

https://github.com/DinoDevCli/dino
```

## Reddit — r/Python or r/MachineLearning

**Title:** [P] Dino — local audit engine for Python pipelines (proof export + index, no dashboard)

**Body:** Same as HN, slightly shorter. Emphasize: not replacing Semgrep, niche is sealed decision-pipeline proofs.

---

## Early-adopter outreach (email/DM)

```
Subject: Early access — Dino (local audit engine for Python pipelines)

Hi — we're looking for 5–10 small teams (risk, fraud, ML governance, research) to try Dino.

Dino is NOT a dashboard or SaaS. It's a local CLI that:
- seals pipeline runs (deterministic proof.json)
- exports to your path / HTTP / S3
- maintains proof_index.json + compare/metrics for your existing tools

15-min setup: pip install from GitHub, proof run + --export, wire index JSON into your dashboard or CI.

If you're open to a 30-min feedback call in exchange for a free Team key, reply here.

Repo: https://github.com/DinoDevCli/dino
```

---

## Case study template (internal → publish later)

```markdown
# Case study: [Team name] + Dino

## Team profile
- Domain: Risk / Fraud / Research / ML Governance
- Stack: Python, [Airflow/Prefect], [dashboard]
- Size: [N] engineers

## Problem
[What audit/repro/drift pain existed]

## Integration
- Export target: [path / S3 / HTTP]
- Dashboard consumer: [tool]
- Index usage: metrics / compare / layout

## Outcome
- [Metric: e.g. CI gate on proof compare]
- [Quote from champion]

## Artifacts
- Sample proof_index.json (redacted)
- CLI commands used
```

---

## Newsletter pitches (one paragraph each)

**Python Weekly / PyCoder's Weekly:**  
Dino is a local-first audit engine for Python decision pipelines — seals runs, exports `dino.proof.export.v1` envelopes to path/HTTP/S3, and maintains `proof_index.json` with compare/metrics/layout CLI for dashboard consumption. MIT, no hosted UI. https://github.com/DinoDevCli/dino

**TLDR / Console.dev:**  
Local audit motor for Python ML/risk pipelines: deterministic proofs + export contracts + proof index. Integrates into your stack — not another platform. v0.3.1 on GitHub.

**MLOps Community / Data Engineering Weekly:**  
Teams wire Dino into Airflow/Prefect post-task hooks → S3 archive → Superset/Metabase reads `proof_index.json` metrics. Compare CLI exits non-zero on drift/leakage regression. Docs: INTEGRATION_DASHBOARDS.md

---

## Repo settings

```bash
gh repo edit DinoDevCli/dino \
  --description "Local-first audit engine for Python pipelines — proofs, export contracts, proof index. Early Access: free scan + free Team Keys." \
  --homepage "https://dinodevcli.github.io/dino/"

gh repo edit DinoDevCli/dino --add-topic python --add-topic mlops --add-topic audit --add-topic local-first
```

Contact: **early@dinodevcli.dev** (same as website). No Lemon checkout during Early Access.