/** Documentary single-page copy — Problem → How → Product → Demo → Early Access */

export const SITE = {
  version: "0.3.1",
  brand: "Dino",
};

export const HERO = {
  prompt: "$ dino version",
  title: "Local-First Audit Engine for Python Pipelines",
  definition:
    "Dino is a local-first audit engine that produces sealed proofs, export envelopes, and a universal proof index for your dashboards.",
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

export const PRODUCT = {
  label: "# product",
  title: "Product Architecture",
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
  ],
  noDashboard:
    "Dino does not include a dashboard — dashboards consume the artifacts (proof_index.json, compare.json).",
  roles: "Dino outputs audit artifacts — dashboards render them.",
  repoBridge:
    "The website demo uses the same artifacts found in tests/simulation/golden in the GitHub repository.",
  wiringLabel: "Dashboard Integration",
  wiring: [
    "Dashboards read Dino's artifacts via Path, HTTP, or S3.",
    "Superset, Airflow, MLflow, or your own UI can render drift, verdicts, and metrics.",
    "Dino provides the data — you choose the visualization.",
  ],
  benefits: [
    "Deterministic CI gate: changed: true/false",
    "Local-first — data never leaves your infra",
  ],
};

/** Real install — not on PyPI as `dino` (name collision) */
export const QUICKSTART = {
  label: "# install",
  line: `pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.1"`,
  hint: "Then: dino scan leakage --help · dino proof run --help",
};

export const DEMO_COPY = {
  title: "Demo",
  intro:
    "Documentary walkthrough — real commands, real hashes, real JSON. Readable without pressing Play.",
  resultNote:
    "exit 1 when changed — CI gate. Local: make demo in tests/simulation.",
};

export const EARLY = {
  label: "# early access",
  title: "Free Mode. Proof Pack. 60 Days.",
  benefits: [
    "Leakage scan — free forever",
    "Proof / index / export — free for 60 days",
    "Team Key by email — name your team or project",
  ],
  note: "Engine only — dashboards are external.",
  cta: "Request a Team Key",
  email: "early@dinodevcli.dev",
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
