# Dino Proof Contract

**Status:** Normative · **Schema:** `dino.proof.bundle.v1` · **CLI:** `dino` ≥ 0.3.0  
**Audience:** Customers, auditors, integrators

This document is the public contract for what a Dino proof *is*, what Dino *guarantees*, and what it *does not*.

---

## 1. Purpose

Dino proves **logic & data integrity** of a run — not supply-chain identity of an image, and not secret presence in a repo.

| Layer | Typical tools | Dino |
|-------|---------------|------|
| Image / binary provenance | Docker, Cosign, Sigstore | **Out of scope** |
| Secrets / generic SAST | gitleaks, Semgrep | **Out of scope** (except research-leakage niche in `scan`) |
| Sealed command execution | ad-hoc scripts | **In scope** (`capsule`) |
| Structural repo IR + drift | — | **In scope** (`map`) |
| Causal / leakage integrity | — | **In scope** (`scan`) |
| Governance vocabulary | — | **In scope** (`verify` drift/supersede) |
| End-to-end evidence object | — | **In scope** (`proof.json`) |

**One-line product promise**

> *Sigstore proves the artifact came from you. Dino proves the decision / feature run was the same sealed logic.*

---

## 2. Proof object (`proof.json`)

### 2.1 Required top-level fields

| Field | Type | Notes |
|-------|------|--------|
| `schema` | string | Must be `dino.proof.bundle.v1` |
| `schemas` | object | Nested schema IDs (see §2.2) |
| `command` | string[] | Exact argv sealed into the capsule |
| `parts` | object | Aggregated results (see §2.3) |
| `artifacts` | object | **Relative** paths under `output_dir` |
| `proof_hash` | string | SHA-256 of canonical JSON of the body (§5) |
| `ok` | bool | `true` iff status is `passed` or `partial` |
| `status` | enum | `passed` \| `partial` \| `failed` |
| `audit` | object | Human/CI audit block (§6) |
| `output_dir` | string | Absolute path; **excluded** from `proof_hash` |

### 2.2 `schemas` block (versioning)

```json
"schemas": {
  "proof": "dino.proof.bundle.v1",
  "capsule": "dino.capsule.capsule.v1",
  "scan": "dino.scan.leakage.v1",
  "map": "dino.map.verify.v1",
  "drift": "dino.verify.drift_class.v1"
}
```

Absent optional parts still list the schema ID Dino *would* emit. Consumers MUST reject unknown `schemas.proof` majors.

### 2.3 `parts`

| Field | When set | Meaning |
|-------|----------|---------|
| `capsule_hash` | always | Content hash of sealed capsule |
| `capsule_replay_ok` | always | Hash + re-exec matched |
| `scan_ok` | if `--scan` | `true` iff no FAIL findings |
| `map_score` | if `--repo` | `overall_quality_score` from map verify |
| `map_graph_hash` | if `--repo` | Structural graph hash |
| `drift_bucket` | always | Drift class (§8); default `aligned` if no map drift |

`null` means **not requested** (partial), not failure.

### 2.4 `artifacts` (relative)

```json
"artifacts": {
  "capsule": "capsule/capsule.json",
  "scan": "scan.json" | null,
  "map_verify": "map_verify.json" | null
}
```

Resolving: `Path(output_dir) / artifacts.capsule`.

### 2.5 Minimal valid example

```json
{
  "schema": "dino.proof.bundle.v1",
  "schemas": {
    "proof": "dino.proof.bundle.v1",
    "capsule": "dino.capsule.capsule.v1",
    "scan": "dino.scan.leakage.v1",
    "map": "dino.map.verify.v1",
    "drift": "dino.verify.drift_class.v1"
  },
  "command": ["echo", "ok"],
  "parts": {
    "capsule_hash": "…",
    "capsule_replay_ok": true,
    "scan_ok": null,
    "map_score": null,
    "map_graph_hash": null,
    "drift_bucket": "aligned"
  },
  "artifacts": {
    "capsule": "capsule/capsule.json",
    "scan": null,
    "map_verify": null
  },
  "status": "partial",
  "ok": true,
  "audit": {
    "verdict": "PROOF_PARTIAL",
    "summary": "Capsule sealed; scan and map not requested.",
    "reasons": ["scan_skipped", "map_skipped"]
  },
  "proof_hash": "…"
}
```

---

## 3. Status & exit codes

### 3.1 Status

