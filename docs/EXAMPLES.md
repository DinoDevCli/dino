# Examples

Short commands for Dino 0.3.0. Live outputs: [`CLI_E2E_REFERENCE.md`](CLI_E2E_REFERENCE.md).

## Proof chain

```bash
dino upgrade --pack proof --key YOUR_LICENSE_KEY

dino proof run \
  --command echo ok \
  --repo . \
  --scan ./tests/dino/fixtures/scan/clean_code.py \
  --output-dir ./proof_out

dino proof verify --proof ./proof_out/proof.json
dino proof doctor
```

`--command` is argv (`echo ok`). One quoted string (`"echo ok"`) also works.

Export to a team store / dashboard ingest (no Dino dashboard — just upload):

```bash
dino proof run ... --export ./proofs_archive
dino proof run ... --export https://internal-dashboard/api/proofs
dino proof run ... --export s3://team-bucket/proofs
dino proof run ... --export ./proofs_archive \
  --pipeline fraud_score_v4 --group risk-team --tag prod

dino proof index show ./proofs_archive
dino proof index metrics ./proofs_archive
dino proof index compare ./proofs_archive <hash_a> <hash_b>
dino proof index layout ./proofs_archive
dino proof index rebuild ./proofs_archive
```

Details: [`PROOF_INDEX.md`](PROOF_INDEX.md) · [`PROOF_EXPORT.md`](PROOF_EXPORT.md)

## Leakage (Free pack)

```bash
dino scan leakage ./tests/dino/fixtures/scan/forbidden_import.py
# exit 1 — LEAKY_IMPORT

dino scan leakage ./tests/dino/fixtures/scan/clean_code.py
# exit 0 — no findings
```

## Capsule

```bash
dino capsule run --command echo sealed --output-dir ./cap
dino capsule replay --capsule ./cap/capsule.json
dino capsule doctor
```

## Map & drift

```bash
dino map analyze ./dino/common
dino map verify --repo ./dino/common
dino map drift ./tests/dino/fixtures/map/repo_small \
  --baseline ./tests/dino/fixtures/map/repo_clean
```

## Bundle & flight

```bash
dino bundle verify \
  --baseline ./tests/dino/fixtures/bundle/baseline_counts.json \
  --current ./tests/dino/fixtures/bundle/current_counts.json

dino flight summary \
  --artifacts-dir ./tests/dino/fixtures/flight/artifacts \
  --output ./flight.json
```

## Verify

```bash
dino verify drift --distance 0
dino verify supersede \
  --runtime-verdict REJECTED \
  --release-verdict APPROVED \
  --contract ./tests/dino/fixtures/verify/contract_release.json \
  --previous ./tests/dino/fixtures/verify/contract_previous.json
dino verify attest ./tests/dino/fixtures/verify/valid_attest.json \
  --trust-anchor ./tests/dino/fixtures/verify/trust_anchor.json
```
