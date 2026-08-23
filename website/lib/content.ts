/** Documentary single-page copy — walkthrough first, golden artifacts */

export const SITE = {
  version: "0.3.1",
  brand: "Dino",
};

/** Static CLI prompt — muted only, no animation */
export const HERO = {
  prompt: "$ dino version",
  title: "Local-First Audit Engine",
  subtitle: "How did fraud_score change between v1 and v2?",
  meta: "v0.3.1 · Early Access · MIT · Python 3.10+",
};

export const PROBLEM_SOLUTION = {
  problemLabel: "# problem",
  problemTitle: "How does fraud_score v1 differ from v2?",
  problemBody:
    "You shipped a new seed, a new pipeline label, maybe a new feature set. Regulators and risk ask: what changed? Without a sealed proof and compare, the answer is guesswork.",
  solutionLabel: "# solution",
  solutionTitle: "Seal both runs. Read changed: true.",
  solutionBody:
    "Dino seals each run into proof.json, exports into an archive, and compares. pipeline_version_diff and artifact deltas are the audit signal — not a vendor dashboard.",
};

export const FLOW = [
  {
    step: "1. Seal",
    title: "proof.json",
    detail: "Capsule + Scan + Hash",
    accent: true,
  },
  {
    step: "2. Export",
    title: "export.v1",
    detail: "Path / HTTP / S3",
    accent: true,
  },
  {
    step: "3. Index",
    title: "proof_index.json",
    detail: "Compare · Metrics · Layout",
    accent: true,
  },
  {
    step: "4. Dashboard",
    title: "Your UI",
    detail: "Superset / Airflow / Custom",
    accent: false,
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
    title: "Content-addressed proof_hash.",
    body: "Every sealed run is reproducible.",
  },
  {
    label: "Universal Index",
    title: "Dashboard-ready JSON.",
    body: "One format for every consumer.",
  },
  {
    label: "Export Contracts",
    title: "Path / HTTP / S3.",
    body: "Integrate anywhere you already store artifacts.",
  },
];

export const USP_WIDE = {
  label: "Compare & Metrics",
  title: "Why is changed: true?",
  body: "pipeline_version_diff, verdict_diff, leakage, artifacts — the fields your CI gate reads.",
};

export const DEMO_COPY = {
  title: "Live Demo",
  intro:
    "We audit a fraud-score pipeline. Two runs — v1 and v2. Dino shows the diff.",
  resultLabel: "# result",
  resultNote:
    "exit 1 when changed — use as a CI gate. Reproduce locally: make demo in tests/simulation.",
  replayLabel: "# replay (optional)",
  replayHint: "Same session, slow line reveal. Walkthrough above is the source of truth.",
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

export const DEMO_STEPS = [
  {
    title: "# 1. Run A — baseline fraud_score_v1",
    command: `dino proof run \\
  --command "python pipeline/run.py --seed seed-42" \\
  --scan ./pipeline \\
  --pipeline fraud_score_v1 \\
  --group risk-team --tag demo \\
  --export ./archive`,
    explanation:
      "→ Seals the baseline run. Capsule replay + leakage scan land in proof.json (golden excerpt below).",
    artifactExcerpt: GOLDEN_PROOF,
  },
  {
    title: "# 2. Run B — fraud_score_v2 (new seed)",
    command: `dino proof run \\
  --command "python pipeline/run.py --seed seed-123" \\
  --scan ./pipeline \\
  --pipeline fraud_score_v2 \\
  --group risk-team --tag demo \\
  --export ./archive`,
    explanation:
      "→ Second seal into the same archive. proof_index.json now lists both pipelines.",
    artifactExcerpt: GOLDEN_INDEX,
  },
  {
    title: "# 3. Compare — what changed?",
    command: `dino proof index compare ./archive \\
  <hash_v1> <hash_v2>`,
    explanation:
      "→ changed: true because pipeline_version_diff moves fraud_score_v1 → fraud_score_v2.",
    artifactExcerpt: GOLDEN_COMPARE,
  },
  {
    title: "# 4. Fail-closed — empty scan roots",
    command: `dino proof run \\
  --command "echo ok" \\
  --scan ./does_not_exist \\
  --output-dir ./proof_out`,
    explanation:
      "→ Dino refuses a silent pass. EMPTY_SCAN_ROOTS / fail-closed — no proof without a real scan target.",
    artifactExcerpt: `{
  "ok": false,
  "type": "EMPTY_SCAN_ROOTS",
  "message": "scan roots resolved to zero .py files"
}`,
  },
];

/** Replay transcript — same story, for slow TerminalPlayer */
export const DEMO_LINES = [
  "# replay — fraud_score v1 then v2, then compare",
  "",
  "$ dino proof run --command \"python pipeline/run.py --seed seed-42\" \\",
  "    --scan ./pipeline --pipeline fraud_score_v1 --export ./archive",
  "sealed  fraud_score_v1  status=partial  scan_ok=true",
  "",
  "$ dino proof run --command \"python pipeline/run.py --seed seed-123\" \\",
  "    --scan ./pipeline --pipeline fraud_score_v2 --export ./archive",
  "sealed  fraud_score_v2  status=partial  scan_ok=true",
  "",
  "$ dino proof index compare ./archive <hash_v1> <hash_v2>",
  'changed: true',
  'pipeline_version_diff: fraud_score_v1 → fraud_score_v2',
  "",
  "# exit 1 — CI gate signal",
];

export const QUICKSTART = `pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.1"

dino proof run \\
  --command "python3 train.py" \\
  --scan ./src \\
  --output-dir ./proof_out \\
  --export ./archive`;

export const EARLY = {
  label: "# early access",
  title: "Free Mode. Proof Pack. 60 Days.",
  body: "Leakage scan stays free forever. The full Proof pack (index, export, compare) is free for 60 days for Early Access teams.",
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
