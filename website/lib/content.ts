/** Documentary single-page copy — Problem → How → Product → Demo → Early Access */

export const SITE = {
  version: "0.3.1",
  brand: "Dino",
};

export const HERO = {
  kicker: "Version",
  title: "Local-First Audit Engine for Python Pipelines",
  definition:
    "Dino is a local-first audit engine that produces sealed proofs, export envelopes, and a universal proof index for your dashboards.",
  meta: "v0.3.1 · Early Access",
};

export const PROBLEM = {
  title: "Problem",
  lead: "Two fraud-score runs — v1 and v2.",
  lines: [
    "You do not know what differs. Drift is invisible: no sealed artifacts, no machine-readable delta.",
    "CI cannot decide if a run changed. Audits stay manual and inconsistent.",
  ],
};

export const HOW = {
  title: "How it works",
  lead: "Seal. Export. Index. Compare.",
  body: "Dino seals each run into a proof bundle (capsule + scan + hash), exports the bundle (Path / HTTP / S3), builds a proof index (proof_index.json), and compares two proofs deterministically. The verdict is changed: true/false.",
};

export const PRODUCT = {
  title: "Engine",
  lead: "pipeline → seal → export → index → compare → dashboard",
  determinism:
    "All proof bundles and indexes are deterministic and reproducible (content-addressed).",
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
  wiringTitle: "Dashboard integration",
  wiring: [
    "Dashboards consume Dino's artifacts (proof_index.json, compare.json) via Path, HTTP, or S3.",
    "Superset, Airflow, MLflow, or your own UI can render drift, verdicts, and metrics.",
    "Dino outputs the data — you choose the visualization.",
  ],
};

/** Real install — not on PyPI as `dino` (name collision) */
export const QUICKSTART = {
  label: "Install",
  line: `pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.1"`,
  hint: "dino proof run --help",
};

export const DEMO_COPY = {
  title: "Demo: Audit Log",
  intro:
    "We audit a fraud-score pipeline. Two runs — v1 and v2. Dino seals both, exports them, builds a proof index, and compares them. The walkthrough shows the exact diff.",
  source:
    "All demo artifacts come from tests/simulation/golden in the GitHub repository.",
};

export const EARLY = {
  title: "Early Access",
  subtitle: "Free Mode. Proof Pack. 60 Days.",
  benefits: [
    "Leakage scan — free forever",
    "Proof pack — free Team Key, 60 days",
    "Email dinodevcli@gmail.com — name your team or project",
  ],
  note: "Engine only — dashboards are external.",
  cta: "Request a Team Key",
  email: "dinodevcli@gmail.com",
};

/** From tests/simulation/golden/demo_excerpts.json — do not invent */
export const GOLDEN_PROOF = `{
  "audit": {
    "reasons": [
      "capsule_sealed",
      "scan_clean",
      "map_skipped"
    ],
    "summary": "Capsule sealed; one or more optional parts were skipped.",
    "verdict": "PROOF_PARTIAL"
  },
  "parts": {
    "capsule_replay_ok": true,
    "drift_bucket": "aligned",
    "scan_ok": true
  },
  "schema": "dino.proof.bundle.v1",
  "status": "partial"
}`;

export const GOLDEN_INDEX = `{
  "pipelines": [
    "fraud_score_v1",
    "fraud_score_v2"
  ],
  "proof_count": 2,
  "schema": "dino.proof.index.v1"
}`;

export const GOLDEN_COMPARE = `{
  "changed": true,
  "drift_delta": {
    "from": "none",
    "to": "none"
  },
  "pipeline_version_diff": {
    "from": "fraud_score_v1",
    "to": "fraud_score_v2"
  },
  "schema": "dino.proof.index.compare.v1",
  "verdict_diff": {
    "from": "PROOF_PARTIAL",
    "to": "PROOF_PARTIAL"
  }
}`;

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
    id: "run-a",
    label: "Run A — baseline",
    command: `dino proof run \\
  --command "python pipeline/run.py --seed seed-42" \\
  --scan ./pipeline \\
  --pipeline fraud_score_v1 \\
  --export ./archive`,
    artifacts: [{ name: "proof.json", json: GOLDEN_PROOF }],
  },
  {
    id: "run-b",
    label: "Run B — updated",
    command: `dino proof run \\
  --command "python pipeline/run.py --seed seed-123" \\
  --scan ./pipeline \\
  --pipeline fraud_score_v2 \\
  --export ./archive`,
    artifacts: [
      { name: "proof.json", json: GOLDEN_PROOF },
      { name: "proof_index.json", json: GOLDEN_INDEX },
    ],
  },
  {
    id: "compare",
    label: "Compare",
    command: `dino proof index compare ./archive <hash_v1> <hash_v2>`,
    artifacts: [{ name: "compare.json", json: GOLDEN_COMPARE, emphasize: true }],
  },
  {
    id: "fail-closed",
    label: "Fail-closed",
    command: `dino proof run --command "echo ok" --scan ./does_not_exist`,
    note: "Dino refuses to pass a run with missing scan roots.",
    artifacts: [{ name: "scan.json", json: FAIL_SNIPPET }],
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
