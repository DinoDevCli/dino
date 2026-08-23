# Early Access Ops — issue Team Keys + customer pack

**Contact (public):** [dinodevcli@gmail.com](mailto:dinodevcli@gmail.com)  
**Website:** https://dinodevcli.github.io/dino/  
**Repo:** https://github.com/DinoDevCli/dino

## Packs (what customers get)

| Pack | Included | Access |
|------|----------|--------|
| **Free** | `dino scan leakage` | Forever, no key |
| **Proof** | capsule, map, bundle, flight, verify, proof (seal → export → index → compare) | Early Access Team Key |

Engine only — dashboards are external. Customers bring Superset / Airflow / MLflow / custom UI.

## Maintainer: issue a key

```bash
# Production: set a strong secret (same secret must verify on customer machines
# only if you distribute online verify — currently keys are HMAC with this secret).
export DINO_EA_SIGNING_SECRET='replace-with-long-random-secret'

# Issue (default 90 days)
dino issue-key --team "acme-risk" --days 90

# Or helper script (prints key + email body)
./scripts/issue-early-access.sh acme-risk 90
```

Record each issuance: team, days, date, contact email, key prefix (`dinoea.v1.…` first 24 chars).

## Customer pack (send together)

1. **Team Key** — full `dinoea.v1.…` string  
2. **Email** — paste from [`customer_pack/EMAIL_TEMPLATE.md`](customer_pack/EMAIL_TEMPLATE.md)  
3. **Quickstart** — attach or link [`customer_pack/QUICKSTART.md`](customer_pack/QUICKSTART.md)  
4. Links: website · README · `docs/INTEGRATION_DASHBOARDS.md` · `tests/simulation/`

## Customer activate

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.1"
dino upgrade --pack proof --key 'dinoea.v1.…'
dino proof doctor
dino packs
```

Free scan works without a key:

```bash
dino scan leakage ./path/to/pipeline
```

## Expiry

Keys embed `exp` (unix). After expiry, `dino upgrade` / proof domains fail closed until a new key is issued.

## Checklist before send

- [ ] Team name matches their project  
- [ ] Days = 60 or 90 (website says 60-day Proof pack)  
- [ ] Key issued with production `DINO_EA_SIGNING_SECRET`  
- [ ] Email uses dinodevcli@gmail.com  
- [ ] No pricing / checkout language  
- [ ] Remind: engine + artifacts only; dashboards are theirs  
