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
    "Two fraud-score runs — v1 and v2.",
    "How do they differ? Why is drift happening?",
    "Without sealed proofs and compare, the answer is guesswork.",
  ],
};

export const HOW = {
  label: "# how",
  body: "Dino seals each run (proof.json), exports it (export.v1), indexes it (proof_index.json), and compares two proofs. The result is a deterministic verdict: changed: true/false.",
};

/** Product core — diagram only, no prose */
export const ARCHITECTURE = {
  label: "# architecture",
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
      detail: "compare · metrics · layout",
    },
    {
      step: "Compare",
      title: "changed: true",
      detail: "pipeline_version_diff",
    },
  ],
};

export const DEMO_COPY = {
  title: "Demo",
  intro:
    "fraud_score_v1 → fraud_score_v2. Golden excerpts from tests/simulation/golden.",
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
