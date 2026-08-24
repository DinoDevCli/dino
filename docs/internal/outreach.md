# Outreach — Fraud / Risk / ML teams

Public contact: dinodevcli@gmail.com  
Website: https://dinodevcli.github.io/dino/  
Codespaces: https://codespaces.new/DinoDevCli/dino

Early Access is open. Any team can request a key. 60-day Proof Pack. No “5–10 teams.” No checkout.

---

## Short message

Subject: Dino — deterministic diff between two pipeline runs

Hi,

Dino is a local-first audit engine for Python pipelines. Two fraud-score runs — v1 and v2 — should not be a mystery. Dino seals both, exports them, and produces a machine-readable compare (`changed: true/false`, `pipeline_version_diff`).

It is not a dashboard or SaaS. You keep Superset, Airflow, MLflow, or your own UI. Dino outputs `proof_index.json` and `compare.json` via Path / HTTP / S3.

Try without setup: https://codespaces.new/DinoDevCli/dino  
Then: `cd tests/simulation && make demo`

Website: https://dinodevcli.github.io/dino/

**Request a Team Key** — 60-day Proof Pack trial. Email your team name to dinodevcli@gmail.com (or open a GitHub issue titled Early Access Request). Leakage scan stays free forever.

MIT core. No subscriptions. No cloud fees.

—
Dino

---

## Value (one line)

Deterministic, content-addressed diff between two pipeline runs — so CI and audits can see what changed.

---

## How to request a Team Key

1. Email dinodevcli@gmail.com with the team / project name (and size if useful).
2. Or open: https://github.com/DinoDevCli/dino/issues/new?title=Early%20Access%20Request
3. You receive a ZIP: KEY.txt, QUICKSTART.md, EMAIL.txt, LICENSE, VERSION, examples.

Activate:

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.1"
dino upgrade --pack proof --key YOUR_TEAM_KEY
dino proof doctor
```
