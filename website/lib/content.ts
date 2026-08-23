export const SITE = {
  version: "0.3.0",
  tagline: "Dino — Local-First Audit Engine for Python Pipelines",
  subtitle:
    "Deterministic proofs, export contracts, and a universal proof index for your dashboards.",
};

export const NAV = [
  { href: "#engine", label: "Engine" },
  { href: "#export", label: "Export" },
  { href: "#index", label: "Index" },
  { href: "#integrate", label: "Integrate" },
  { href: "#cli", label: "CLI" },
  { href: "#pricing", label: "Pricing" },
  { href: "#faq", label: "FAQ" },
  { href: "/docs", label: "Docs" },
];

export const ABOUT = [
  "Dino is a local-first audit engine for Python decision pipelines — research, fraud, risk, compliance.",
  "No cloud. No hosted UI. No platform. Only deterministic proof artifacts your systems can consume.",
  "Seal → scan → map → proof.json → export → proof_index.json. Your dashboard does the rest.",
];

export const ENGINE_POINTS = [
  {
    title: "Local-first",
    body: "Runs on your machine and CI. Offline by default. No telemetry required.",
  },
  {
    title: "Deterministic proofs",
    body: "Content-addressed proof_hash, capsule replay, fail-closed leakage and tamper checks.",
  },
  {
    title: "Not a platform",
    body: "Dino is the audit motor. You keep storage, dashboards, and governance UIs.",
  },
];

export const EXPORT_CONTRACTS = [
  {
    title: "Path export",
    body: "--export ./archive → content-addressed folders + proof_index.json for filesystem consumers.",
  },
  {
    title: "HTTP export",
    body: "--export https://…/api/proofs → POST dino.proof.export.v1 with optional Bearer token.",
  },
  {
    title: "S3 export",
    body: "--export s3://bucket/prefix → upload bundles and merge proof_index.json via boto3 or AWS CLI.",
  },
];

export const INDEX_FEATURES = [
  {
    title: "Listing",
    body: "proof_index.json lists every sealed proof with pipeline, group, tags, drift, leakage, verdict.",
  },
  {
    title: "Metrics",
    body: "dino proof index metrics — totals, pass/fail, drift buckets, leakage counts, pipelines.",
  },
  {
    title: "Compare",
    body: "dino proof index compare — drift/leakage/artifacts/pipeline/verdict deltas for CI and audits.",
  },
  {
    title: "Layout",
    body: "pipelines/ · groups/ · tags/ browse links so folders can be scanned without a Dino UI.",
  },
];

export const INTEGRATE = [
  {
    title: "Dino delivers the engine",
    body: "CLI seals runs and emits contracts: export.v1 + index.v1 + compare/metrics JSON.",
  },
  {
    title: "Your dashboard consumes artifacts",
    body: "Ingest path archives, HTTP POSTs, or S3 prefixes. Render charts and alerts yourself.",
  },
  {
    title: "No SaaS, no hosting",
    body: "No Dino cloud, no lock-in. MIT core + optional paid unlock for the Proof pack.",
  },
];

export const ICPS = [
  {
    title: "Risk & Fraud",
    body: "Sealed scoring runs, leakage checks, proof history for model governance.",
  },
  {
    title: "Research & Compliance",
    body: "Reproducible backtests and audit trails without a vendor dashboard.",
  },
];

export const PAINPOINTS = [
  {
    title: "ML pipeline leakage",
    body: "Future-index, shift-negative, seedless splits, target leakage.",
  },
  {
    title: "Non-deterministic runs",
    body: "Same inputs, different results — no sealed replay.",
  },
  {
    title: "Structural drift",
    body: "Import-graph changes without a content-addressed record.",
  },
  {
    title: "Dashboard gap",
    body: "Teams need artifacts, not another hosted control plane.",
  },
];

export const MODULES = [
  {
    title: "Capsule Seal",
    body: "Deterministic subprocess execution with replay integrity.",
  },
  {
    title: "Leakage Scan",
    body: "Research leakage rules for Python pipelines (Free pack).",
  },
  {
    title: "Structural Map",
    body: "AST graph, drift buckets, plan analysis.",
  },
  {
    title: "Proof Chain",
    body: "proof.json with PROOF_PASSED / PROOF_VERIFY_PASSED.",
  },
  {
    title: "Export Contracts",
    body: "Path / HTTP / S3 upload — dino.proof.export.v1.",
  },
  {
    title: "Proof Index",
    body: "proof_index.json + compare / metrics / layout.",
  },
];

export const GUARANTEES = [
  "deterministic sealed execution",
  "deterministic replay",
  "content-addressed proof_hash",
  "export contract dino.proof.export.v1",
  "index contract dino.proof.index.v1",
  "compare + metrics JSON for your consumers",
  "layout links under pipelines/ groups/ tags/",
  "PROOF_PASSED / PROOF_VERIFY_PASSED",
];

