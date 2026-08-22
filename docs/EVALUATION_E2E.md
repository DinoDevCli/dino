# Dino — Vollständige technische Evaluation (E2E + Proof-Contract)

**Datum:** 2026-08-22  
**Version:** `dino` 0.3.0  
**Umgebung:** Linux · Python 3.12 · Repo `/home/noahp/DevKit_Collected/devsecops`  
**Normativ:** [`PROOF_CONTRACT.md`](PROOF_CONTRACT.md)  
**Artefakte:** `/tmp/dino_eval/` (reproduzierbar)

---

## Executive Summary

| Bereich | Ergebnis | Exit / Verdict |
|---------|----------|----------------|
| **Setup + Doctor** | **PASS** | `PROOF_DOCTOR_PASSED` |
| **Capsule** | **PASS** | replay 0 · tamper 1 |
| **Scan** | **PASS** (mit Hinweisen) | 6/7 Regeln belegt · `leaky_code.py` fehlt |
| **Map** | **PASS** | plan 0 · drift `controlled_drift` |
| **Bundle** | **PASS** | PASSED exit 0 · FAILED exit 1 |
| **Verify** | **PASS** (partial) | drift/supersede OK · binary FAIL erwartet |
| **Proof E2E** | **PASS** | `PROOF_PASSED` · `PROOF_VERIFY_PASSED` |
| **Test-Suite** | **PASS** | 94 tests · 0 failed |

**Gesamturteil:** Proof-Contract-konform für den implementierten Scope. Abweichungen vom Evaluations-Script (CLI-Flags, fehlende Fixtures) sind dokumentiert — kein Produkt-Blocker.

---

## 1. Setup

```bash
cd devsecops
pip install -e '.[dev]'          # via .venv (PEP 668 auf System-Python)
.venv/bin/dino upgrade --pack proof
.venv/bin/dino proof doctor --output-dir /tmp/dino_eval/doctor
```

| Check | Ergebnis |
|-------|----------|
| Proof-Pack aktiv | `free`, `proof` |
| Doctor | `PROOF_DOCTOR_PASSED` · status `passed` |
| Checks | python 3.12, proof_schema, scan_grammar, drift_aligned, map_verify, capsule_seal, proof_run, proof_verify, pack_proof_domains |

---

## 2. Capsule — Execution Seal

### Commands (ausgeführt)

```bash
dino --json capsule run --command echo capsule_ok --output-dir /tmp/dino_eval/capsule_out
dino --json capsule replay --capsule /tmp/dino_eval/capsule_out/capsule.json --output-dir /tmp/dino_eval/capsule_replay
# Tamper-Test: output in capsule.json manuell geändert → replay erneut
```

### Ergebnis: **PASS**

| Prüfpunkt | Erwartung | Ist |
|-----------|-----------|-----|
| run exit | 0 | **0** |
| replay exit | 0 | **0** |
| `hash_ok` | true | **true** |
| `exec_ok` | true | **true** |
| `replay_ok` | true | **true** |
| stdout sealed | `capsule_ok\n` | **ja** |
| stderr / exit_code | captured | **"" / 0** |
| Schema | `dino.capsule.capsule.v1` | **ja** |
| Tamper exit | 1 | **1** |
| Tamper `hash_ok` | false | **false** |
| Tamper `exec_ok` | false | **false** (live stdout ≠ tampered) |

**Capsule-Hash (Referenz):** `59f7521870cca8f657ae1218b88f34119c4f8075b8cc6778a62bc891143503ca`

Contract-Garantie §4.1 (Capsule content-addressing + Replay integrity): **erfüllt**.

---

## 3. Scan — Causal Leakage Detection

### Commands (Eval-Script vs. Ist)

| Eval-Script | Ist (Fixture existiert / CLI) |
|-------------|-------------------------------|
| `clean_code.py` | ✅ ausgeführt |
| `leaky_code.py` | ❌ **Datei existiert nicht** → Ersatz-Fixtures unten |

