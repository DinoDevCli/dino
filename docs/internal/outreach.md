# Outreach — Fraud / Risk / ML teams

Public contact: dinodevcli@gmail.com  
Website: https://dinodevcli.github.io/dino/  
Codespaces: https://codespaces.new/DinoDevCli/dino  
Version: v1.0.0 · Open Early Access

Early Access is open. Any team can request a key. 60-day Proof Pack. No “5–10 teams.” No checkout.

MIT core. Proof Pack license after Early Access: one-time purchase per seat or team. No subscriptions. No cloud fees.

Related: [`outreach_targets.md`](outreach_targets.md) · [`outreach_sequence.md`](outreach_sequence.md)

---

## Kurztext (DE)

Hallo, wir bauen Dino — eine Audit-Engine für Python-Pipelines.  
Wenn ihr Fraud-Scores oder Risk-Pipelines habt, könnt ihr damit deterministisch prüfen, ob ein Run sich geändert hat.  
Demo + Codespaces + Starter Kit: https://dinodevcli.github.io/dino  
Wenn ihr testen wollt, schicke ich euch KEY.txt + Quickstart.  
Early Access ist offen — 60 Tage Proof Pack.

Codespaces (ohne Setup): https://codespaces.new/DinoDevCli/dino → `cd tests/simulation && make demo`

Key anfordern: Teamnamen an dinodevcli@gmail.com (oder GitHub Issue „Early Access Request“).

Wert in einem Satz: deterministischer Diff zwischen zwei Pipeline-Läufen (`changed: true/false`).

---

## X / Twitter (neutral)

```
Pipeline drift debugging experiment.
Compare two runs deterministically.
https://github.com/DinoDevCli/dino
```

---

## A) English Outreach Template

Subject: Dino — deterministic diff between two pipeline runs

Hi,

Dino is a local-first audit engine for Python pipelines (Fraud / Risk / ML / Data Engineering).

**Value:** two runs of the same pipeline should not be a mystery. Dino seals both, exports them, and produces a machine-readable compare — `changed: true/false`, `pipeline_version_diff`. Content-addressed. Deterministic.

Not a dashboard or SaaS. You keep Superset, Airflow, MLflow, or your own UI. Dino outputs `proof_index.json` and `compare.json` via Path / HTTP / S3. Starter kit: `examples/superset/drift_dashboard.yaml`.

- Website: https://dinodevcli.github.io/dino/
- Codespaces (no local setup): https://codespaces.new/DinoDevCli/dino  
  Then: `cd tests/simulation && make demo`

**Request a Team Key** — open Early Access, 60-day Proof Pack trial.  
Email your team name to dinodevcli@gmail.com (or open a GitHub issue titled “Early Access Request”). You get KEY.txt + Quickstart.

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v1.0.0"
dino upgrade --pack proof --key YOUR_TEAM_KEY
dino proof doctor
```

Leakage scan stays free forever. Production stays fail-closed; local iteration can use `dino --dev` (relaxes `EMPTY_SCAN_ROOTS` only).

MIT core. No subscriptions. No cloud fees.

— Dino

---

## B) Outreach Channels

| Channel | Use |
|---------|-----|
| **Direct email** | Primary. dinodevcli@gmail.com ↔ team lead / engineer. |
| **LinkedIn** | Technical leads only (Fraud Eng, Risk Modeling, ML Ops, Data Eng). No spray. |
| **GitHub** | Issues / Discussions in Fraud / Risk / ML pipeline repos — only when relevant and welcome. |
| **Slack / Discord** | Fraud / Risk / ML Ops communities — short technical note + website + Codespaces. |
| **MLflow / Airflow Discussions** | Integration patterns (proof after task, compare in CI). Point to docs + starter kit. |

Do not claim limited seats. Early Access is open.

---

## C) Outreach Sequence

1. Identify 10–20 target teams → [`outreach_targets.md`](outreach_targets.md).
2. Send the short technical outreach message (DE or EN above).
3. On request: provide KEY.txt + Quickstart (customer-pack ZIP via [`EARLY_ACCESS_OPS.md`](EARLY_ACCESS_OPS.md)).
4. Provide Codespaces link: https://codespaces.new/DinoDevCli/dino → `cd tests/simulation && make demo`.
5. Offer help integrating `proof_index.json` (Path / HTTP / S3; Superset starter kit).
6. After 60 days: follow-up for Proof Pack licensing (one-time purchase per seat or team; MIT core remains free).

Full workflow: [`outreach_sequence.md`](outreach_sequence.md).

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
pip install "git+https://github.com/DinoDevCli/dino.git@v1.0.0"
dino upgrade --pack proof --key YOUR_TEAM_KEY
dino proof doctor
```
