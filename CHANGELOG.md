# Changelog

## 0.3.1

- **Early Access:** free Team Keys (`dinodevcli@gmail.com` / GitHub issue); no checkout
- **Early Access keys:** HMAC-signed `dinoea.v1.*` with expiry (`dino issue-key`, auto-deactivate)
- **Packs:** Free scan forever · Proof pack via Early Access Team Key
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
