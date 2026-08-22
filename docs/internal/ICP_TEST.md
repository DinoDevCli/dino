# Dino — Offizieller ICP-Test

**Status:** Normativ für Go-to-Market · **Stand:** 2026-08-21  
**Produkt:** Dino CLI (`proof` pack) · **Contract:** [`PROOF_CONTRACT.md`](PROOF_CONTRACT.md)  
**Zweck:** Markt validieren — nicht Features raten.

Dieses Dokument ist der **offizielle Testplan**, mit dem Noah entscheidet:

> Haben wir einen zahlenden ICP — ja oder nein?

Kein „vielleicht Python Research“. Nur **Rolle + Problem + Budget + Beleg + Preis-Hypothese + Pass/Fail**.

---

## 0. Test-Metadaten

| Feld | Wert |
|------|------|
| Test-ID | `DINO-ICP-T1` |
| Primäre ICPs | **ICP-1 Quant Research** · **ICP-2 Fraud/Scoring** |
| Sekundäre ICPs | ICP-3 Reco · ICP-4 Pharma · ICP-5 Insurance (nur beobachten) |
| Stichprobe | **mindestens 10 Gespräche** (Ziel: 6× ICP-1 + 4× ICP-2) |
| Dauer | 2–3 Wochen Discovery |
| Entscheidung | nach Scorecard §8 |

**Pass-Regel (hart):** Mindestens **3** Gesprächspartner aus Primär-ICPs bestätigen (a) den Schmerz ≥ €10k/Jahr und (b) Zahlungsbereitschaft für Tier 2 oder Interesse an Tier 3 Pilot.

**Fail-Regel (hart):** Nach 10 Gesprächen niemand nennt Drift/Leakage/Repro als Top-3-Schmerz **oder** niemand akzeptiert Preis ≥ €49 als sinnvoll.

---

## 1. ICP-Definitionen (offiziell)

Jede ICP-Zeile = **eine Berufsrolle + ein konkretes Problem + ein Budgetfenster**.

### ICP-1 — Quant Research (Start #1)

| Feld | Definition |
|------|------------|
| **Wer** | Quant Researcher, Risk Engineer, Systematic Trading Research Lead |
| **Wo** | Banken (Prop/Structuring), Hedge Funds, Prop Shops, Quant Boutiques (DACH + London + remote EU) |
| **Stack** | Python-heavy Feature/Backtest Pipelines |
| **Schmerz** | Stille Drift in Backtests, Feature-Leakage (lookahead), nicht reproduzierbare Research-Runs |
| **Budget** | €10k–€250k/Jahr (Tooling + Model Risk / Research Ops) |
| **Warum Dino** | `scan` (leakage) + Capsule-Seal + Drift-Buckets + `proof.json` als Research-Evidence |
| **Kaufsignal** | „Wir hatten schon lookahead / non-repro incidents“ · internes Model-Risk-Review |
| **Anti-ICP** | Rein Excel/R-Teams · keine Python-Pipelines · nur Cloud-MLOps ohne Research-Code |

### ICP-2 — Fraud / Scoring FinTech (Start #2)

| Feld | Definition |
|------|------------|
| **Wer** | Fraud Analyst Tech Lead, ML Engineer Fraud/Credit Scoring, Head of Decisioning |
| **Wo** | FinTechs, Neobanken, Payment/Lending, Buy-Now-Pay-Later (EU) |
| **Stack** | Python Scoring/Feature Pipelines, Canaries, Audit-Anforderungen |
| **Schmerz** | Feature-Drift, Canary-Instabilität, nicht auditierbare Entscheidungen |
| **Budget** | €5k–€50k/Jahr (Compliance + Fraud-Tooling) |
| **Warum Dino** | `proof.json` als Audit-Artefakt · Flight/Canary-Linse · Bundle-Regression · Supersession |
| **Kaufsignal** | Regulatorische Prüfung / interne Audit-Findings · „wir können den Run nicht beweisen“ |
| **Anti-ICP** | Nur Rules-Engines ohne ML · Teams die nur SaaS-Fraud-Vendor kaufen und keinen Code besitzen |

### ICP-3 — Recommendation / Ranking (Beobachten)

| Feld | Definition |
|------|------------|
| **Wer** | Data Scientist Reco, ML Ops Ranking |
| **Schmerz** | Pipeline-Drift, nicht reproduzierbare Feature-Runs |
| **Budget** | €3k–€30k/Jahr |
| **Priorität im T1-Test** | Sekundär — nur wenn ICP-1/2-Pipeline leer |