```bash
dino --json scan leakage tests/dino/fixtures/alpha/clean_code.py
dino --json scan leakage tests/dino/fixtures/alpha/forbidden_import.py      # LEAKY_IMPORT
dino --json scan leakage tests/dino/fixtures/alpha/shift_and_seedless.py    # SHIFT + SEEDLESS
dino --json scan leakage tests/dino/fixtures/alpha/target_in_features.py    # TARGET_IN_FEATURES
dino --json scan leakage /tmp/dino_eval/future_convolve.py                  # FUTURE + CONVOLVE (synthetisch)
```

### Ergebnis: **PASS** (Regelabdeckung)

| Regel | Getestet | Finding | Exit |
|-------|----------|---------|------|
| `clean` (0 findings) | `clean_code.py` | 0 | 0 |
| `LEAKY_IMPORT` | `forbidden_import.py` | 1 | 1 |
| `SHIFT_NEGATIVE` | `shift_and_seedless.py` | 1 | 1 |
| `SEEDLESS_SPLIT` | `shift_and_seedless.py` | 1 | 1 |
| `TARGET_IN_FEATURES` | `target_in_features.py` | 1 | 1 |
| `FUTURE_INDEX` | `future_convolve.py` | 1 | 1 |
| `CONVOLVE_MODE_SAME_AST` | `future_convolve.py` | 1 | 1 |
| `SYNTAX` | — | nicht isoliert getestet | — |
| `leakage_code.py` | vorhanden, **0 findings** | harmlos (`closes[1:]`) | 0 |

Report-Schema: `dino.scan.leakage.v1` · Rules-Liste vollständig in Output.

**Hinweis:** Evaluations-Script sollte `leaky_code.py` anlegen oder auf `shift_and_seedless.py` / `forbidden_import.py` verweisen.

---

## 4. Map — Structural IR + Drift

### Commands (Eval-Script vs. Ist)

| Eval-Script | Ist |
|-------------|-----|
| `map plan --repo dino/common --output-dir ./map_out` | ❌ Flag existiert nicht |
| `map drift --baseline …/map/baseline_graph.json --current …` | ❌ Fixtures fehlen |

**Korrekte Commands (ausgeführt):**

```bash
dino --json map plan dino/common
dino --json map verify --repo dino/common
dino --json map drift tests/dino/fixtures/brain/repo_small \
  --baseline tests/dino/fixtures/brain/repo_clean
```

### Ergebnis: **PASS**

| Prüfpunkt | Erwartung | Ist |
|-----------|-----------|-----|
| plan exit | 0 | **0** |
| plan complete | true | **true** (7 steps) |
| verify score | present | **0.914143** |
| graph_hash | present | `5cae106c…` |
| drift bucket | korrekt vs baseline | **`controlled_drift`** (distance=4, τ=5) |
| drift schema | `dino.map.drift.v1` | **ja** |

Drift-Buckets `aligned` / `severe_drift` / `synthetic_world` zusätzlich via `verify drift` (§6) verifiziert.

---

## 5. Bundle — Regression Proof

```bash
dino --json bundle verify \
  --baseline tests/dino/fixtures/artifact/baseline_counts.json \
  --current tests/dino/fixtures/artifact/current_counts.json

# Negativfall (synthetisch):
# current: true_count=1, endpoint_count=1
```

### Ergebnis: **PASS**

| Fall | exit | verdict | passed |
|------|------|---------|--------|
| Regression OK | **0** | `BUNDLE_REGRESSION_PASSED` | true |
| Regression FAIL | **1** | `BUNDLE_REGRESSION_FAILED` | false |

Semantik: `true_delta=1`, `endpoint_ratio=1.0` (Pass) · `true_delta=-2`, `endpoint_ratio=0.5` (Fail).  
Schema: `dino.bundle.regression.v1`.

**Hinweis:** Audit-Verdicts sind `BUNDLE_REGRESSION_PASSED/FAILED`, nicht `PASSED/PARTIAL/FAILED` (Eval-Script-Wortlaut leicht abweichend).

