# Dino — Technischer Stand (Jetzt)

**Datum:** 2026-08-21 · **Version:** `dino` 0.3.0  
**Suite:** `pytest tests/dino` → **grün** (inkl. Gap-Closure + Proof-Contract-E2E)  
**Normative Spezifikation:** [`docs/PROOF_CONTRACT.md`](PROOF_CONTRACT.md)

---

## Executive summary

Dino ist ein **verkaufbares Proof-CLI**: es versiegelt Ausführung, prüft Logic-/Data-Integrität und liefert ein content-addressiertes `proof.json` — nicht Image-Provenance und nicht Secret-SAST.

| Frage | Antwort |
|-------|---------|
| Was ist das Produkt? | `dino proof run` → Capsule + optional Scan + Map → `proof.json` |
| Was ist neu am Markt? | Eine CLI, die **Execution-Seal + Causal Leakage + Structural Drift** in einem Audit-Objekt bindet |
| Technischer Stand | Capsule sealed (re-exec), Bundle-Regression, Supersession-Verträge, Proof-Doctor, Contract-Doku |
| Nächster Engpass | **Markt-Validierung** — offizieller ICP-Test [`internal/ICP_TEST.md`](internal/ICP_TEST.md) (Quant + Fraud) |

---

## 1. Oberfläche

```
dino {scan,bundle,flight,verify,map,capsule,proof}
```

| Domain | Pack | Rolle |
|--------|------|--------|
| `scan` | free | Leakage / grammar |
| `capsule` | proof | Sealed subprocess |
| `map` | proof | Import-IR / plan / verify / drift |
| `bundle` | proof | Evidence + regression (`replay`/`verify`/`diff`) |
| `flight` | proof | Canary stability |
| `verify` | proof | Attest / binary / drift / supersede |
| `proof` | proof | End-to-end chain + doctor |

Packs: `free` = `{scan}` · `proof` = `{capsule,map,bundle,flight,verify,proof}`

---

## 2. Proof-Contract (implementiert)

Siehe **[`PROOF_CONTRACT.md`](PROOF_CONTRACT.md)** — Pflicht vor Verkauf.

Kurz:

- Schema `dino.proof.bundle.v1` + `schemas{}` für Capsule/Scan/Map/Drift  
- Status: `passed` | `partial` | `failed`  
- Audit: `PROOF_PASSED` / `PROOF_PARTIAL` / `PROOF_FAILED` (+ verify/doctor)  
- Exit: `0` passed/partial · `1` failed · `2` usage/pack/missing  
- `proof_hash` über Body ohne `ok` / `output_dir`  
- Guarantees / Non-guarantees / Drift- & Supersession-Vokabular dokumentiert  

Code: `dino/domains/proof/chain.py`

---

## 3. Domain-Technik (aktuell)

### 3.1 Capsule — sealed execution

- `run_command` → stdout/stderr/exit, `\n`-normalisiert, PATH/LANG-Seal  
- `make_capsule` hasht command/stdin/env/output/stderr/exit_code/extra  
- `replay` = Hash-Recompute **und** Re-Exec (`hash_ok` ∧ `exec_ok`)  
- Schema: `dino.capsule.capsule.v1`

### 3.2 Scan — free moat

Regeln: `LEAKY_IMPORT`, `FUTURE_INDEX`, `SHIFT_NEGATIVE`, `CONVOLVE_MODE_SAME_AST`, `SEEDLESS_SPLIT`, `TARGET_IN_FEATURES`, `SYNTAX`  
Report-Schema: `dino.scan.leakage.v1`

### 3.3 Map — structural IR

- AST-Import-Graph, Topo-Plan, Quality-Score, Drift vs Baseline  
- Schemas: `dino.map.graph.v1` / `plan.v1` / `verify.v1` / `drift.v1`  
- Python-only (bewusste Spezialisierung)

### 3.4 Bundle — official regression workflow

| Command | Exit |
|---------|------|
| `bundle replay` / `bundle verify` | `1` wenn Baseline nicht erfüllt |
| `bundle diff` | immer `0` (Review) |
| `bundle create` | Evidence merge `complete-run-v1` |