### ICP-4 — Pharma / Clinical ML (Beobachten)

| Feld | Definition |
|------|------------|
| **Wer** | Bioinformatics / Clinical ML Engineer |
| **Schmerz** | Deterministische Repro für Audits |
| **Budget** | €20k–€200k/Jahr |
| **Priorität** | Später (längere Sales-Cycles) |

### ICP-5 — Insurance Risk Modeling (Beobachten)

| Feld | Definition |
|------|------------|
| **Wer** | Actuarial ML, Risk Modeling |
| **Schmerz** | Drift in Feature-Stores, nicht repro Scoring |
| **Budget** | €10k–€100k/Jahr |
| **Priorität** | Später / Parallel zu ICP-2 wenn Versicherungs-Kontakte da |

---

## 2. Hypothesen (was der Test prüft)

| ID | Hypothese | Messgröße |
|----|-----------|-----------|
| H1 | ICP-1 und ICP-2 haben **mindestens einen** Vorfall Leakage/Drift/Non-Repro in 24 Monaten | Ja/Nein + Schätzung € |
| H2 | Der Schmerz kostet intern **≥ €10k/Jahr** (Zeit, False Alpha, Audit, Rollback) | Genannte Zahl oder Band |
| H3 | Docker+Sigstore+Semgrep **decken den Schmerz nicht** | Explizite Aussage |
| H4 | `proof.json` / Capsule / Scan ist verständlich in **≤ 10 Minuten** Demo | Self-score 1–5 |
| H5 | Zahlungsbereitschaft: Tier1 €49 **oder** Tier2 €29/Dev/Mo **oder** Tier3 Pilot ≥ €5k | Mind. eine Option „ja/vielleicht mit Pilot“ |
| H6 | Kaufentscheider erreichbar in ≤ 2 Steps vom Gesprächspartner | Named role |

---

## 3. Beleglage (Schmerz ist real — vor dem Gespräch)

Kein Ratespiel: diese Pain-Klassen sind in der Praxis und Literatur etabliert. Im Gespräch **nicht dozieren** — als Anker nutzen.

### 3.1 Leakage / Research-Integrity (→ `scan`)

| Dino-Regel | Schmerzklasse | Warum Käufer nicken |
|------------|---------------|---------------------|
| `FUTURE_INDEX` | Lookahead bias in Backtests | Klassischer Quant-Fehler; teure False Alpha |
| `SHIFT_NEGATIVE` | Label/future peek | Feature aus Zukunft → kontaminierte Modelle |
| `TARGET_IN_FEATURES` | Data contamination | Target in X → Schein-Performance |
| `SEEDLESS_SPLIT` | Non-reproducible experiments | Audits / Peer-Review scheitern |
| `CONVOLVE_MODE_SAME` / leaky imports | Causal / domain leakage | Spezifisch Research-Pipelines |

**Sales-Satz:** „Semgrep findet Secrets. Dino findet Lookahead.“

### 3.2 Proof / Governance (→ `proof.json`, Capsule, Drift, Supersession)

| Anforderung (typisch) | Dino-Antwort |
|-----------------------|--------------|
| Reproduzierbare Pipeline / Evidence | Capsule seal + re-exec |
| Drift / Model change visibility | Drift-Buckets + Map |
| Decision override nach Release | Supersession-Chain |
| Baseline nicht unterschreiten | Bundle verify/regression |
| Ein Artefakt für Review | `proof.json` + Audit-Verdict |

**Sales-Satz:** „Sigstore beweist Herkunft. Dino beweist dieselbe Logik.“

### 3.3 Beleg-Backlog (vor Launch füllen — parallel zum ICP-Test)

Ziel pro Kategorie **≥ 3** Einträge (öffentlich zitierbar oder anonymisierte Customer Stories):

| Kategorie | Ziel | Status im Repo |
|-----------|------|----------------|
| Drift-Postmortems | 3 | ⏳ zu sammeln → `docs/evidence/` |
| Leakage-Fehler (Repos/Papers/Kaggle) | 3 | ⏳ |
| Canary-Instabilitäten | 3 | ⏳ |
| Backtest-Fehler | 3 | ⏳ |
| Audit-/Regulatory-Anforderungen (Zusammenfassung) | 3 | ⏳ |

Vorlagen: siehe §9.

---

## 4. Pricing — Hypothesen zum Testen (nicht final)