---

## 6. Verify — Governance

### Commands (Eval-Script vs. Ist)

| Eval-Script | Ist |
|-------------|-----|
| `verify drift --repo dino/common` | ❌ `--repo` nicht unterstützt |
| `supersede --contract tests/.../supersession/contract.json` | ❌ Pfad existiert nicht |

**Ausgeführt:**

```bash
dino --json verify drift --distance 0          # aligned
dino --json verify drift --distance 3 --tau 5  # controlled_drift
dino --json verify drift --distance 12 --tau 5 # severe_drift
dino --json verify drift --distance 0 --graph-truth engine_synthetic  # synthetic_world

dino --json verify supersede \
  --runtime-verdict REJECTED --release-verdict APPROVED \
  --contract tests/dino/fixtures/attest/contract_release.json \
  --previous tests/dino/fixtures/attest/contract_previous.json

dino --json verify attest valid_attest.json --trust-anchor trust_anchor.json
dino --json verify binary valid_attest.json
```

### Ergebnis: **PASS** (Governance-Kern) · **PARTIAL** (Binary)

| Prüfpunkt | Ergebnis |
|-----------|----------|
| drift `aligned` (d=0) | ✅ |
| drift `controlled_drift` (d=3, τ=5) | ✅ |
| drift `severe_drift` (d=12) | ✅ |
| drift `synthetic_world` | ✅ |
| supersede chain | ✅ `chain_ok=true`, `runtime_supersedes=true`, `supersedes=release-0`, revision 1 |
| attest | ✅ `VERIFIED` / passed |
| binary vs Live-Repo | ⚠️ `FAIL` / passed=false (compiler_graph_hash_replay) — **erwartet** laut Contract §4.2 |

Supersession-Verdict: Runtime **DENY** (via REJECTED-Alias) überschreibt APPROVED Release — kein separates „ALLOWED/DENY“-Feld, sondern `runtime_supersedes: true/false`.

---

## 7. Proof — End-to-End Contract

```bash
dino --json proof run \
  --command echo proof_ok \
  --repo dino/common \
  --scan tests/dino/fixtures/alpha/clean_code.py \
  --output-dir /tmp/dino_eval/proof_out

dino --json proof verify --proof /tmp/dino_eval/proof_out/proof.json
```

### Ergebnis: **PASS**

| Prüfpunkt | Erwartung (Contract) | Ist |
|-----------|----------------------|-----|
| run exit | 0 | **0** |
| verify exit | 0 | **0** |
| schema | `dino.proof.bundle.v1` | **ja** |
| `schemas{}` | capsule/scan/map/drift/proof | **ja** |
| status | passed | **passed** |
| audit | PROOF_PASSED | **PROOF_PASSED** |
| proof_hash | stabil recomputable | **ok** (`proof_hash_ok=true`) |
| capsule re-exec | ok | **capsule_replay_ok=true** |

### `proof.json` Inhalt (Eval-Script-Korrektur)

Eval-Script erwartet „capsule, scan, map, drift, **bundle**, **supersession**“ in `proof.json`.

**Contract-korrekt (implementiert):**

| Teil | in `proof.json` |
|------|-----------------|
| Capsule | `parts.capsule_hash`, `parts.capsule_replay_ok`, artifact `capsule/capsule.json` |
| Scan | `parts.scan_ok`, artifact `scan.json` |
| Map | `parts.map_score`, `parts.map_graph_hash`, artifact `map_verify.json` |
| Drift | `parts.drift_bucket` |
| Bundle | **nicht** in proof run (separater Domain-Workflow) |
| Supersession | **nicht** in proof run (separater `verify supersede`) |

Artefakt-Tree:

```
/tmp/dino_eval/proof_out/
  proof.json
  capsule/capsule.json
  capsule/replay.json
  scan.json
  map_verify.json
```

**Proof-Hash (Referenz):** `e2688f276065d75c9a72276a18ea94c7a6e7d0092dc473981ab92e8a4b9246b3`

---

## 8. Test-Suite

