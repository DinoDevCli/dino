# Dino CLI — Reference (engine + contracts)

**Version:** 0.3.0 · **Positioning:** local-first audit engine — not a platform  
**Flag:** `--json` (JSON envelope) · **E2E suite:** `tests/e2e/`

Dino seals proofs and emits **export** + **index** contracts for *your* dashboards. No hosted UI. No SaaS.

### Integration snapshot

```bash
dino proof run \
  --command echo ok \
  --scan ./tests/e2e/pipe.py \
  --output-dir ./proof_out \
  --pipeline fraud_score_v4 \
  --group risk-team \
  --tag prod --tag v4 \
  --export ./archive

dino proof index metrics ./archive
dino proof index compare ./archive <hash_a> <hash_b>
dino proof index layout ./archive
```

Contracts: [`PROOF_EXPORT.md`](PROOF_EXPORT.md) · [`PROOF_INDEX.md`](PROOF_INDEX.md) · [`PROOF_CONTRACT.md`](PROOF_CONTRACT.md)

---

# Dino CLI — Vollständige Referenz mit E2E-Outputs

**Stand:** 2026-08-22 · **Version:** 0.3.0
**Repo:** `devsecops` · **Flag:** `--json` (JSON-Envelope)
**Artefakte:** `/tmp/dino_cli_e2e/`

---

## Global

```bash
dino [--help] [--version] [--json]
```

| Flag | Beschreibung |
|------|--------------|
| `--help` | Hilfe |
| `--version` | Version anzeigen |
| `--json` | JSON-Output-Envelope (domain/command/result) |

---

## Meta-Befehle (Top-Level)

### `dino packs`

```bash
dino packs
```

```
Dino packs (free + proof)

[*] free       free   forever
    Free forever — grammar smoke + causal leakage scan for research pipelines.
    domains: scan

[*] proof      ea     Early Access · free Team Key
    Proof Pack (Early Access) — capsule, map, bundle, flight, verify, proof chain, export, and index. Request a free Team Key.
    domains: capsule, map, bundle, flight, verify, proof

Unlock:  dino upgrade --pack proof --key YOUR_TEAM_KEY
         (request key: early@dinodevcli.dev)
```

**exit:** 0

### `dino status`

```bash
dino status
```

```
dino 0.3.0
Active packs: free, proof
  [ON ] bundle
  [ON ] capsule
  [ON ] flight
  [ON ] map
  [ON ] proof
  [ON ] scan
  [ON ] verify
```

**exit:** 0

### `dino version`

```bash
dino version
```

```
0.3.0
```

**exit:** 0

```bash
dino init-license
dino upgrade --pack proof|free [--key KEY]
```

*(init-license/upgrade geben Text aus — siehe `dino upgrade` ohne Args für Usage)*

---

## Pack-Gate

| Pack | Domains |
|------|---------|
| **free** | `scan` |
| **proof** | `capsule`, `map`, `bundle`, `flight`, `verify`, `proof` |

---

## Baum

```
dino
├── packs | status | init-license | upgrade | version
├── scan → grammar | leakage
├── bundle → create | replay | verify | diff | archive | dedup
├── flight → summary
├── verify → attest | binary | drift | supersede
├── map → analyze | verify | plan | drift
├── capsule → run | replay | doctor
└── proof → run | verify | doctor
```

---

## scan (pack: free)

### `dino scan grammar`

```bash
dino scan grammar
```

```json
{
  "command": "grammar",
  "domain": "scan",
  "result": {
    "backend": "dino.domains.scan.grammar",
    "invalid": [
      true,
      true,
      true
    ],
    "status": "ok",
    "valid": [
      true,
      true,
      true
    ],
    "version": "ALPHA_GRAMMAR_V1"
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino scan leakage tests/dino/fixtures/scan/clean_code.py`

```bash
dino scan leakage tests/dino/fixtures/scan/clean_code.py
```

```json
{
  "command": "leakage",
  "domain": "scan",
  "result": {
    "files_scanned": 1,
    "findings": [],
    "ok": true,
    "rules": [
      "SYNTAX",
      "LEAKY_IMPORT",
      "FUTURE_INDEX",
      "SHIFT_NEGATIVE",
      "CONVOLVE_MODE_SAME_AST",
      "SEEDLESS_SPLIT",
      "TARGET_IN_FEATURES"
    ],
    "schema": "dino.scan.leakage.v1"
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino scan leakage tests/dino/fixtures/scan/forbidden_import.py`

```bash
dino scan leakage tests/dino/fixtures/scan/forbidden_import.py
```