Drei Preispunkte, die **im Gespräch** kalibriert werden:

| Tier | Preis (Hypothese) | Für wen | Was drin |
|------|-------------------|---------|----------|
| **T1 Indie** | **€49 einmalig** | Einzel-Dev / Indie ML | Proof-Pack: Capsule, Map, Scan, Drift, Proof |
| **T2 Team** | **€29 / Monat / Entwickler** | Teams 2–10 | + Bundle-Regression, Supersession, Flight, Support-Light |
| **T3 Enterprise** | **€5.000–€50.000 / Jahr** | Bank / Insurance / Pharma / großer FinTech | Audit-Support, Contract-Integration, Compliance-Review, Private builds |

**Kalibrierungsfragen (Pflicht):**

1. „Was kostet euch ein Drift-Fehler / ein nicht reproduzierbarer Run / ein Leakage-Bug — grob?“  
2. „Wäre €49 einmalig für einen Researcher sinnvoll?“  
3. „Wäre €29/Dev/Mo für ein 5er-Team denkbar?“  
4. „Ab welchem jährlichen Betrag lohnt sich ein Pilot mit Audit-Support?“

**Erwartetes Band der Schmerz-Antwort:** €10k–€500k (wenn darunter → ICP falsch oder Schmerz zu weich).

Vergleichskategorie (nicht Feature-Parität): MLflow Enterprise, Evidently, Fiddler, Arize, Seldon, Neptune — Dino kleiner, gleiche **Budget-Schublade** Model/Decision Governance.

---

## 5. Gesprächsprotokoll (30–40 Min)

### 5.1 Qualifikation (3 Min)

- Rolle / Teamgröße / Python-Pipelines ja/nein?  
- Backtest, Scoring, Fraud, Ranking? → ICP-Label setzen  
- Anti-ICP? → höflich beenden, notieren

### 5.2 Schmerz (12 Min)

Fragen (wörtlich nutzbar):

1. „Wann ist euch zuletzt ein Backtest / Score **zu gut** vorgekommen — und warum?“  
2. „Hattet ihr schon Lookahead / Label-Leakage / seedlose Splits?“  
3. „Könnt ihr einen Research-Run von vor 6 Monaten **bitgenau** wiederholen?“  
4. „Was passiert bei Canary-/Feature-Drift — wer merkt es zuerst?“  
5. „Was kostet so ein Vorfall (Zeit, PnL, Audit, Rollback)?“

### 5.3 Status-quo Tools (5 Min)

- Docker / Cosign / Semgrep / MLflow / Evidently / interne Scripts?  
- „Was davon beweist **dieselbe Logik**, nicht nur denselben Container?“

### 5.4 Demo (8 Min) — festes Script

```bash
dino proof doctor
dino scan leakage <ihre_oder_demo_datei>
dino proof run --command <minimal> --repo <demo> --scan <pfad> --output-dir ./proof_out
dino proof verify --proof ./proof_out/proof.json
```

Zeig: Audit-Verdict + `proof.json` Felder laut Contract.

### 5.5 Preis (5 Min)

Tier 1 → 2 → 3 der Reihe nach; Reaktion notieren: **Nein / Vielleicht / Ja / Pilot**.

### 5.6 Nächster Schritt (2 Min)

- Pilot-Repo? Follow-up? Intro zu Risk/Compliance?

---

## 6. Scorecard (pro Gespräch)

Kopiere pro Call eine Zeile nach `docs/evidence/icp_scorecard.csv` (oder Notion).

| Feld | Werte |
|------|--------|
| date | ISO |
| contact | name/org (oder anonym) |
| icp | 1\|2\|3\|4\|5\|anti |
| role | text |
| pain_confirmed | y/n |
| pain_cost_eur | number oder band |
| tools_gap_confirmed | y/n (Sigstore≠Logic) |
| demo_score_1_5 | 1–5 |
| price_t1 | no\|maybe\|yes |
| price_t2 | no\|maybe\|yes |
| price_t3_pilot | no\|maybe\|yes |
| champion | y/n |
| next_step | text |
| notes | text |

**Gesprächs-Score (0–10):**

- +2 pain_confirmed  
- +2 pain_cost ≥ 10k  
- +2 tools_gap_confirmed  
- +1 demo ≥ 4  
- +2 price yes/maybe auf T2 oder T3  
- +1 champion  

**Starker Lead:** Score ≥ 7.

---