```bash
pytest tests/dino -q
```

| Metrik | Wert |
|--------|------|
| Tests gesamt | **94** |
| Failed | **0** |
| `test_gap_closure.py` | ✅ |
| `test_proof_contract.py` (6 tests) | ✅ |

---

## 9. Abweichungsmatrix (Eval-Script → Repo)

| # | Eval-Script | Tatsächliche CLI / Fixture | Impact |
|---|-------------|----------------------------|--------|
| 1 | `leaky_code.py` | nicht vorhanden; `leakage_code.py` ist clean | Script anpassen |
| 2 | `map plan --repo --output-dir` | `map plan <path>` | Script anpassen |
| 3 | `fixtures/map/baseline_graph.json` | fehlt; `brain/repo_small` vs `repo_clean` | Script anpassen |
| 4 | `verify drift --repo` | `verify drift --distance N` | Script anpassen |
| 5 | `supersession/contract.json` | `attest/contract_release.json` + `contract_previous.json` | Script anpassen |
| 6 | proof.json enthält bundle/supersession | nicht im Contract für `proof run` | Erwartung korrigieren |
| 7 | Bundle audit „PARTIAL“ | nur PASSED/FAILED | Wortlaut |

---

## 10. Strukturierter Pass/Fail-Report

```
┌─────────────┬────────┬──────────────────────────────────────────────────┐
│ Domain      │ Status │ Detail                                           │
├─────────────┼────────┼──────────────────────────────────────────────────┤
│ Setup       │ PASS   │ proof pack · PROOF_DOCTOR_PASSED                 │
│ Capsule     │ PASS   │ hash_ok ∧ exec_ok · tamper → exit 1              │
│ Scan        │ PASS   │ 6 Regeln belegt · SYNTAX isoliert offen          │
│ Map         │ PASS   │ plan complete · controlled_drift d=4             │
│ Bundle      │ PASS   │ PASSED exit 0 · FAILED exit 1                    │
│ Verify      │ PASS*  │ drift/supersede/attest OK · binary FAIL expected │
│ Proof       │ PASS   │ PROOF_PASSED · PROOF_VERIFY_PASSED               │
│ Test-Suite  │ PASS   │ 94/94 green                                      │
└─────────────┴────────┴──────────────────────────────────────────────────┘
* Verify binary: repo-gebundener FAIL ist Contract-konform (kein Regression).
```

---

## 11. Reproduktion (Copy-Paste)

```bash
cd /home/noahp/DevKit_Collected/devsecops
.venv/bin/dino upgrade --pack proof
.venv/bin/dino proof doctor --output-dir /tmp/dino_eval/doctor
.venv/bin/dino --json capsule run --command echo capsule_ok --output-dir /tmp/dino_eval/capsule_out
.venv/bin/dino --json proof run --command echo proof_ok --repo dino/common \
  --scan tests/dino/fixtures/alpha/clean_code.py --output-dir /tmp/dino_eval/proof_out
.venv/bin/dino --json proof verify --proof /tmp/dino_eval/proof_out/proof.json
.venv/bin/pytest tests/dino -q
```

---

## 12. Fazit

Dino **0.3.0** erfüllt den **Proof-Contract** für:

- Sealed Execution (Capsule + Re-Exec)  
- Causal Leakage Scan (Free + Proof-Integration)  
- Structural Map + Drift-Buckets  
- Bundle-Regression mit Audit-Verdicts  
- Governance (Drift-Klassifikation, Supersession-Chain, Attest)  
- End-to-End `proof.json` mit `PROOF_PASSED` / `PROOF_VERIFY_PASSED`  

Die Evaluation ist **deterministisch reproduzierbar** (canonical hashes, `timestamp: null`, feste Fixtures). Offene Punkte sind **Eval-Script-Drift** (falsche CLI-Flags/Fixtures), nicht Produktdefekte.

**Nächster Schritt (GTM):** [`ICP_TEST.md`](ICP_TEST.md) ausführen — technische Evaluation abgeschlossen.
