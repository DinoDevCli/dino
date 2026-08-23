# Customer email — Early Access Team Key

**From:** dinodevcli@gmail.com  
**Subject:** Dino Early Access — Proof Pack Team Key ({TEAM})

---

Hi {NAME},

Welcome to Dino Early Access.

Dino is a local-first audit engine: it seals runs, exports envelopes, and builds a proof index your dashboards consume. It does not include a dashboard.

## Your Team Key

```
{KEY}
```

- Team: `{TEAM}`
- Valid: `{DAYS}` days
- Pack: Proof (capsule · map · bundle · flight · verify · proof)

## Activate

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.1"
dino upgrade --pack proof --key '{KEY}'
dino proof doctor
```

Leakage scan stays free forever (no key):

```bash
dino scan leakage ./your_pipeline
```

## Docs

- Website: https://dinodevcli.github.io/dino/
- README: https://github.com/DinoDevCli/dino#readme
- Dashboard integration: https://github.com/DinoDevCli/dino/blob/main/docs/INTEGRATION_DASHBOARDS.md
- Local demo: `tests/simulation/` (`make demo`)

Questions → reply to this email (dinodevcli@gmail.com).

— Dino
