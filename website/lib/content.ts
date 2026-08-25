/** Documentary single-page copy — Problem → How → Product → Demo → Early Access */

export const SITE = {
  version: "1.0.0",
  brand: "Dino",
};

export const HERO = {
  kicker: "Version",
  title: "Local-First Audit Engine for Python Pipelines",
  definition:
    "Dino is a local-first audit engine that produces sealed proofs, export envelopes, and a universal proof index for your dashboards.",
  meta: "v1.0.0 · Early Access · CLI v1.0",
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
    "Dino outputs the data — you choose the visualization. Starter kit: examples/superset/drift_dashboard.yaml.",
  ],
};

/** Real install — not on PyPI as `dino` (name collision) */
export const QUICKSTART = {
  label: "Install",
  line: `pip install "git+https://github.com/DinoDevCli/dino.git@v1.0.0"`,
  hint: "dino --help · dino run --help",
};

/** Documentary CLI help epilog — keep wording verbatim */
export const CLI_EARLY_ACCESS = `---
Early Access (Proof Pack)
  CI compare gate · S3/HTTP backends · engine contract stability · team mode
  These features are not part of the open-source scan engine.

  Details & instructions:
    https://github.com/DinoDevCli/dino#early-access
    Contact: dinodevcli@gmail.com`;

export const CLI_GROUPS = {
  title: "CLI (v1.0)",
  core: ["dino run — alias for proof run", "dino proof — full proof chain", "dino scan — grammar + leakage"],
  pipeline: [
    "dino capsule",
    "dino bundle",
    "dino map",
    "dino verify",
    "dino flight",
  ],
  system: ["dino packs", "dino status", "dino upgrade", "dino version"],
  forms: [
    "dino run --scan ./pipeline -- python pipeline/run.py",
    "dino bundle create RUNDATA_PATH OUTPUT_PATH [--repo-root ROOT]",
    "dino proof index compare PATH HASH_A HASH_B",
  ],
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
  subtitle: "Request a Team Key — Start your 60-day Proof Pack trial.",
  steps: [
    "Email your team name to dinodevcli@gmail.com.",
    "Receive KEY.txt, Quickstart, and examples.",
    "dino upgrade --pack proof --key …",
  ],
  benefits: [
    "Leakage scan — free forever",
    "Proof pack — free Team Key, 60 days",
  ],
  note: "Engine only — dashboards are external.",
  cta: "Request a Team Key",
  email: "dinodevcli@gmail.com",
  flow: "Email your team name to dinodevcli@gmail.com.",
};

export const LICENSING = {
  title: "Pricing & Licensing",
  lead: "MIT core. Proof Pack license after Early Access.",
  lines: [
    "Dino is MIT-licensed.",
    "The core engine is free.",
    "Advanced audit features (Proof Pack) require a license.",
    "After Early Access, Proof Pack will be available as a one-time purchase per seat or team.",
    "No subscriptions. No cloud fees.",
  ],
};

export const CODESPACES = {
  label: "Try it",
  title: "Open in GitHub Codespaces",
  body: "Clones the repo, installs Python and Dino, and opens a terminal. Then: cd tests/simulation && make demo",
  cta: "Open in GitHub Codespaces",
};

export const SUPPORT =
  "Questions or issues? Open an Issue or Discussion on GitHub.";

export const ROADMAP_DEV =
  "Shipped: dino --dev relaxes EMPTY_SCAN_ROOTS for local iteration. Production proofs stay fail-closed. CLI v1.0: dino run + grouped --help + Early Access (Proof Pack) block.";

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
    command: `dino run \\
  --scan ./pipeline \\
  --pipeline fraud_score_v1 \\
  --export ./archive \\
  -- python pipeline/run.py --seed seed-42`,
    artifacts: [{ name: "proof.json", json: GOLDEN_PROOF }],
  },
  {
    id: "run-b",
    label: "Run B — updated",
    command: `dino run \\
  --scan ./pipeline \\
  --pipeline fraud_score_v2 \\
  --export ./archive \\
  -- python pipeline/run.py --seed seed-123`,
    artifacts: [
      { name: "proof.json", json: GOLDEN_PROOF },
      { name: "proof_index.json", json: GOLDEN_INDEX },
    ],
  },
  {
    id: "compare",
    label: "Compare",
    command: `dino proof index compare ./archive <HASH_A> <HASH_B>`,
    artifacts: [{ name: "compare.json", json: GOLDEN_COMPARE, emphasize: true }],
  },
  {
    id: "fail-closed",
    label: "Fail-closed",
    command: `dino run --scan ./does_not_exist -- echo ok`,
    note: "Dino refuses to pass a run with missing scan roots. For local iteration only: dino --dev …",
    artifacts: [{ name: "scan.json", json: FAIL_SNIPPET }],
  },
];

export const DOC_LINKS = [
  { label: "Engine", path: "docs/PROOF_CONTRACT.md" },
  { label: "Proof Pack", path: "docs/index.md#proof-pack" },
  { label: "Contracts", path: "docs/PROOF_INDEX.md" },
  { label: "Quickstart", path: "docs/QUICKSTART.md" },
  { label: "Examples", path: "docs/EXAMPLES.md" },
  { label: "Early Access", path: "docs/index.md#early-access" },
  { label: "Pricing & Licensing", path: "docs/LICENSING.md" },
  { label: "Roadmap", path: "docs/ROADMAP.md" },
  { label: "Dashboard Integration", path: "docs/INTEGRATION_DASHBOARDS.md" },
  { label: "CLI Reference", path: "docs/CLI_E2E_REFERENCE.md" },
];