```json
{
  "command": "leakage",
  "domain": "scan",
  "result": {
    "files_scanned": 1,
    "findings": [
      {
        "detail": "forbidden economics import",
        "line": null,
        "path": "tests/dino/fixtures/scan/forbidden_import.py",
        "rule": "LEAKY_IMPORT",
        "severity": "FAIL"
      }
    ],
    "ok": false,
    "rules": [
      "SYNTAX",
      "LEAKY_IMPORT",
      "FUTURE_INDEX",
      "SHIFT_NEGATIVE",
      "CONVOLVE_MODE_SAME_AST",
      "SEEDLESS_SPLIT",
      "TARGET_IN_FEATURES"
    ],
    "schema": "dino.scan.leakage.v1"
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 1

### `dino scan leakage tests/dino/fixtures/scan/shift_and_seedless.py`

```bash
dino scan leakage tests/dino/fixtures/scan/shift_and_seedless.py
```

```json
{
  "command": "leakage",
  "domain": "scan",
  "result": {
    "files_scanned": 1,
    "findings": [
      {
        "detail": "train_test_split without random_state",
        "line": 11,
        "path": "tests/dino/fixtures/scan/shift_and_seedless.py",
        "rule": "SEEDLESS_SPLIT",
        "severity": "FAIL"
      },
      {
        "detail": "negative shift (future peek)",
        "line": null,
        "path": "tests/dino/fixtures/scan/shift_and_seedless.py",
        "rule": "SHIFT_NEGATIVE",
        "severity": "FAIL"
      }
    ],
    "ok": false,
    "rules": [
      "SYNTAX",
      "LEAKY_IMPORT",
      "FUTURE_INDEX",
      "SHIFT_NEGATIVE",
      "CONVOLVE_MODE_SAME_AST",
      "SEEDLESS_SPLIT",
      "TARGET_IN_FEATURES"
    ],
    "schema": "dino.scan.leakage.v1"
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 1

### `dino scan leakage tests/dino/fixtures/scan/target_in_features.py`

```bash
dino scan leakage tests/dino/fixtures/scan/target_in_features.py
```

```json
{
  "command": "leakage",
  "domain": "scan",
  "result": {
    "files_scanned": 1,
    "findings": [
      {
        "detail": "feature matrix appears to include label/target columns",
        "line": 4,
        "path": "tests/dino/fixtures/scan/target_in_features.py",
        "rule": "TARGET_IN_FEATURES",
        "severity": "FAIL"
      }
    ],
    "ok": false,
    "rules": [
      "SYNTAX",
      "LEAKY_IMPORT",
      "FUTURE_INDEX",
      "SHIFT_NEGATIVE",
      "CONVOLVE_MODE_SAME_AST",
      "SEEDLESS_SPLIT",
      "TARGET_IN_FEATURES"
    ],
    "schema": "dino.scan.leakage.v1"
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 1

---

## capsule (pack: proof)

### `dino capsule run --command echo capsule_e2e --output-dir /tmp/dino_cli_e2e/capsule`

```bash
dino capsule run --command echo capsule_e2e --output-dir /tmp/dino_cli_e2e/capsule
```

```json
{
  "command": "run",
  "domain": "capsule",
  "result": {
    "capsule_hash": "95959a23f94b95eabbf5bbcea70bd2a274e40cdc8c8033913f65c8f3471b5569",
    "exec_ok": true,
    "exit_code": 0,
    "hash_ok": true,
    "output_dir": "/tmp/dino_cli_e2e/capsule",
    "replay_ok": true,
    "stderr_bytes": 0,
    "stdout_bytes": 12
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino capsule replay --capsule /tmp/dino_cli_e2e/capsule/capsule.json --output-dir /tmp/dino_cli_e2e/capsule_replay`

```bash
dino capsule replay --capsule /tmp/dino_cli_e2e/capsule/capsule.json --output-dir /tmp/dino_cli_e2e/capsule_replay
```

```json
{
  "command": "replay",
  "domain": "capsule",
  "result": {
    "capsule": {
      "capsule_hash": "95959a23f94b95eabbf5bbcea70bd2a274e40cdc8c8033913f65c8f3471b5569",
      "command": [
        "echo",
        "capsule_e2e"
      ],
      "env": {},
      "exit_code": 0,
      "extra": {},
      "output": "capsule_e2e\n",
      "schema": "dino.capsule.capsule.v1",
      "stderr": "",
      "stdin": ""
    },
    "exec_ok": true,
    "expected_hash": "95959a23f94b95eabbf5bbcea70bd2a274e40cdc8c8033913f65c8f3471b5569",
    "hash_ok": true,
    "live": {
      "exit_code": 0,
      "stderr": "",
      "stdout": "capsule_e2e\n"
    },
    "recomputed_hash": "95959a23f94b95eabbf5bbcea70bd2a274e40cdc8c8033913f65c8f3471b5569",
    "replay_ok": true,
    "schema": "dino.capsule.replay.v1"
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino capsule doctor --output-dir /tmp/dino_cli_e2e/capsule_doctor`

```bash
dino capsule doctor --output-dir /tmp/dino_cli_e2e/capsule_doctor
```

```json
{
  "command": "doctor",
  "domain": "capsule",
  "result": {
    "checks": [
      {
        "check": "python_major_minor",
        "detail": "3.12",
        "passed": true
      },
      {
        "check": "capsule_schema",
        "detail": "dino.capsule.capsule.v1",
        "passed": true
      },
      {
        "check": "replay_symmetry",
        "detail": "7392cbdf9866e63c",
        "passed": true
      },
      {
        "check": "exec_capture",
        "detail": "'ok\\n'",
        "passed": true
      },
      {
        "check": "output_writable",
        "detail": "/tmp/dino_cli_e2e/capsule_doctor",
        "passed": true
      },
      {
        "check": "seal_roundtrip",
        "detail": "cbf5a596b0b8736f",
        "passed": true
      }
    ],
    "ok": true,
    "output_dir": "/tmp/dino_cli_e2e/capsule_doctor",
    "report_hash": "29846eef2d4dcc1e98b2aad515925af235c5a8c4f06b74bfdc697b9f33742aee",
    "schema": "dino.capsule.doctor.v1"
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

---

## map (pack: proof)

### `dino map analyze dino/common`

```bash
dino map analyze dino/common
```

```json
{
  "command": "analyze",
  "domain": "map",
  "result": {
    "graph": {
      "edge_count": 4,
      "edges": [
        {
          "from": "__init__",
          "to": "determinism"
        },
        {
          "from": "__init__",
          "to": "errors"
        },
        {
          "from": "__init__",
          "to": "paths"
        },
        {
          "from": "__init__",
          "to": "utils"
        }
      ],
      "graph_hash": "5cae106cf0936032bbf9a900d48f790aebdbf330affed7246aeb0ad277be620f",
      "node_count": 7,
      "nodes": [
        {
          "id": "__init__",
          "imports": [
            "determinism",
            "errors",
            "paths",
            "utils"
          ],
          "path": "__init__.py"
        },
        {
          "id": "determinism",
          "imports": [
            "__future__",
            "hashlib",
            "json",
            "os",
            "typing"
          ],
          "path": "determinism.py"
        },
        {
          "id": "domain_self_test",
          "imports": [
            "__future__",
            "dino",
            "json",
            "pathlib",
            "shutil",
            "sys",
            "tempfile",
            "typing"
          ],
          "path": "domain_self_test.py"
        },
        {
          "id": "errors",
          "imports": [
            "__future__"
          ],
          "path": "errors.py"
        },
        {
          "id": "output",
          "imports": [
            "__future__",
            "dataclasses",
            "dino",
            "json",
            "sys",
            "typing"
          ],
          "path": "output.py"
        },
        {
          "id": "paths",
          "imports": [
            "__future__",
            "pathlib"
          ],
          "path": "paths.py"
        },
        {
          "id": "utils",
          "imports": [
            "__future__",
            "json",
            "pathlib",
            "typing"
          ],
          "path": "utils.py"
        }
      ],
      "root": "dino/common",
      "schema": "dino.map.graph.v1"
    },
    "plan": {
      "blocked_cycles": [],
      "complete": true,
      "schema": "dino.map.plan.v1",
      "steps": [
        "__init__",
        "determinism",
        "domain_self_test",
        "errors",
        "output",
        "paths",
        "utils"
      ]
    }
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino map verify --repo dino/common`

```bash
dino map verify --repo dino/common
```

```json
{
  "command": "verify",
  "domain": "map",
  "result": {
    "cycles": [],
    "drift": null,
    "drift_bucket": "stable",
    "edge_count": 4,
    "graph_hash": "5cae106cf0936032bbf9a900d48f790aebdbf330affed7246aeb0ad277be620f",
    "kernel_contract_details": {
      "reason": "embedded",
      "skipped": false
    },
    "max_fanout": 8,
    "node_count": 7,
    "overall_quality_score": 0.914143,
    "plan": {
      "complete": true,
      "steps": [
        "__init__",
        "determinism",
        "domain_self_test",
        "errors",
        "output",
        "paths",
        "utils"
      ]
    },
    "plan_complete": true,
    "schema": "dino.map.verify.v1",
    "score_inputs": {
      "completeness": 1.0,
      "connectivity": 0.571429,
      "cycle_penalty": 0.0,
      "determinism": 1.0,
      "drift": 1.0,
      "size": 0.14
    }
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino map plan dino/common`

```bash
dino map plan dino/common
```

```json
{
  "command": "plan",
  "domain": "map",
  "result": {
    "blocked_cycles": [],
    "complete": true,
    "schema": "dino.map.plan.v1",
    "steps": [
      "__init__",
      "determinism",
      "domain_self_test",
      "errors",
      "output",
      "paths",
      "utils"
    ]
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino map drift tests/dino/fixtures/map/repo_small --baseline tests/dino/fixtures/map/repo_clean`

```bash
dino map drift tests/dino/fixtures/map/repo_small --baseline tests/dino/fixtures/map/repo_clean
```

```json
{
  "command": "drift",
  "domain": "map",
  "result": {
    "added_edges": [
      "a->b"
    ],
    "added_nodes": [
      "a",
      "b"
    ],
    "baseline_hash": "07a64f9ce6eeeb3242a861ffbbd76499d2d20eda44f1c2188cf886bb2aa32932",
    "bucket": "controlled_drift",
    "current_hash": "3a1a0fda0d2b60ac50a000ca73578c13c7ee882f6750866ff80f1b3a9cfbf5c3",
    "distance": 4,
    "removed_edges": [],
    "removed_nodes": [
      "main"
    ],
    "schema": "dino.map.drift.v1",
    "tau": 5
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

---

## bundle (pack: proof)

### `dino bundle create --rundata tests/dino/fixtures/bundle/rundata.json --output /tmp/dino_cli_e2e/bundle.json`

```bash
dino bundle create --rundata tests/dino/fixtures/bundle/rundata.json --output /tmp/dino_cli_e2e/bundle.json
```

```json
{
  "command": "create",
  "domain": "bundle",
  "result": {
    "bytes": 568,
    "output": "/tmp/dino_cli_e2e/bundle.json",
    "status": "ok"
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino bundle verify --baseline tests/dino/fixtures/bundle/baseline_counts.json --current tests/dino/fixtures/bundle/current_counts.json`

```bash
dino bundle verify --baseline tests/dino/fixtures/bundle/baseline_counts.json --current tests/dino/fixtures/bundle/current_counts.json
```

```json
{
  "command": "verify",
  "domain": "bundle",
  "result": {
    "audit": {
      "reasons": [
        "true_delta=1",
        "endpoint_ratio=1.0"
      ],
      "summary": "Baseline met (true_count and endpoint coverage).",
      "verdict": "BUNDLE_REGRESSION_PASSED"
    },
    "baseline": {
      "dual_session_diffs": 0,
      "endpoint_count": 2,
      "evidence_summary": {},
      "mutation_count": 0,
      "phi_summary": {},
      "psi_summary": {},
      "target_id": "lab",
      "true_count": 3,
      "verified_count": 5,
      "xhr_count": 1
    },
    "current": {
      "dual_session_diffs": 0,
      "endpoint_count": 2,
      "evidence_summary": {},
      "mutation_count": 0,
      "phi_summary": {},
      "psi_summary": {},
      "target_id": "lab",
      "true_count": 4,
      "verified_count": 6,
      "xhr_count": 1
    },
    "endpoint_delta": 0,
    "endpoint_ratio": 1.0,
    "passed": true,
    "schema": "dino.bundle.regression.v1",
    "true_delta": 1
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino bundle verify --baseline tests/dino/fixtures/bundle/baseline_counts.json --current /tmp/dino_cli_e2e/bad.json`

```bash
dino bundle verify --baseline tests/dino/fixtures/bundle/baseline_counts.json --current /tmp/dino_cli_e2e/bad.json
```

```json
{
  "command": "verify",
  "domain": "bundle",
  "result": {
    "audit": {
      "reasons": [
        "true_delta=-2",
        "endpoint_ratio=0.5"
      ],
      "summary": "Regression: true_count or endpoint coverage below baseline.",
      "verdict": "BUNDLE_REGRESSION_FAILED"
    },
    "baseline": {
      "dual_session_diffs": 0,
      "endpoint_count": 2,
      "evidence_summary": {},
      "mutation_count": 0,
      "phi_summary": {},
      "psi_summary": {},
      "target_id": "lab",
      "true_count": 3,
      "verified_count": 5,
      "xhr_count": 1
    },
    "current": {
      "dual_session_diffs": 0,
      "endpoint_count": 1,
      "evidence_summary": {},
      "mutation_count": 0,
      "phi_summary": {},
      "psi_summary": {},
      "target_id": "lab",
      "true_count": 1,
      "verified_count": 0,
      "xhr_count": 0
    },
    "endpoint_delta": -1,
    "endpoint_ratio": 0.5,
    "passed": false,
    "schema": "dino.bundle.regression.v1",
    "true_delta": -2
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 1

### `dino bundle diff --baseline tests/dino/fixtures/bundle/baseline_counts.json --current /tmp/dino_cli_e2e/bad.json`

```bash
dino bundle diff --baseline tests/dino/fixtures/bundle/baseline_counts.json --current /tmp/dino_cli_e2e/bad.json
```

```json
{
  "command": "diff",
  "domain": "bundle",
  "result": {
    "audit": {
      "reasons": [
        "true_delta=-2",
        "endpoint_ratio=0.5"
      ],
      "summary": "Regression: true_count or endpoint coverage below baseline.",
      "verdict": "BUNDLE_REGRESSION_FAILED"
    },
    "baseline": {
      "dual_session_diffs": 0,
      "endpoint_count": 2,
      "evidence_summary": {},
      "mutation_count": 0,
      "phi_summary": {},
      "psi_summary": {},
      "target_id": "lab",
      "true_count": 3,
      "verified_count": 5,
      "xhr_count": 1
    },
    "current": {
      "dual_session_diffs": 0,
      "endpoint_count": 1,
      "evidence_summary": {},
      "mutation_count": 0,
      "phi_summary": {},
      "psi_summary": {},
      "target_id": "lab",
      "true_count": 1,
      "verified_count": 0,
      "xhr_count": 0
    },
    "endpoint_delta": -1,
    "endpoint_ratio": 0.5,
    "passed": false,
    "schema": "dino.bundle.regression.v1",
    "true_delta": -2
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino bundle archive --path /tmp/dino_cli_e2e/archive`

```bash
dino bundle archive --path /tmp/dino_cli_e2e/archive
```

```json
{
  "command": "archive",
  "domain": "bundle",
  "result": {
    "path": "/tmp/dino_cli_e2e/archive",
    "status": "initialized",
    "store": "archive"
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino bundle dedup --path /tmp/dino_cli_e2e/dedup.json`

```bash
dino bundle dedup --path /tmp/dino_cli_e2e/dedup.json
```

```json
{
  "command": "dedup",
  "domain": "bundle",
  "result": {
    "path": "/tmp/dino_cli_e2e/dedup.json",
    "status": "initialized",
    "store": "dedup"
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino bundle replay --baseline tests/dino/fixtures/bundle/baseline_counts.json --current tests/dino/fixtures/bundle/current_counts.json`

```bash
dino bundle replay --baseline tests/dino/fixtures/bundle/baseline_counts.json --current tests/dino/fixtures/bundle/current_counts.json
```

```json
{
  "command": "replay",
  "domain": "bundle",
  "result": {
    "audit": {
      "reasons": [
        "true_delta=1",
        "endpoint_ratio=1.0"
      ],
      "summary": "Baseline met (true_count and endpoint coverage).",
      "verdict": "BUNDLE_REGRESSION_PASSED"
    },
    "baseline": {
      "dual_session_diffs": 0,
      "endpoint_count": 2,
      "evidence_summary": {},
      "mutation_count": 0,
      "phi_summary": {},
      "psi_summary": {},
      "target_id": "lab",
      "true_count": 3,
      "verified_count": 5,
      "xhr_count": 1
    },
    "current": {
      "dual_session_diffs": 0,
      "endpoint_count": 2,
      "evidence_summary": {},
      "mutation_count": 0,
      "phi_summary": {},
      "psi_summary": {},
      "target_id": "lab",
      "true_count": 4,
      "verified_count": 6,
      "xhr_count": 1
    },
    "endpoint_delta": 0,
    "endpoint_ratio": 1.0,
    "passed": true,
    "schema": "dino.bundle.regression.v1",
    "true_delta": 1
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

---

## flight (pack: proof)

### `dino flight summary --artifacts-dir tests/dino/fixtures/flight/artifacts --output /tmp/dino_cli_e2e/flight.json`

```bash
dino flight summary --artifacts-dir tests/dino/fixtures/flight/artifacts --output /tmp/dino_cli_e2e/flight.json
```

```json
{
  "command": "summary",
  "domain": "flight",
  "result": {
    "avg_flakiness_score": 0.54,
    "best_flakiness_score": 0.8500000000000001,
    "best_record": "engine_j_canary_07.json",
    "hash_change_events": 0,
    "most_unstable_payload_fields": {
      "b": 4
    },
    "records": 10,
    "runtime_delta_ratio_max": 0.07,
    "runtime_delta_ratio_min": 0.0,
    "stable_since_runs": 0,
    "trend": [
      {
        "file": "engine_j_canary_08.json",
        "flakiness_score": 0.0,
        "run_count": 0,
        "runtime_delta_ratio_first_second": 0.0,
        "strict_mode": false,
        "timestamp": ""
      },
      {
        "file": "engine_j_canary_09.json",
        "flakiness_score": 0.0,
        "run_count": 0,
        "runtime_delta_ratio_first_second": 0.0,
        "strict_mode": false,
        "timestamp": ""
      },
      {
        "file": "engine_j_canary_00.json",
        "flakiness_score": 0.5,
        "run_count": 2,
        "runtime_delta_ratio_first_second": 0.0,
        "strict_mode": false,
        "timestamp": "2024-01-01T00:00:00Z"
      },
      {
        "file": "engine_j_canary_01.json",
        "flakiness_score": 0.55,
        "run_count": 2,
        "runtime_delta_ratio_first_second": 0.01,
        "strict_mode": false,
        "timestamp": "2024-01-02T00:00:00Z"
      },
      {
        "file": "engine_j_canary_02.json",
        "flakiness_score": 0.6,
        "run_count": 2,
        "runtime_delta_ratio_first_second": 0.02,
        "strict_mode": false,
        "timestamp": "2024-01-03T00:00:00Z"
      },
      {
        "file": "engine_j_canary_03.json",
        "flakiness_score": 0.65,
        "run_count": 2,
        "runtime_delta_ratio_first_second": 0.03,
        "strict_mode": false,
        "timestamp": "2024-01-04T00:00:00Z"
      },
      {
        "file": "engine_j_canary_04.json",
        "flakiness_score": 0.7,
        "run_count": 2,
        "runtime_delta_ratio_first_second": 0.04,
        "strict_mode": false,
        "timestamp": "2024-01-05T00:00:00Z"
      },
      {
        "file": "engine_j_canary_05.json",
        "flakiness_score": 0.75,
        "run_count": 2,
        "runtime_delta_ratio_first_second": 0.05,
        "strict_mode": false,
        "timestamp": "2024-01-06T00:00:00Z"
      },
      {
        "file": "engine_j_canary_06.json",
        "flakiness_score": 0.8,
        "run_count": 2,
        "runtime_delta_ratio_first_second": 0.06,
        "strict_mode": false,
        "timestamp": "2024-01-07T00:00:00Z"
      },
      {
        "file": "engine_j_canary_07.json",
        "flakiness_score": 0.8500000000000001,
        "run_count": 2,
        "runtime_delta_ratio_first_second": 0.07,
        "strict_mode": false,
        "timestamp": "2024-01-08T00:00:00Z"
      }
    ],
    "worst_flakiness_score": 0.0,
    "worst_record": "engine_j_canary_08.json"
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

---

## verify (pack: proof)

### `dino verify drift --distance 0`

```bash
dino verify drift --distance 0
```

```json
{
  "command": "drift",
  "domain": "verify",
  "result": {
    "bucket": "aligned",
    "distance": 0,
    "tau": 5
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino verify drift --distance 3 --tau 5`

```bash
dino verify drift --distance 3 --tau 5
```

```json
{
  "command": "drift",
  "domain": "verify",
  "result": {
    "bucket": "controlled_drift",
    "distance": 3,
    "tau": 5
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino verify drift --distance 12 --tau 5`

```bash
dino verify drift --distance 12 --tau 5
```

```json
{
  "command": "drift",
  "domain": "verify",
  "result": {
    "bucket": "severe_drift",
    "distance": 12,
    "tau": 5
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino verify drift --distance 0 --graph-truth engine_synthetic`

```bash
dino verify drift --distance 0 --graph-truth engine_synthetic
```

```json
{
  "command": "drift",
  "domain": "verify",
  "result": {
    "bucket": "synthetic_world",
    "distance": 0,
    "tau": 5
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino verify supersede --runtime-verdict REJECTED --release-verdict APPROVED --contract tests/dino/fixtures/verify/contract_release.json --previous tests/dino/fixtures/verify/contract_previous.json`

```bash
dino verify supersede --runtime-verdict REJECTED --release-verdict APPROVED --contract tests/dino/fixtures/verify/contract_release.json --previous tests/dino/fixtures/verify/contract_previous.json
```

```json
{
  "command": "supersede",
  "domain": "verify",
  "result": {
    "chain_detail": "ok",
    "chain_ok": true,
    "decision": {
      "decision_id": "release-1",
      "revision": 1,
      "runtime_supersedes": true,
      "supersedes": "release-0",
      "verdict": "APPROVED"
    },
    "runtime_exposure": {
      "runtime_supersedes": true
    }
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino verify attest tests/dino/fixtures/verify/valid_attest.json --trust-anchor tests/dino/fixtures/verify/trust_anchor.json`

```bash
dino verify attest tests/dino/fixtures/verify/valid_attest.json --trust-anchor tests/dino/fixtures/verify/trust_anchor.json
```

```json
{
  "command": "attest",
  "domain": "verify",
  "result": {
    "anchor": {
      "errors": [],
      "ok": true
    },
    "passed": true,
    "pipeline_hash": {
      "ok": true,
      "value": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    },
    "signature": {
      "detail": "preimage hash bound",
      "ok": true
    },
    "verdict": "VERIFIED"
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino verify binary tests/dino/fixtures/verify/valid_attest.json`

```bash
dino verify binary tests/dino/fixtures/verify/valid_attest.json
```

```json
{
  "command": "binary",
  "domain": "verify",
  "result": {
    "checks": [
      {
        "check": "H_verdict_present",
        "detail": "ffffffffffffffff",
        "passed": true
      },
      {
        "check": "compiler_graph_hash_present",
        "detail": "dddddddddddddddd",
        "passed": true
      },
      {
        "check": "pipeline_hash_present",
        "detail": "aaaaaaaaaaaaaaaa",
        "passed": true
      },
      {
        "check": "policy_verdict_hash_present",
        "detail": "2222222222222222",
        "passed": true
      },
      {
        "check": "compiler_graph_hash_replay",
        "detail": "recomputed=fc29a90da274d30c expected=dddddddddddddddd",
        "passed": false
      },
      {
        "check": "transparency_log",
        "detail": "transparency_log_optional",
        "passed": true
      }
    ],
    "compiler_binary": "stdlib_embedded",
    "edge_count": 0,
    "hashes": {
      "H_verdict": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
      "compiler_graph_hash": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
      "pipeline_hash": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "policy_verdict_hash": "2222222222222222222222222222222222222222222222222222222222222222"
    },
    "node_count": 423,
    "passed": false,
    "recomputed_compiler_graph_hash": "fc29a90da274d30ca706f5de97f4cd973c3642cd0ee48aeb2374f01dca306746",
    "repo": "/home/noahp/DevKit_Collected/devsecops",
    "schema_id": "dino_verify_binary_v1",
    "verdict": "FAIL",
    "verify_hash": "17456d6e68352c4d304062b009b6d59767fba6896a1b35601e26a67ea4f770a9",
    "version": "1.0.0"
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 1

---

## proof (pack: proof)

### `dino proof doctor --output-dir /tmp/dino_cli_e2e/proof_doctor`

```bash
dino proof doctor --output-dir /tmp/dino_cli_e2e/proof_doctor
```

```json
{
  "command": "doctor",
  "domain": "proof",
  "result": {
    "active_packs": [
      "free",
      "proof"
    ],
    "audit": {
      "reasons": [
        "all_passed"
      ],
      "summary": "Proof stack healthy.",
      "verdict": "PROOF_DOCTOR_PASSED"
    },
    "checks": [
      {
        "check": "python_major_minor",
        "detail": "3.12",
        "passed": true
      },
      {
        "check": "proof_schema",
        "detail": "dino.proof.bundle.v1",
        "passed": true
      },
      {
        "check": "scan_grammar",
        "detail": "ALPHA_GRAMMAR_V1",
        "passed": true
      },
      {
        "check": "drift_aligned",
        "detail": "distance=0",
        "passed": true
      },
      {
        "check": "map_verify",
        "detail": "0.914143",
        "passed": true
      },
      {
        "check": "license_packs",
        "detail": "free,proof",
        "passed": true
      },
      {
        "check": "pack_proof_domains",
        "detail": "proof=True",
        "passed": true
      },
      {
        "check": "capsule_seal",
        "detail": "cbf5a596b0b8736f",
        "passed": true
      },
      {
        "check": "proof_run",
        "detail": "partial",
        "passed": true
      },
      {
        "check": "proof_verify",
        "detail": "PROOF_VERIFY_PASSED",
        "passed": true
      }
    ],
    "domains": {
      "bundle": true,
      "capsule": true,
      "flight": true,
      "map": true,
      "proof": true,
      "scan": true,
      "verify": true
    },
    "ok": true,
    "output_dir": "/tmp/dino_cli_e2e/proof_doctor",
    "report_hash": "57344618554911aa13f290450cad1b916aa5ef18ade5b5f786b88d5fb0fb8eff",
    "schema": "dino.proof.doctor.v1",
    "status": "passed"
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino proof run --command echo proof_e2e --repo dino/common --scan tests/dino/fixtures/scan/clean_code.py --output-dir /tmp/dino_cli_e2e/proof`

```bash
dino proof run --command echo proof_e2e --repo dino/common --scan tests/dino/fixtures/scan/clean_code.py --output-dir /tmp/dino_cli_e2e/proof
```

```json
{
  "command": "run",
  "domain": "proof",
  "result": {
    "artifacts": {
      "capsule": "capsule/capsule.json",
      "map_verify": "map_verify.json",
      "scan": "scan.json"
    },
    "audit": {
      "reasons": [
        "capsule_sealed",
        "scan_clean",
        "map_scored"
      ],
      "summary": "All requested proof parts succeeded.",
      "verdict": "PROOF_PASSED"
    },
    "command": [
      "echo",
      "proof_e2e"
    ],
    "ok": true,
    "output_dir": "/tmp/dino_cli_e2e/proof",
    "parts": {
      "capsule_hash": "cdb859b064f4b761218adc4d1ebd6044b25282413defd32436cf6ec33eac09cb",
      "capsule_replay_ok": true,
      "drift_bucket": "aligned",
      "map_graph_hash": "5cae106cf0936032bbf9a900d48f790aebdbf330affed7246aeb0ad277be620f",
      "map_score": 0.914143,
      "scan_ok": true
    },
    "proof_hash": "30fe74e8e3da87477f3de3bb5092642126625a5e2dcb29bd2223a70f034e1bc1",
    "schema": "dino.proof.bundle.v1",
    "schemas": {
      "capsule": "dino.capsule.capsule.v1",
      "drift": "dino.verify.drift_class.v1",
      "map": "dino.map.verify.v1",
      "proof": "dino.proof.bundle.v1",
      "scan": "dino.scan.leakage.v1"
    },
    "status": "passed"
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

### `dino proof verify --proof /tmp/dino_cli_e2e/proof/proof.json`

```bash
dino proof verify --proof /tmp/dino_cli_e2e/proof/proof.json
```

```json
{
  "command": "verify",
  "domain": "proof",
  "result": {
    "audit": {
      "reasons": [
        "verify_ok"
      ],
      "summary": "Proof hash and capsule re-exec verified.",
      "verdict": "PROOF_VERIFY_PASSED"
    },
    "capsule": {
      "capsule": {
        "capsule_hash": "cdb859b064f4b761218adc4d1ebd6044b25282413defd32436cf6ec33eac09cb",
        "command": [
          "echo",
          "proof_e2e"
        ],
        "env": {},
        "exit_code": 0,
        "extra": {},
        "output": "proof_e2e\n",
        "schema": "dino.capsule.capsule.v1",
        "stderr": "",
        "stdin": ""
      },
      "exec_ok": true,
      "expected_hash": "cdb859b064f4b761218adc4d1ebd6044b25282413defd32436cf6ec33eac09cb",
      "hash_ok": true,
      "live": {
        "exit_code": 0,
        "stderr": "",
        "stdout": "proof_e2e\n"
      },
      "recomputed_hash": "cdb859b064f4b761218adc4d1ebd6044b25282413defd32436cf6ec33eac09cb",
      "replay_ok": true,
      "schema": "dino.capsule.replay.v1"
    },
    "capsule_replay_ok": true,
    "expected_proof_hash": "30fe74e8e3da87477f3de3bb5092642126625a5e2dcb29bd2223a70f034e1bc1",
    "ok": true,
    "proof_hash_ok": true,
    "proof_schema_ok": true,
    "recomputed_proof_hash": "30fe74e8e3da87477f3de3bb5092642126625a5e2dcb29bd2223a70f034e1bc1",
    "schema": "dino.proof.verify.v1",
    "schemas": {
      "capsule": "dino.capsule.capsule.v1",
      "drift": "dino.verify.drift_class.v1",
      "map": "dino.map.verify.v1",
      "proof": "dino.proof.bundle.v1",
      "scan": "dino.scan.leakage.v1"
    },
    "status": "passed"
  },
  "timestamp": null,
  "version": "0.3.0"
}
```

**exit:** 0

---

## Test-Suite

```bash
pytest tests/dino -q
```

```
........................................................................ [ 76%]
......................                                                   [100%]
```

**exit:** 0

---

## Zusammenfassung Exit-Codes (dieser Lauf)

| Befehl | exit |
|--------|------|
| scan grammar / clean | 0 |
| scan leakage (findings) | 1 |
| capsule * / map * / bundle PASS / flight / verify drift+supersede+attest / proof * | 0 |
| bundle verify FAIL | 1 |
| verify binary (Fixture ≠ Live-Repo) | 1 |
| pytest tests/dino | 0 |
