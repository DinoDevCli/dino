# Examples

Short commands for Dino 1.0.0 — local audit engine. Live dumps: [`CLI_E2E_REFERENCE.md`](CLI_E2E_REFERENCE.md).

## Proof + export + index

```bash
dino upgrade --pack proof --key YOUR_LICENSE_KEY

# Primary: trailing command form
dino run \
  --scan ./tests/e2e/pipe.py \
  --output-dir ./proof_out \
  --pipeline fraud_score_v4 \
  --group risk-team \
  --tag prod --tag v4 \
  --export ./archive \
  -- echo ok

dino proof verify --proof ./proof_out/proof.json
dino proof doctor

dino proof index show ./archive
dino proof index metrics ./archive
dino proof index compare ./archive <HASH_A> <HASH_B>
dino proof index layout ./archive
dino proof index rebuild ./archive
```

Other export targets (same labels):

```bash
dino run ... --export https://internal.example/api/proofs \
  --pipeline fraud_score_v4 --group risk-team --tag prod \
  -- echo ok

dino run ... --export s3://team-bucket/proofs \
  --pipeline fraud_score_v4 --group risk-team --tag prod \
  -- echo ok
```

`--command ARGV` still works. Trailing `-- cmd …` is the preferred form.

Contracts: [`PROOF_EXPORT.md`](PROOF_EXPORT.md) · [`PROOF_INDEX.md`](PROOF_INDEX.md)

## Leakage (Free pack)

```bash
dino scan leakage ./tests/dino/fixtures/scan/forbidden_import.py
# exit 1 — LEAKY_IMPORT

dino scan leakage ./tests/e2e/pipe.py
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
dino bundle create RUNDATA_PATH OUTPUT_PATH [--repo-root ROOT]

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

```text
---
Early Access (Proof Pack)
  CI compare gate · S3/HTTP backends · engine contract stability · team mode
  These features are not part of the open-source scan engine.

  Details & instructions:
    https://github.com/DinoDevCli/dino#early-access
    Contact: dinodevcli@gmail.com
```
