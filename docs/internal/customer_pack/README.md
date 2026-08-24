# Customer Pack ZIP — Early Access

Format: **customer-pack.v1**  
Issued by: [`scripts/issue-early-access.sh`](../../../scripts/issue-early-access.sh)

This folder is the **template**. Live packs (with a real Team Key) are written to `dist/customer-packs/` and are gitignored.

Early Access is open — any team can request a key.

## Tomorrow: customer writes → you send a ZIP

```bash
export DINO_EA_SIGNING_SECRET='prod-secret'
./scripts/issue-early-access.sh acme-risk 60
```

Optional greeting name:

```bash
./scripts/issue-early-access.sh acme-risk 60 --name "Alex"
```

The script issues the key, writes the folder, zips it, and prints the email body.

**Send:** paste `EMAIL.txt` → attach the `.zip` → From `dinodevcli@gmail.com`.

## Naming

| Piece | Rule | Example |
|-------|------|---------|
| Team slug | lowercase `[a-z0-9-]+` (spaces → `-`) | `acme-risk` |
| ZIP name | `dino-ea-<slug>-v<version>-<UTC stamp>.zip` | `dino-ea-acme-risk-v0.3.1-20260824T094300Z.zip` |
| Inner folder | `<slug>/` (exactly one top-level directory) | `acme-risk/` |
| Version | Dino release from `pyproject.toml` (install pin) | `0.3.1` |

Re-issuing the same team creates a **new** stamp + ZIP. Do not reuse an old ZIP after a new key.

## ZIP contents (`customer-pack.v1`)

```
acme-risk/
  KEY.txt              # Team Key only (one line) — dinoea.v1.…
  QUICKSTART.md        # install + unlock + first seal (key filled in)
  EMAIL.txt            # ready-to-send plaintext (Subject on line 1)
  LICENSE              # MIT (repo LICENSE)
  VERSION              # Dino release this pack is pinned to
  examples/
    proof_index.json   # schema-complete dashboard example
    compare.json       # schema-complete compare example
```

| File | Required | Source |
|------|----------|--------|
| `KEY.txt` | yes | `dino issue-key` |
| `QUICKSTART.md` | yes | this folder, `{KEY}` / `{VERSION}` substituted |
| `EMAIL.txt` | yes | [`EMAIL.txt`](EMAIL.txt) template, substituted |
| `LICENSE` | yes | repo `LICENSE` |
| `VERSION` | yes | `pyproject.toml` → `0.3.1` |
| `examples/proof_index.json` | optional (included) | this folder |
| `examples/compare.json` | optional (included) | this folder |

## Versioning

- **Dino version** (`VERSION`, install URL): the Git tag customers `pip install` (`v0.3.1`).
- **Pack layout** (`customer-pack.v1`): this file list and names. Bump to `v2` only if you add/rename/remove ZIP entries.
- **Key format**: `dinoea.v1.<payload>.<sig>` (independent of pack layout).

Install line in email + quickstart:

```bash
pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.1"
dino upgrade --pack proof --key "$(cat KEY.txt)"
dino proof doctor
```

## Examples

`examples/*.json` match engine schemas (`dino.proof.index.v1`, `dino.proof.index.compare.v1`) and the website demo story (fraud_score v1 → v2, `changed: true`).

Hashes are **illustrative** (`sha256("dino-example-fraud_score_v1")` / `_v2`), not from a sealed run. Dashboards should consume the customer's own `./archive/proof_index.json`.

## Ledger

After each send, record: team slug, days, UTC date, customer email, key prefix (`dinoea.v1.` + first 24 chars), ZIP filename.

## Local test (sim secret — do not send)

```bash
./scripts/issue-early-access.sh acme-risk 60 --allow-sim
```