| Status | `ok` | Meaning |
|--------|------|---------|
| `passed` | true | Capsule sealed; every *requested* part succeeded |
| `partial` | true | Capsule sealed; one or more optional parts skipped |
| `failed` | false | Capsule failed, or a requested part failed |

### 3.2 CLI exit codes (`dino proof run` / `verify`)

| Code | Meaning |
|------|---------|
| `0` | `passed` or `partial` |
| `1` | `failed` (proof or verify) |
| `2` | Usage / missing file / pack locked |

---

## 4. Guarantees

### 4.1 What Dino **does** guarantee (when `status` ∈ {passed, partial} and verify succeeds)

1. **Capsule content-addressing** — `capsule_hash` is SHA-256 over the canonical capsule body (command, stdin, sealed env, stdout, stderr, exit_code, extra).
2. **Replay integrity** — Recomputing the hash and **re-executing** the command yields the same stdout, stderr, and exit_code (`hash_ok` ∧ `exec_ok`).
3. **Deterministic JSON** — Domain payloads use sorted keys / stable separators; CLI `--json` envelopes set `timestamp: null`.
4. **Drift vocabulary** — `drift_bucket` is one of the fixed classes in §8.
5. **Proof hash binding** — `proof_hash` binds `schema`, `schemas`, `command`, `parts`, `artifacts`, `status`, `audit` (not `output_dir`, not `ok` if duplicated — see §5).
6. **Scan FAIL semantics** — If `--scan` was requested and findings with severity FAIL exist, proof `status` is `failed`.

### 4.2 What Dino **does not** guarantee

1. Cryptographic signature of the proof by an HSM / Sigstore (attest is hash-bound trust surface, not full PKI).
2. Bit-identical runs across different OSes if the sealed *command* itself is non-deterministic.
3. Completeness of leakage detection (rules are finite; evasion is possible).
4. That ambient host env was frozen — only an explicit capsule `env` plus a minimal PATH/LANG seal for execution.
5. Non-Python semantic equivalence (map is Python AST import graph).
6. That skipped parts (`scan_ok: null`) were safe — partial means unchecked, not clean.

---

## 5. Determinism

### 5.1 Deterministic by contract

- `canonical_hash` / `canonical_dumps` (`dino.common.determinism`)
- Capsule fields listed in §4.1
- Map graph node/edge ordering
- Drift classification from `(distance, tau, graph_truth)`
- `proof_hash` over the hashed body
- CLI JSON envelopes (`timestamp: null`)

### 5.2 Not deterministic by contract

- Wall-clock, PIDs, absolute `output_dir`
- Command side effects outside captured stdout/stderr/exit
- Map scores on changing trees
- Flight summaries over changing canary dirs
- Binary verify against a repo that changed since attestation

### 5.3 `proof_hash` algorithm

1. Take proof object.  
2. Drop keys: `proof_hash`, `ok`, `output_dir`.  
3. `canonical_dumps` → UTF-8 → SHA-256 hex.

`dino proof verify` recomputes this and re-executes the capsule.

---

## 6. Audit UX (Proof as audit event)

Every `proof run` / `proof verify` result includes:

```json
"audit": {
  "verdict": "PROOF_PASSED" | "PROOF_PARTIAL" | "PROOF_FAILED" | "PROOF_VERIFY_PASSED" | "PROOF_VERIFY_FAILED",
  "summary": "<one sentence>",
  "reasons": ["machine_reason", ...]
}
```

### 6.1 Reason codes (`proof run`)

| Code | Meaning |
|------|---------|
| `capsule_sealed` | Capsule replay_ok |
| `capsule_failed` | Capsule hash or re-exec failed |
| `scan_clean` | Scan requested and ok |
| `scan_failed` | Scan requested and not ok |
| `scan_skipped` | No `--scan` |
| `map_scored` | Map verify produced a score |
| `map_skipped` | No `--repo` |
| `map_failed` | Repo given but verify incomplete |

Text mode prints verdict + summary as an audit banner (not a generic “Done” only).

---

## 7. Capsule contract (embedded)

Schema: `dino.capsule.capsule.v1`

| Field | Role |
|-------|------|
| `command` | argv |
| `stdin` | sealed stdin |
| `env` | explicit env map (sorted) |
| `output` | canonical stdout (`\n` normalized) |
| `stderr` | canonical stderr |
| `exit_code` | int |
| `extra` | opaque sealed bag |
| `capsule_hash` | hash of the above |

Replay: rebuild hash + re-exec; both must match.

---

## 8. Drift buckets (governance)

