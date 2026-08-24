# Outreach sequence (step-by-step)

Internal GTM workflow for open Early Access. Version: v0.3.1.

**Positioning (must stay consistent):**

- Open Early Access — any team can request a key. No “5–10 teams.”
- MIT core. Proof Pack after Early Access: one-time purchase per seat or team. No subscriptions. No cloud fees.
- Deterministic, content-addressed proofs and indexes.
- Dashboard integration: Path / HTTP / S3; starter kit `examples/superset/drift_dashboard.yaml`.
- Developer Mode: `dino --dev` relaxes `EMPTY_SCAN_ROOTS` only; production stays fail-closed.
- Codespaces: https://codespaces.new/DinoDevCli/dino → `cd tests/simulation && make demo`
- Website: https://dinodevcli.github.io/dino/

Templates: [`outreach.md`](outreach.md) · Targets: [`outreach_targets.md`](outreach_targets.md) · Keys: [`EARLY_ACCESS_OPS.md`](EARLY_ACCESS_OPS.md)

---

## Workflow

### 1. Prepare outreach message

Use the DE Kurztext or the English Outreach Template in [`outreach.md`](outreach.md).

Include: value (deterministic diff), website, Codespaces, key-request path (email / Early Access issue).

### 2. Select target teams

Pick 10–20 rows from [`outreach_targets.md`](outreach_targets.md) (Fraud Eng, Risk Modeling, ML Ops, Data Eng). Prefer Lead Engineer / ML Ops Lead / Fraud Analyst.

### 3. Send initial message

Channel: direct email (primary), or LinkedIn / community / GitHub only when appropriate. One short technical note — not a sales deck.

### 4. Respond with KEY.txt + Quickstart

When they reply with a team name:

```bash
export DINO_EA_SIGNING_SECRET='…'
./scripts/issue-early-access.sh <team-slug> 60
```

Send EMAIL.txt + attach the customer-pack ZIP (KEY.txt, QUICKSTART.md, LICENSE, VERSION, examples). See [`EARLY_ACCESS_OPS.md`](EARLY_ACCESS_OPS.md).

Activate hint:

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.1"
dino upgrade --pack proof --key "$(cat KEY.txt)"
dino proof doctor
```

### 5. Provide Codespaces link

https://codespaces.new/DinoDevCli/dino  

Then: `cd tests/simulation && make demo`

Point at the documentary walkthrough on the website if they want the audit log without setup.

### 6. Offer help integrating `proof_index.json`

- Export via Path / HTTP / S3.
- Consume `proof_index.json` / `compare.json` in their dashboard.
- Starter kit: `examples/superset/drift_dashboard.yaml`.
- Optional: `dino --dev` for local iteration only (not CI / production).

### 7. After 60 days: follow-up for Proof Pack licensing

- Remind key expiry (`exp` embedded).
- Offer renewal / post–Early Access one-time Proof Pack (seat or team).
- MIT core and free leakage scan remain available.
- No subscriptions. No cloud fees.

---

## Checklist (per team)

- [ ] Target logged (name, pipeline type, contact role)
- [ ] Initial message sent
- [ ] Key + Quickstart ZIP sent (ledger: team, days, prefix, ZIP name)
- [ ] Codespaces / demo pointed
- [ ] Integration help offered (`proof_index.json`)
- [ ] Day-60 licensing follow-up scheduled
