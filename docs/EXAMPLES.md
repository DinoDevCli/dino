# Examples

Kurze, aktuelle Befehle für Dino 0.3.0. Vollständige Outputs: [`CLI_E2E_REFERENCE.md`](CLI_E2E_REFERENCE.md).

## Proof chain

```bash
dino upgrade --pack proof

dino proof run \
  --command "echo ok" \
  --repo . \
  --scan ./tests/dino/fixtures/alpha/clean_code.py \
  --output-dir ./proof_out

dino proof verify --proof ./proof_out/proof.json
dino proof doctor
```

## Leakage (Free Pack)

```bash
dino scan leakage ./tests/dino/fixtures/alpha/forbidden_import.py
# exit 1 — LEAKY_IMPORT

dino scan leakage ./tests/dino/fixtures/alpha/clean_code.py
# exit 0 — no findings
```

## Capsule

```bash
dino capsule run --command "echo sealed" --output-dir ./cap
dino capsule replay --capsule ./cap/capsule.json
dino capsule doctor
```

## Map & drift

```bash
dino map analyze ./dino/common
dino map verify --repo ./dino/common
dino map drift ./tests/dino/fixtures/brain/repo_small \
  --baseline ./tests/dino/fixtures/brain/repo_clean
```

## Bundle & flight

```bash
dino bundle verify \
  --baseline ./tests/dino/fixtures/artifact/baseline_counts.json \
  --current ./tests/dino/fixtures/artifact/current_counts.json

dino flight summary \
  --artifacts-dir ./tests/dino/fixtures/canary/artifacts \
  --output ./flight.json
```

## Verify

```bash
dino verify drift --distance 0
dino verify supersede \
  --contract ./tests/dino/fixtures/attest/contract_release.json \
  --previous ./tests/dino/fixtures/attest/contract_previous.json
dino verify attest ./tests/dino/fixtures/attest/valid_attest.json \
  --trust-anchor ./tests/dino/fixtures/attest/trust_anchor.json
```