Shared vocabulary (`dino.verify.drift_class.v1` / map drift buckets):

| Bucket | Meaning |
|--------|---------|
| `aligned` | distance = 0 |
| `controlled_drift` | 0 < distance ≤ τ |
| `severe_drift` | distance > τ |
| `synthetic_world` | `graph_truth=engine_synthetic` |
| `unmeasured` | insufficient / distance &lt; 0 |

Default τ = 5 unless overridden.

---

## 9. Supersession vocabulary

### 9.1 Release verdicts

| Verdict | Meaning |
|---------|---------|
| `APPROVED` | Gate allowed release |
| `PASS` / `OK` | Aliases → `APPROVED` |

### 9.2 Runtime verdicts

| Verdict | Meaning |
|---------|---------|
| `ALLOW` | Runtime confirms release |
| `WARN` | Runtime soft override |
| `DENY` | Runtime hard override |
| `REJECTED` / `BLOCK` / `FAIL` / `DENIED` | Aliases → `DENY` |

### 9.3 Rules

Runtime **supersedes** when:

`runtime ∈ {DENY, WARN}` ∧ `release == APPROVED` ∧ previous decision id present.

Then: `revision := previous.revision + 1`, `supersedes := previous.decision_id`, `runtime_supersedes := true`.

Chain check (`verify_supersession_chain`): revision must bump by 1; `supersedes` must match previous id.

---

## 10. Scan rules (free moat)

Schema report: `dino.scan.leakage.v1` (via `rules` list in report).

| Rule ID | Signal |
|---------|--------|
| `LEAKY_IMPORT` | forbidden `economics` imports |
| `FUTURE_INDEX` | `close|label|…[i+1]` |
| `SHIFT_NEGATIVE` | `.shift(-N)` |
| `CONVOLVE_MODE_SAME_AST` | `convolve(..., mode="same")` |
| `SEEDLESS_SPLIT` | `train_test_split` without `random_state` |
| `TARGET_IN_FEATURES` | feature matrix includes label/target |
| `SYNTAX` | parse error |

Exit: CLI `scan leakage` → `1` if any FAIL finding.

---

## 11. Bundle regression semantics

`dino bundle replay|verify --baseline B --current C`

| Result | Meaning |
|--------|---------|
| `passed: true` | `true_count(current) ≥ true_count(baseline)` ∧ endpoint_ratio ≥ 0.8 |
| `passed: false` | Regression — coverage or true-count dropped |

`true_delta` / `endpoint_delta` / `endpoint_ratio` explain *what* moved.  
A failed regression means: **the evidence baseline is no longer met**, not that the host is compromised.

`dino bundle diff` returns the same comparison payload with informational intent (exit 0) for review UIs.

---

## 12. Full proof run (reference)

```bash
dino upgrade --pack proof
dino proof doctor
dino proof run \
  --command "python3 train.py --seed 0" \
  --repo . \
  --scan ./src \
  --output-dir ./proof_out
# exit 0 + audit.verdict PROOF_PASSED|PROOF_PARTIAL
# Note: put flags inside one --command string (or argv tokens without leading --).
# If --scan paths resolve to zero .py files, scan fails (EMPTY_SCAN_ROOTS).
# dino --dev relaxes EMPTY_SCAN_ROOTS only (not for production proofs).
dino proof verify --proof ./proof_out/proof.json
# exit 0 + PROOF_VERIFY_PASSED
```

Artifacts:

```
proof_out/
  proof.json
  capsule/capsule.json
  capsule/replay.json
  scan.json          # if --scan
  map_verify.json    # if --repo
```

---

## 13. Compatibility

- **v1** is the current major. Additive optional fields are allowed.  
- Removing/renaming hashed fields or changing hash preimage is a **major** bump (`dino.proof.bundle.v2`).  
- Consumers MUST ignore unknown non-hashed advisory fields only if they do not affect `proof_hash` verification.

---

## 14. Normative references (code)

| Concern | Module |
|---------|--------|
| Proof build/verify | `dino.domains.proof.chain` |
| Capsule seal/replay | `dino.domains.capsule.*` |
| Map verify/drift | `dino.domains.map.*` |
| Scan | `dino.domains.scan.leakage` |
| Drift classes | `dino.domains.verify.drift_classifier` |
| Supersession | `dino.domains.verify.supersession_checker` |
| Bundle regression | `dino.domains.bundle.replay_baseline` |

This contract is the source of truth for launch messaging and enterprise diligence.
