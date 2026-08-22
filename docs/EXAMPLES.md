# Examples

Kurze, aktuelle Befehle für Dino 0.3.0. Vollständige Outputs: [`CLI_E2E_REFERENCE.md`](CLI_E2E_REFERENCE.md).

## Proof chain

```bash
dino upgrade --pack proof

dino proof run \
  --command "echo ok" \
  --repo . \
  --scan ./tests/dino/fixtures/scan/clean_code.py \
  --output-dir ./proof_out

dino proof verify --proof ./proof_out/proof.json
dino proof doctor
```

## Leakage (Free Pack)

```bash
dino scan leakage ./tests/dino/fixtures/scan/forbidden_import.py
# exit 1 — LEAKY_IMPORT

dino scan leakage ./tests/dino/fixtures/scan/clean_code.py
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
  --contract ./tests/dino/fixtures/verify/contract_release.json \
  --previous ./tests/dino/fixtures/verify/contract_previous.json
dino verify attest ./tests/dino/fixtures/verify/valid_attest.json \
  --trust-anchor ./tests/dino/fixtures/verify/trust_anchor.json
```
