/** Site copy + demo transcript for TerminalPlayer */

export const SITE = {
  version: "0.3.1",
  brand: "Dino",
};

export const HERO = {
  badge: "v0.3.1 · Early Access",
  line1: "Local-First",
  line2: "Audit Engine",
  subtitle:
    "Deterministic proofs, export contracts, and a universal proof index for your Python pipelines.",
  footnote: "MIT · GitHub · Python 3.10+",
};

export const PROBLEM_SOLUTION = {
  problemLabel: "# problem",
  problemTitle: "Pipelines are black boxes.",
  problemBody:
    "Non-deterministic runs, silent drift, and no standard audit trail. Every team builds its own fragile workaround.",
  solutionLabel: "# solution",
  solutionTitle: "Dino is the engine.",
  solutionBody:
    "Seal. Export. Index. Deterministic. Local. Reproducible. One universal format for every dashboard.",
};

export const FLOW = [
  {
    step: "1 · Seal",
    title: "proof.json",
    detail: "Capsule + Scan + Hash",
    accent: true,
  },
  {
    step: "2 · Export",
    title: "export.v1",
    detail: "Path / HTTP / S3",
    accent: true,
  },
  {
    step: "3 · Index",
    title: "proof_index.json",
    detail: "Compare · Metrics · Layout",
    accent: true,
  },
  {
    step: "4 · Dashboard",
    title: "Your UI",
    detail: "Superset / Airflow / Custom",
    accent: false,
  },
];

export const USPS = [
  {
    label: "Local-First",
    icon: "L",
    title: "No cloud. No platform.",
    body: "No data leaves your infrastructure. Offline by default.",
  },
  {
    label: "Deterministic",
    icon: "D",
    title: "Content-addressed proof_hash.",
    body: "Same seal inputs → same hash. Capsule replay included.",
  },
  {
    label: "Universal Index",
    icon: "I",
    title: "Dashboard-ready JSON.",
    body: "proof_index.json — one format for every consumer.",
  },
  {
    label: "Export Contracts",
    icon: "E",
    title: "Path / HTTP / S3.",
    body: "dino.proof.export.v1 into your store or ingest API.",
  },
  {
    label: "Compare & Metrics",
    icon: "C",
    title: "Drift between runs.",
    body: "pipeline · verdict · leakage · artifacts deltas for CI gates.",
  },
];

/** Line-by-line transcript for the embedded terminal player */
export const DEMO_LINES = [
  "$ dino proof run --command \"python pipeline/run.py --seed seed-42\" \\",
  "    --scan ./pipeline --pipeline fraud_score_v1 \\",
  "    --group risk-team --tag demo --export ./archive",
  "",
  "sealed  fraud_score_v1",
  "proof_hash  fa7f1ccc86efbecd47674a659b2a04e3…",
  "export     ./archive/fa7f1ccc86efbecd/",
  "index      proof_index.json updated",
  "",
  "$ dino proof run --command \"python pipeline/run.py --seed seed-123\" \\",
  "    --scan ./pipeline --pipeline fraud_score_v2 \\",
  "    --group risk-team --tag demo --export ./archive",
  "",
  "sealed  fraud_score_v2",
  "proof_hash  fc4a30f5bca098f4d3665242785ef779…",
  "export     ./archive/fc4a30f5bca098f4/",
  "index      proof_index.json updated",
  "",
  "$ dino proof index compare ./archive fa7f1ccc86efbecd fc4a30f5bca098f4",
  "",
  "{",
  '  "schema": "dino.proof.index.compare.v1",',
  '  "changed": true,',
  '  "pipeline_version_diff": {',
  '    "from": "fraud_score_v1",',
  '    "to": "fraud_score_v2"',
  "  },",
  '  "drift_delta": { "from": "none", "to": "none" }',
  "}",
  "",
  "# exit 1 — changed: true  (CI gate signal)",
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
