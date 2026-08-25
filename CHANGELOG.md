# Changelog

## Unreleased

## 1.0.0

- **CLI UX v1.0:** grouped `dino --help`, first-class `dino run` alias (trailing `--` form), positional `bundle create`, compare metavars `HASH_A` / `HASH_B`
- **Docs / website:** install pins, examples, and CLI reference updated for `dino run` + Early Access (Proof Pack) help block
- **Version:** public release tag `v1.0.0`

## 0.3.2

- **CLI help:** documentary `Optional features (Proof Pack)` block on `dino --help`, `dino proof run --help`, and `dino proof index compare --help` (no behavior change)
- **Packs:** `dino packs` points at `--help` Proof Pack section + Early Access email
- **Version sync:** `dino.__version__` aligned with `pyproject.toml` (was stale at 0.3.0)
- **Developer Mode:** `dino --dev` relaxes `EMPTY_SCAN_ROOTS` for local iteration (not for production proofs)
- **Docs landing:** [`docs/index.md`](docs/index.md)
- **Codespaces:** `.devcontainer/` — Open in GitHub Codespaces
- **Dashboard starter:** [`examples/superset/drift_dashboard.yaml`](examples/superset/drift_dashboard.yaml)
- **Docs / website:** install pins and GitHub Pages copy bumped to v0.3.2
- **Help tour:** [`docs/cli-help-tour.txt`](docs/cli-help-tour.txt)

## 0.3.1

- **Early Access is open** — any team can request a free Team Key ([dinodevcli@gmail.com](mailto:dinodevcli@gmail.com) / GitHub issue); no checkout
- **Early Access keys:** HMAC-signed `dinoea.v1.*` with expiry (`dino issue-key`, auto-deactivate)
- **Packs:** Free scan forever · Proof pack via Early Access Team Key
- **Determinism:** All proof bundles and indexes are deterministic and reproducible (content-addressed)
- **Production simulation:** `tests/simulation/` — fraud pipeline + full Dino team workflow
- **Positioning:** local-first audit engine — outputs artifacts; dashboards are external
- Export contracts: path / HTTP / S3 (`dino.proof.export.v1`)
- Proof index: `proof_index.json`, compare, metrics, layout (`dino.proof.index.v1`)
- Full E2E suite: `tests/e2e/`
- Dashboard integration guide: `docs/INTEGRATION_DASHBOARDS.md`

## 0.3.0

- Proof chain: `proof run` / `verify` / `doctor` with content-addressed `proof.json`
- Capsule seal + replay with tamper detection
- Leakage scan (7 research rules) + `EMPTY_SCAN_ROOTS` fail-closed
- `--command` accepts argv tokens or one shell-like string
- Packs: Free (scan) · Proof (capsule, map, bundle, flight, verify, proof)
- License unlock path for Proof pack (`dino upgrade --pack proof --key`)