Semantik: `true_count` darf nicht sinken; `endpoint_ratio ≥ 0.8`.  
Schema: `dino.bundle.regression.v1` + Audit-Verdicts.

### 3.5 Verify — governance

- `drift`: aligned / controlled_drift / severe_drift / synthetic_world / unmeasured  
- `supersede`: Contract-Files; `REJECTED`→`DENY`; Chain-Check  
- `attest` / `binary`: hash-bound trust surface (kein Cosign-Ersatz)

### 3.6 Flight

Canary-Aggregator (`engine_j_canary_*.json`) — Consumer, kein Producer.

### 3.7 Proof CLI

| Command | Funktion |
|---------|----------|
| `proof run` | Kette → `proof.json` + Audit-Banner |
| `proof verify` | Hash + Capsule-Re-Exec |
| `proof doctor` | Stack-Health (Python, scan, map, drift, capsule, proof, packs) |

---

## 4. Test-Lage

| Suite | Inhalt | Status |
|-------|--------|--------|
| `tests/dino` Kern | Isolation, Determinism, Domains, Packs | ✅ |
| `test_gap_closure.py` | Capsule re-exec, tamper, bundle, supersede, scan rules, map plan/drift, proof | ✅ |
| `test_proof_contract.py` | E2E run, verify pass/fail, JSON contract, doctor, scan-fail | ✅ |

Einziger historischer Env-Fail (`which dino`) → Fallback auf Modul-`version`.

---

## 5. Reife-Matrix (nach Gap-Closure + Contract)

| Domain / Cmd | Reife 1–5 | Bemerkung |
|--------------|-----------|-----------|
| scan grammar/leakage | 4 | Moat + Schema |
| capsule run/replay/doctor | 4 | Echte Seal+Re-Exec |
| map * | 4 | Solid, Python-TAM |
| bundle create/verify/diff | 4 | Offizieller Workflow |
| flight summary | 3 | Format-gekoppelt |
| verify drift/supersede | 4 | Vokabular + Files |
| verify attest/binary | 3 | Preimage, kein PKI |
| proof run/verify/doctor | 5 | Contract + Tests + UX |

---

## 6. Was Dino bewusst nicht ist

- Kein Sigstore/Cosign-Ersatz  
- Kein gitleaks/Semgrep-Ersatz (außer Research-Leakage)  
- Kein polyglot-SAST  
- Partial proof ≠ „alles sauber“ — nur „nicht angefordert“

---

## 7. Referenz-Workflow

```bash
pip install -e '.[dev]'
dino upgrade --pack proof
dino proof doctor
dino proof run \
  --command echo market_unique \
  --repo dino/common \
  --scan tests/dino/fixtures/scan/clean_code.py \
  --output-dir ./proof_out
dino proof verify --proof ./proof_out/proof.json
dino bundle verify \
  --baseline tests/dino/fixtures/bundle/baseline_counts.json \
  --current tests/dino/fixtures/bundle/current_counts.json
pytest tests/dino -q
```

---

## 8. Dokumente

| Doc | Rolle |
|-----|--------|
| [`../README.md`](../README.md) | Produkt-Einstieg (aligned mit Website) |
| [`PROOF_CONTRACT.md`](PROOF_CONTRACT.md) | Normative Guarantees / Schemas |
| [`CLI_E2E_REFERENCE.md`](CLI_E2E_REFERENCE.md) | CLI + Live-Outputs |
| [`EXAMPLES.md`](EXAMPLES.md) | Kurzbeispiele |
| [`internal/`](internal/) | ICP, Evaluation, Publish |
| [`../website/`](../website/) | Landing Page |

---

## 9. Verbleibende Launch-Engpässe

1. **ICP-Test ausführen** — 10 Gespräche laut [`internal/ICP_TEST.md`](internal/ICP_TEST.md)  
2. Evidence-Backlog füllen (`docs/internal/evidence/`)  
3. Pricing an Gesprächsdaten kalibrieren  
4. Repo auf GitHub pushen (`ArdentCrab/devsecops`)

**Fazit:** Technisch verkaufbar. Marktentscheidung = ICP-Test, nicht mehr Code.