## 7. Firmen-/Kanal-Targets (Startliste, keine Exhaustion)

Zum Outreach **konkretisieren**, nicht „irgendwelche Banken“:

### ICP-1 Kanäle

- Quant Meetups / London & Frankfurt Quant circles  
- LinkedIn: „Quant Researcher“ + „Python“ + „Backtest“  
- Alumni von Prop Shops / bekannten Quant Funds (warm intros)  
- Open-Source Quant/Backtest Maintainer (Schmerz + Credibility)

### ICP-2 Kanäle

- FinTech Engineering Leads (Fraud/Credit) LinkedIn  
- Compliance/ML meetups EU  
- Partner: Consultancies die Model Governance verkaufen  

**Regel:** Pro Woche ≥ 15 Outreaches, Ziel ≥ 3 Calls.

*(Namen konkreter Firmen bewusst als Arbeitsliste pflegen — datenschutz-/sales-sensibel — in privatem CRM, nicht zwingend public im Repo.)*

---

## 8. Pass / Fail / Pivot (Entscheidung nach 10 Calls)

| Ergebnis | Bedingung | Aktion |
|----------|-----------|--------|
| **PASS — ICP-1** | ≥ 3 starke Leads (Score ≥7) in Quant | ICP-1 Landing + Outreach verdoppeln; T2/T3 Pitches |
| **PASS — ICP-2** | ≥ 3 starke Leads in Fraud/Scoring | Fraud-Audit-Story first; Bundle/Supersession betonen |
| **PASS — Dual** | beide ≥ 2 starke Leads | Zwei One-Pagers, ein Product |
| **PIVOT secondary** | Primär &lt; 2, aber ICP-3/5 ≥ 3 | Messaging auf Reco/Insurance schwenken |
| **FAIL** | &lt; 2 starke Leads total; Schmerz &lt; €10k; Preis überall „nein“ | Produkt nicht GTM-ready für bezahltes Proof — Free-`scan` Viralität testen, ICP neu wählen |

**Keine Parallel-Erfindung neuer Features während des Tests**, außer Blocker aus ≥ 3 Calls identisch.

---

## 9. Evidence-Backlog Vorlage

Ordner: `docs/evidence/` (anlegen beim ersten Eintrag).

Pro Eintrag eine Markdown-Datei:

```markdown
# EVIDENCE-001 — <Titel>
- Kategorie: leakage | drift | canary | backtest | audit
- Quelle: URL / Paper / anonymisierte Story
- Datum:
- ICP-Relevanz: 1|2|…
- One-liner für Sales:
- Mapping auf Dino: scan rule / proof / drift / capsule / …
```

Ziel vor öffentlichem Launch: **15 Einträge** (3×5 Kategorien).

---

## 10. One-Pager Messaging (für Calls)

**Headline:** Logic & Data Integrity Proof for Python Decision Pipelines.

**Für Quant:** Stop silent lookahead. Seal the research run. Prove drift class.

**Für Fraud:** Audit-ready `proof.json`. Regression gates. Runtime supersession when production overrides the gate.

**Nicht sagen:** „DevSecOps Platform“, „besser als Semgrep“, „Enterprise für alle“.

**Immer sagen:** Rolle + Schmerz + Artefakt (`proof.json`) + Preis-Hypothese zum Testen.

---

## 11. Beziehung zu Produkt-Docs

| Doc | Rolle |
|-----|--------|
| [`PROOF_CONTRACT.md`](PROOF_CONTRACT.md) | Was wir technisch garantieren |
| [`TECH_STATUS_NOW.md`](TECH_STATUS_NOW.md) | Technischer Stand |
| **Dieses Doc** | Ob und für wen der Markt zahlt |

Produkt ist fertig. **Dieser Test entscheidet den Markt.**

---

## 12. Sofort-Checkliste (Woche 1)

- [ ] 20 ICP-1 + 20 ICP-2 Kontakte listen (CRM)  
- [ ] 15 Outreaches senden  
- [ ] Demo-Repo + 3 Leakage-Beispiele vorbereiten  
- [ ] Scorecard-Sheet anlegen  
- [ ] Ersten Evidence-Ordner mit 3 Leakage-Belegen füllen  
- [ ] Nach Call #5: Zwischenstand H1–H6  
- [ ] Nach Call #10: PASS/FAIL laut §8  

**Owner:** Noah · **Review:** nach Call #10 schriftlich in `docs/evidence/ICP_TEST_RESULT.md`