export const CONTRACT_FOOTNOTE =
  "Dino is a local audit motor — not a platform. Guarantees sealed deterministic execution, not bit-identical runs across OS boundaries or complete AppSec coverage.";

export const CLI_EXAMPLES = [
  {
    label: "proof run + export",
    code: `dino proof run \\
  --command echo ok \\
  --scan ./tests/e2e/pipe.py \\
  --output-dir ./proof_out \\
  --pipeline fraud_score_v4 \\
  --group risk-team \\
  --tag prod --tag v4 \\
  --export ./archive`,
  },
  {
    label: "index metrics",
    code: "dino proof index metrics ./archive",
  },
  {
    label: "index compare",
    code: "dino proof index compare ./archive <hash_a> <hash_b>",
  },
];

export const PACKS = [
  {
    name: "Free",
    price: "€0",
    hint: "Leakage Scan",
    cta: "Get started",
    tier: "free" as const,
  },
  {
    name: "Indie",
    price: "€49",
    hint: "One-time — Full Proof Pack",
    cta: "Buy",
    tier: "indie" as const,
    featured: true,
  },
  {
    name: "Team",
    price: "€39",
    hint: "Per seat (20% off) — Full Proof Pack",
    cta: "Buy / Contact",
    tier: "team" as const,
  },
  {
    name: "Large Teams",
    price: "Custom",
    hint: "20+ seats, invoicing on request",
    cta: "Contact",
    tier: "large" as const,
  },
];

export const PRICING_RULES = [
  "Team pricing starts at 3 seats",
  "Team pricing applies up to 20 seats",
  "Above 20 seats → contact us",
  "No Enterprise tier, no subscriptions, no lock-in",
  "Checkout via Lemon Squeezy · unlock with: dino upgrade --pack proof --key YOUR_KEY",
];

export const PRICING_UNLOCK = "dino upgrade --pack proof --key YOUR_LICENSE_KEY";

export const FAQ = [
  {
    q: "Is Dino a SaaS or dashboard?",
    a: "No. Dino is a local audit engine. It emits proof artifacts and contracts; you own dashboards and storage.",
  },
  {
    q: "Is Dino open source?",
    a: "Yes — MIT on GitHub. Paid packs are optional commercial unlocks (local license file).",
  },
  {
    q: "How do I feed our dashboard?",
    a: "Use --export path|https://…|s3://… then consume proof_index.json, metrics, and compare JSON — or browse pipelines/groups/tags.",
  },
  {
    q: "Does Dino need the cloud?",
    a: "No — fully offline. S3/HTTP export is optional integration, not a Dino-hosted service.",
  },
  {
    q: "Is Dino deterministic?",
    a: "Yes — capsule + replay + proof_hash within a sealed environment.",
  },
  {
    q: "How do I unlock the Proof Pack?",
    a: "Buy Indie/Team on Lemon Squeezy, then: dino upgrade --pack proof --key YOUR_LICENSE_KEY",
  },
  {
    q: "Is Dino on PyPI?",
    a: "No — name collision. Install: pip install \"git+https://github.com/DinoDevCli/dino.git\".",
  },
];

export const DOC_LINKS = [
  { label: "Proof Contract", path: "docs/PROOF_CONTRACT.md" },
  { label: "Proof Export", path: "docs/PROOF_EXPORT.md" },
  { label: "Proof Index", path: "docs/PROOF_INDEX.md" },
  { label: "CLI Reference", path: "docs/CLI_E2E_REFERENCE.md" },
  { label: "Examples", path: "docs/EXAMPLES.md" },
  { label: "Lemon Squeezy", path: "docs/LEMON_SQUEEZY.md" },
];

export const SECTIONS = {
  about: { label: "Engine", title: "Local-First Audit Engine" },
  audience: { label: "Audience", title: "Built for risk, fraud, research, compliance" },
  features: { label: "Modules", title: "Seal, scan, prove, export, index" },
  export: { label: "Export", title: "Three export contracts" },
  index: { label: "Index", title: "Universal proof index" },
  integrate: { label: "Integrate", title: "Integrates into your dashboard" },
  contract: { label: "Contracts", title: "What Dino guarantees" },
  cli: { label: "CLI", title: "Engine commands" },
  pricing: { label: "Pricing", title: "Simple packs" },
  faq: { label: "FAQ", title: "FAQ" },
  docsHint: "Full docs",
  cliRef: "CLI reference ↗",
  cliHint:
    "Always prefer --export with --pipeline / --group / --tag so proof_index.json stays useful.",
  footerLine: "Dino is a local audit motor — not a platform.",
};
