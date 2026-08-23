/** Documentary single-page copy — walkthrough first, golden artifacts */

export const SITE = {
  version: "0.3.1",
  brand: "Dino",
};

/** Static CLI prompt — muted only, no animation */
export const HERO = {
  prompt: "$ dino version",
  title: "Local-First Audit Engine for Python Pipelines",
  subtitle: "How did fraud_score change between v1 and v2?",
  meta: "v0.3.1 · Early Access",
};

export const PROBLEM_SOLUTION = {
  problemLabel: "# problem",
  problemTitle: "Two fraud-score runs — v1 and v2.",
  problemBody:
    "How do they differ? Why is drift happening? Without a sealed proof and compare, the answer is guesswork.",
  solutionLabel: "# solution",
  solutionTitle: "Seal both. Export. Diff.",
  solutionBody:
    "Dino seals both runs, exports them, and shows the diff — pipeline_version_diff, verdict, artifacts.",
};

export const FLOW = [
  {
    icon: "🛡",
    step: "Seal",
    title: "proof.json",
    detail: "Capsule + Scan + Hash",
  },
  {
    icon: "📦",
    step: "Export",
    title: "Path / HTTP / S3",
    detail: "export.v1 envelope",
  },
  {
    icon: "📊",
    step: "Index",
    title: "proof_index.json",
    detail: "Compare · Metrics · Layout",
  },
  {
    icon: "📈",
    step: "Dashboard",
    title: "Your UI",
    detail: "Superset / Airflow / Custom",
  },
];

export const USPS = [
  {
    label: "Local-First",
    title: "No cloud. No platform.",
    body: "No data leaves your infrastructure.",
  },
  {
    label: "Deterministic",
    title: "proof_hash",
    body: "Content-addressed. Every sealed run is reproducible.",
  },
  {
    label: "Universal Index",
    title: "proof_index.json",
    body: "One dashboard-ready format for every consumer.",
  },
  {
    label: "Export Contracts",
    title: "Path / HTTP / S3",
    body: "Integrate where you already store artifacts.",
  },
  {
    label: "Compare / Metrics",
    title: "changed: true",
    body: "pipeline_version_diff, verdict_diff, leakage, artifacts.",
  },
];

export const DEMO_COPY = {
  title: "Demo",
  intro:
    "fraud_score_v1 → fraud_score_v2. Walkthrough below — readable without Play. Artifacts from tests/simulation/golden.",
  resultLabel: "# result",
  resultNote:
    "exit 1 when changed — CI gate. Local: make demo in tests/simulation.",
};

/** From tests/simulation/golden/demo_excerpts.json — do not invent */
const GOLDEN_PROOF = `{
  "schema": "dino.proof.bundle.v1",
  "status": "partial",
  "parts": {
    "capsule_replay_ok": true,
    "scan_ok": true,
    "drift_bucket": "aligned"
  },
  "audit": {
    "verdict": "PROOF_PARTIAL",
    "reasons": ["capsule_sealed", "scan_clean", "map_skipped"]
  }
}`;

const GOLDEN_COMPARE = `{
  "schema": "dino.proof.index.compare.v1",
  "changed": true,
  "pipeline_version_diff": {
    "from": "fraud_score_v1",
    "to": "fraud_score_v2"
  },
  "drift_delta": { "from": "none", "to": "none" },
  "verdict_diff": {
    "from": "PROOF_PARTIAL",
    "to": "PROOF_PARTIAL"
  }
}`;

const GOLDEN_INDEX = `{
  "schema": "dino.proof.index.v1",
  "proof_count": 2,
  "pipelines": ["fraud_score_v1", "fraud_score_v2"]
}`;

export const DEMO_RESULT = GOLDEN_COMPARE;

export const FAIL_SNIPPET = `{
  "ok": false,
  "files_scanned": 0,
  "findings": [{
    "rule": "EMPTY_SCAN_ROOTS",
    "detail": "no .py files under scan roots",
    "severity": "FAIL"
  }]
}`;

export const DEMO_STEPS = [
  {
    title: "Run A — fraud_score_v1",
    command: `dino proof run \\
  --command "python pipeline/run.py --seed seed-42" \\
  --scan ./pipeline \\
  --pipeline fraud_score_v1 \\
  --export ./archive`,
    explanation:
      "Seals the baseline run. Capsule replay + leakage scan land in proof.json (golden excerpt).",
    artifactExcerpt: GOLDEN_PROOF,
  },
  {
    title: "Run B — fraud_score_v2",
    command: `dino proof run \\
  --command "python pipeline/run.py --seed seed-123" \\
  --scan ./pipeline \\
  --pipeline fraud_score_v2 \\
  --export ./archive`,
    explanation:
      "Second seal into the same archive. proof_index.json lists both pipelines.",
    artifactExcerpt: GOLDEN_INDEX,
  },
  {
    title: "Compare",
    command: `dino proof index compare ./archive <hash_v1> <hash_v2>`,
    explanation:
      "Shows the diff. changed: true because pipeline_version_diff moves fraud_score_v1 → fraud_score_v2.",
    artifactExcerpt: GOLDEN_COMPARE,
  },
  {
    title: "Fail-closed",
    command: `dino proof run --command "echo ok" --scan ./does_not_exist`,
    explanation:
      "EMPTY_SCAN_ROOTS — no silent pass without a real scan target.",
    artifactExcerpt: FAIL_SNIPPET,
  },
];

export const EARLY = {
  label: "# early access",
  title: "Free Mode. Proof Pack. 60 Days.",
  body: "Leakage scan stays free forever. Proof / index / export free for 60 days for Early Access teams. Email early@dinodevcli.dev — team or project name — receive a Team Key.",
  email: "early@dinodevcli.dev",
};

export const DOC_LINKS = [
  { label: "Proof Contract", path: "docs/PROOF_CONTRACT.md" },
  { label: "Proof Export", path: "docs/PROOF_EXPORT.md" },
  { label: "Proof Index", path: "docs/PROOF_INDEX.md" },
  { label: "CLI Reference", path: "docs/CLI_E2E_REFERENCE.md" },
  { label: "Examples", path: "docs/EXAMPLES.md" },
  { label: "Dashboard Integration", path: "docs/INTEGRATION_DASHBOARDS.md" },
  { label: "Production Simulation", path: "tests/simulation/README.md" },
  { label: "Website Blueprint", path: "docs/internal/WEBSITE_BLUEPRINT.md" },
];
