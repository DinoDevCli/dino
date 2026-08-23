/** Documentary single-page copy — Problem → How → Architecture → Demo */

export const SITE = {
  version: "0.3.1",
  brand: "Dino",
};

/** Identity only — problem lives in SECTION 1 */
export const HERO = {
  prompt: "$ dino version",
  title: "Local-First Audit Engine for Python Pipelines",
  meta: "v0.3.1 · Early Access",
};

export const PROBLEM = {
  label: "# problem",
  lines: [
    "Two fraud-score runs — v1 and v2. You do not know what differs.",
    "Drift is invisible: no sealed artifacts, no machine-readable delta.",
    "CI cannot decide if a run changed. Audits stay manual and inconsistent.",
  ],
};

export const HOW = {
  label: "# how",
  body: "Dino seals each run into a proof bundle (capsule + scan + hash), exports the bundle (Path / HTTP / S3), builds a proof index (proof_index.json), and compares two proofs deterministically. The verdict is changed: true/false.",
};

/** Product core — definition once, then diagram; dashboard = consumer */
export const PRODUCT = {
  label: "# product",
  title: "Product Architecture",
  lines: [
    "Dino is a local-first audit engine for Python pipelines.",
    "It is not a platform, not a cloud service, not a workflow orchestrator — it runs locally and outputs deterministic audit artifacts.",
  ],
  /** Explicit boundary — immediately after the architecture diagram */
  noDashboard: [
    "Dino does not include a dashboard.",
    "It produces sealed proofs, export envelopes, and a universal proof index that your dashboards consume.",
  ],
  roles: "Engine in → Artifacts out → Dashboard renders.",
  flow: "pipeline → seal → export → index → compare → dashboard",
  blocks: [
    {
      step: "Seal",
      title: "proof.json",
      detail: "capsule + scan + hash",
    },
    {
      step: "Export",
      title: "Path / HTTP / S3",
      detail: "export.v1 envelope",
    },
    {
      step: "Index",
      title: "proof_index.json",
      detail: "metadata · metrics · layout",
    },
    {
      step: "Compare",
      title: "changed: true",
      detail: "pipeline_version_diff",
    },
    {
      step: "Dashboard",
      title: "Your UI",
      detail: "reads proof_index.json / compare.json · Superset / Airflow / Custom",
      consumer: true,
    },
  ],
};

export const DASHBOARD = {
  label: "# dashboard",
  title: "Dashboard Integration (bring your own UI)",
  lines: [
    "Dashboards read Dino's artifacts.",
    "proof_index.json and compare.json are designed for Superset, Airflow, MLflow, or your own UI.",
    "Dino outputs the data — you choose the visualization.",
  ],
  example:
    "Example: Superset reads proof_index.json via S3 or HTTP and renders drift charts.",
};

export const DEMO_COPY = {
  title: "Demo",
  intro:
    "This is a documentary walkthrough — readable without Play. All artifacts come from tests/simulation/golden.",
  resultNote:
    "exit 1 when changed — CI gate. Local: make demo in tests/simulation.",
  dashboardNote:
    "The demo shows the engine output. Dashboards are built on top of these artifacts.",
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
  note: "Early Access includes the engine and artifacts — dashboards are built by your team.",
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
