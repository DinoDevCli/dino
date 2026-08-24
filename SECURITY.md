# Security

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.3.x   | Yes       |

## Reporting a vulnerability

Email **dinodevcli@gmail.com** with subject `Dino security`. Do not open a public issue for exploitable defects.

We aim to acknowledge within 72 hours.

## Fail-closed scan

Dino’s leakage scan is fail-closed: `EMPTY_SCAN_ROOTS` prevents silent passes. If `--scan` resolves to zero `.py` files, the run fails — it does not report a clean proof.

`dino --dev` relaxes `EMPTY_SCAN_ROOTS` for local iteration only. Do not use Developer Mode for production proofs. Other leakage rules still fail.

## Scope notes

Dino seals local subprocesses and scans Python research pipelines. It is **not** a general AppSec scanner. Report issues in: capsule replay integrity, proof hash verification, license/pack gating, or leakage-scan false negatives that break the stated contract.
