export const SITE = {
  version: "0.3.0",
  tagline: "Deterministic Proof for Python Decision Pipelines",
  subtitle:
    "Dino versiegelt Ausführung, erkennt Leakage, klassifiziert Drift und erzeugt ein auditierbares proof.json.",
};

export const NAV = [
  { href: "#features", label: "Features" },
  { href: "#contract", label: "Contract" },
  { href: "#cli", label: "CLI" },
  { href: "#pricing", label: "Pricing" },
  { href: "#faq", label: "FAQ" },
  { href: "/docs", label: "Docs" },
];

export const ABOUT = [
  "Dino ist ein Proof-CLI für Python-Entscheidungslogik — Research-Pipelines, Backtests und Risk-Systeme.",
  "Es erzeugt deterministische Ausführungsbeweise, verhindert ML-Leakage und liefert reproduzierbare Audit-Artefakte.",
  "Dino ist kein Secret-Scanner oder Image-Provenance-Tool — es ist ein Proof-Tool für versiegelte Entscheidungslogik.",
];

export const ICPS = [
  {
    title: "Quant Research",
    body: "Lookahead, non-repro Backtests, sealed pipeline evidence.",
  },
  {
    title: "Fraud / Scoring FinTech",
    body: "Audit-ready decision evidence und Governance-Signale.",
  },
];

export const PAINPOINTS = [
  {
    title: "Leakage in ML-Pipelines",
    body: "Future-Index, Shift-Negative, Seedless-Splits, Target-Leakage.",
  },
  {
    title: "Nicht-deterministische Backtests",
    body: "Unterschiedliche Ergebnisse bei identischen Runs.",
  },
  {
    title: "Strukturelle Drift",
    body: "Import-Graph-Änderungen, unkontrollierte Abhängigkeiten.",
  },
  {
    title: "Fehlende Audit-Beweise",
    body: "Kein Replay, keine deterministische Ausführung, keine Proof-Artefakte.",
  },
];

export const MODULES = [
  {
    title: "Capsule Seal",
    body: "Deterministische Subprocess-Ausführung mit Replay-Integrität.",
  },
  {
    title: "Leakage Scan",
    body: "7 ML-Leakage-Regeln für Research-Pipelines (Free Pack).",
  },
  {
    title: "Structural Map",
    body: "AST-Graph, Drift-Buckets und Plan-Analyse.",
  },
  {
    title: "Bundle Regression",
    body: "true_delta und endpoint_ratio für Backtest-Regressionen.",
  },
  {
    title: "Flight Canary",
    body: "Canary-Summary über Evidence-Verzeichnisse.",
  },
  {
    title: "Governance Verify",
    body: "Drift, Supersession, Attest und Binary-Checks.",
  },
  {
    title: "Proof Chain",
    body: "proof.json mit PROOF_PASSED und PROOF_VERIFY_PASSED.",
  },
];

export const GUARANTEES = [
  "deterministische Ausführung",
  "deterministische Wiederholung",
  "content-addressed Artefakte",
  "Leakage-Regeln für Research-Code",
  "Drift-Klassifikation",
  "Regression-Proof",
  "Governance-Verträge",
  "PROOF_PASSED / PROOF_VERIFY_PASSED",
];

export const CONTRACT_FOOTNOTE =
  "Dino garantiert deterministische Ausführung, aber nicht bit-identische Runs über OS-Grenzen oder vollständige Leakage-Erkennung.";

export const CLI_EXAMPLES = [
  {
    label: "proof run",
    code: `dino proof run \\
  --command "echo ok" \\
  --repo . \\
  --scan ./src \\
  --output-dir ./proof_out`,
  },
  {
    label: "proof verify",
    code: "dino proof verify --proof ./proof_out/proof.json",
  },
  {
    label: "scan leakage",
    code: "dino scan leakage my_pipeline.py",
  },
];

export const PACKS = [
  {
    name: "Free",
    price: "0 €",
    hint: "Leakage-Scan",
    cta: "Kostenlos starten",
    tier: "free" as const,
  },
  {
    name: "Indie",
    price: "49 €",
    hint: "einmalig — Proof Pack",
    cta: "Download",
    tier: "indie" as const,
    featured: true,
  },
  {
    name: "Team",
    price: "20 %",
    hint: "Rabatt — 5–10 Sitze",
    cta: "Anfragen",
    tier: "team" as const,
  },
];

export const FAQ = [
  {
    q: "Ist Dino Open Source?",
    a: "Nein — deterministische Proof-Artefakte benötigen kontrollierte Releases.",
  },
  {
    q: "Welche Sprache unterstützt Dino?",
    a: "Ausführung: jede Sprache. Analyse: Python-Pipelines.",
  },
  {
    q: "Braucht Dino Cloud?",
    a: "Nein — vollständig offline.",
  },
  {
    q: "Ist Dino deterministisch?",
    a: "Ja — Capsule + Replay + proof_hash.",
  },
];

/** Public docs — same set as README */
export const DOC_LINKS = [
  { label: "Proof-Contract", path: "docs/PROOF_CONTRACT.md" },
  { label: "CLI-Referenz", path: "docs/CLI_E2E_REFERENCE.md" },
  { label: "Examples", path: "docs/EXAMPLES.md" },
  { label: "Tech Status", path: "docs/TECH_STATUS_NOW.md" },
];
