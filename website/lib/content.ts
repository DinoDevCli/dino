export const SITE = {
  version: "0.3.0",
  tagline: "Deterministic Proof for Python Decision Pipelines",
  subtitle:
    "Seal execution, detect leakage, classify drift, emit auditable proof.json.",
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
  "Dino is a proof CLI for Python decision logic — research pipelines, backtests, risk systems.",
  "It seals runs, detects ML leakage, and produces reproducible audit artifacts.",
  "Narrow by design: deterministic seal → replay → proof_hash. Not a general SAST suite, secret scanner, SBOM tool, or image provenance product.",
];

export const ICPS = [
  {
    title: "Quant Research",
    body: "Lookahead, non-repro backtests, sealed pipeline evidence.",
  },
  {
    title: "Fraud / Scoring FinTech",
    body: "Audit-ready decision evidence and governance signals.",
  },
];

export const PAINPOINTS = [
  {
    title: "ML pipeline leakage",
    body: "Future-index, shift-negative, seedless splits, target leakage.",
  },
  {
    title: "Non-deterministic backtests",
    body: "Divergent results on identical runs.",
  },
  {
    title: "Structural drift",
    body: "Import-graph changes, uncontrolled dependencies.",
  },
  {
    title: "Missing audit evidence",
    body: "No replay, no sealed execution, no proof artifacts.",
  },
];

export const MODULES = [
  {
    title: "Capsule Seal",
    body: "Deterministic subprocess execution with replay integrity.",
  },
  {
    title: "Leakage Scan",
    body: "Seven ML leakage rules for research pipelines (Free pack).",
  },
  {
    title: "Structural Map",
    body: "AST graph, drift buckets, plan analysis.",
  },
  {
    title: "Bundle Regression",
    body: "true_delta and endpoint_ratio for backtest regressions.",
  },
  {
    title: "Flight Canary",
    body: "Canary summary over evidence directories.",
  },
  {
    title: "Governance Verify",
    body: "Drift, supersession, attest, binary checks.",
  },
  {
    title: "Proof Chain",
    body: "proof.json with PROOF_PASSED and PROOF_VERIFY_PASSED.",
  },
];

export const GUARANTEES = [
  "deterministic sealed execution",
  "deterministic replay",
  "content-addressed proof_hash",
  "research leakage rules (not complete AppSec)",
  "drift classification",
  "regression signals (bundle)",
  "governance checks (verify)",
  "PROOF_PASSED / PROOF_VERIFY_PASSED",
];

export const CONTRACT_FOOTNOTE =
  "Dino guarantees deterministic execution within a sealed environment — not bit-identical runs across OS boundaries, not complete leakage coverage, and not a replacement for broad AppSec scanners.";

export const CLI_EXAMPLES = [
  {
    label: "proof run",
    code: `dino proof run \\
  --command echo ok \\
  --repo . \\
  --scan ./path/to/pipeline.py \\
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
    price: "€0",
    hint: "Leakage Scan",
    cta: "Get started",
    tier: "free" as const,
  },
  {
    name: "Indie",
    price: "€49",
    hint: "One-time — Full Proof Pack",
    cta: "Download",
    tier: "indie" as const,
    featured: true,
  },
  {
    name: "Team",
    price: "€39",
    hint: "Per seat (20% off) — Full Proof Pack",
    cta: "Contact",
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
  "Unlock is local today (dino upgrade --pack proof); pay via contact until storefront ships",
];

export const PRICING_UNLOCK = "dino upgrade --pack proof";

export const FAQ = [
  {
    q: "Is Dino open source?",
    a: "Yes — MIT on GitHub. Paid packs are optional commercial unlocks (local license file), not a closed core.",
  },
  {
    q: "How is Dino different from Semgrep / Trivy / secret scanners?",
    a: "Those cover broad AppSec surface. Dino is a sealed proof chain for decision pipelines: capsule → scan → map → proof.json with verify and tamper checks.",
  },
  {
    q: "What languages does Dino support?",
    a: "Execution: any language. Analysis: Python pipelines.",
  },
  {
    q: "Does Dino need the cloud?",
    a: "No — fully offline.",
  },
  {
    q: "Is Dino deterministic?",
    a: "Yes — capsule + replay + proof_hash. Same inputs → same proof_hash within a sealed environment.",
  },
  {
    q: "How do I pass --command?",
    a: "Prefer argv tokens: --command echo ok. Use one quoted string when the program takes flags: --command \"python3 train.py --seed 0\".",
  },
  {
    q: "Is Dino on PyPI?",
    a: "No — the name dino is taken. Install from GitHub: pip install \"git+https://github.com/DinoDevCli/dino.git\".",
  },
];

export const DOC_LINKS = [
  { label: "Proof Contract", path: "docs/PROOF_CONTRACT.md" },
  { label: "CLI Reference", path: "docs/CLI_E2E_REFERENCE.md" },
  { label: "Examples", path: "docs/EXAMPLES.md" },
  { label: "Tech Status", path: "docs/TECH_STATUS_NOW.md" },
];

/** Section chrome — English labels / titles on the landing page */
export const SECTIONS = {
  about: { label: "Product" },
  audience: { label: "Audience", title: "ICP & pain points" },
  features: { label: "Features", title: "Seven modules, one proof" },
  contract: { label: "Proof contract", title: "What Dino guarantees" },
  cli: { label: "CLI", title: "Three commands" },
  pricing: { label: "Pricing", title: "Simple packs" },
  faq: { label: "FAQ", title: "FAQ" },
  docsHint: "Full docs",
  cliRef: "CLI reference ↗",
  cliHint:
    "--command takes argv tokens (echo ok). Quote the whole string when the program itself needs --flags.",
};
