# Early Access Ops — issue Team Keys + customer pack ZIP

**Contact (public):** [dinodevcli@gmail.com](mailto:dinodevcli@gmail.com)  
**Website:** https://dinodevcli.github.io/dino/  
**Repo:** https://github.com/DinoDevCli/dino  
**Pack spec:** [`customer_pack/README.md`](customer_pack/README.md) (`customer-pack.v1`)

Early Access is open — any team can request a key.

## Packs (what customers get)

| Pack | Included | Access |
|------|----------|--------|
| **Free** | `dino scan leakage` | Forever, no key |
| **Proof** | capsule, map, bundle, flight, verify, proof (seal → export → index → compare) | Early Access Team Key |

Engine only — dashboards are external. Customers bring Superset / Airflow / MLflow / custom UI.

## When a customer writes

Example: *We are ACME Risk, team size 4, want Early Access.*

```bash
export DINO_EA_SIGNING_SECRET='prod-secret'
./scripts/issue-early-access.sh acme-risk 60
# optional: --name "Alex"
```

The script issues the key and writes:

```
dist/customer-packs/dino-ea-acme-risk-v0.3.2-<stamp>.zip
```

Inner layout:

```
acme-risk/
  KEY.txt
  QUICKSTART.md
  EMAIL.txt
  LICENSE
  VERSION
  examples/
    proof_index.json
    compare.json
```

Send `EMAIL.txt` from dinodevcli@gmail.com and attach the ZIP.

Record: team, days, date, contact email, key prefix (`dinoea.v1.` + first 24 chars), ZIP name.

## Customer activate

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.2"
dino upgrade --pack proof --key "$(cat KEY.txt)"
dino proof doctor
dino packs
```

Free scan works without a key:

```bash
dino scan leakage ./path/to/pipeline
```

## Expiry

Keys embed `exp` (unix). After expiry, `dino upgrade` / proof domains fail closed until a new key is issued. Re-run the script and send a **new** ZIP (do not reuse the old KEY.txt).

## Checklist before send

- [ ] `DINO_EA_SIGNING_SECRET` is the production secret (not `--allow-sim`)
- [ ] Team slug matches their project (`acme-risk`)
- [ ] Days = 60 (website) unless you agreed otherwise
- [ ] Email body is the generated `EMAIL.txt` (dinodevcli@gmail.com)
- [ ] ZIP attached
- [ ] No pricing / checkout language
- [ ] Ledger line copied
- [ ] Remind: engine + artifacts only; dashboards are theirs
