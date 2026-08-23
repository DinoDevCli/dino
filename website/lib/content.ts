/** Single-page landing copy — Hero → Problem → Engine → Live Demo → Early Access */

export const SITE = {
  version: "0.3.1",
  brand: "Dino",
  tagline: "Local-First Audit Engine for Python Pipelines",
  promise: "No SaaS. No Cloud. Only Proofs.",
  subtitle:
    "Deterministic proofs, export contracts, and a universal proof index for your dashboards.",
};

export const EARLY_ACCESS = {
  email: "early@dinodevcli.dev",
  banner:
    "Early Access: onboarding 5–10 teams · Free Team Keys · 60–90 days",
  days: "60–90 days",
};

export const NAV = [
  { href: "#problem", label: "Problem" },
  { href: "#engine", label: "Engine" },
  { href: "#demo", label: "Live Demo" },
  { href: "#early-access", label: "Early Access" },
  { href: "/docs", label: "Docs" },
];

export const MOMENT_OF_TRUTH =
  "Your ML model changes. Your features drift. Regulators ask questions. Dino gives you the deterministic proof.";

export const PROBLEM = {
  label: "The problem",
  title: "Risk, Fraud, and Research teams need audit trails — without a vendor dashboard.",
  body: "Non-deterministic runs, silent structural drift, and a dashboard gap leave governance teams without sealed evidence. Another hosted control plane is the wrong answer.",
  pains: [
    {
      title: "Non-deterministic runs",
      body: "Same inputs, different results — no sealed replay, no content-addressed hash.",
    },
    {
      title: "Structural drift",
      body: "Import graphs and pipeline versions change without a durable record.",
    },
    {
      title: "Dashboard gap",
      body: "Teams already have Superset, Airflow, MLflow — they need artifacts, not another UI.",
    },
  ],
};

export const ENGINE = {
  label: "The engine",
  title: "How Dino works",
  flow: `seal → export → proof_index.json → your dashboard`,
  contracts: [
    {
      id: "proof.json",
      schema: "dino.proof.bundle.v1",
      body: "Sealed run: capsule replay, leakage scan, content-addressed proof_hash.",
    },
    {
      id: "export.v1",
      schema: "dino.proof.export.v1",
      body: "Path / HTTP / S3 envelope your ingest API or archive can consume.",
    },
    {
      id: "index.v1",
      schema: "dino.proof.index.v1",
      body: "Universal listing + compare / metrics / layout for your dashboards.",
    },
  ],
  localFirst: [
    { title: "No data leaves", body: "Proofs stay on your machine, CI, or your own store." },
    { title: "No cloud dependency", body: "Offline by default. Export is your integration." },
    { title: "Deterministic proofs", body: "Same seal inputs → same proof_hash." },
  ],
};

export const DEMO = {
  label: "Live demo",
  title: "We audit a fraud-score pipeline",
  intro:
    "Two runs of the same decision pipeline — model v1 (seed 42) vs model v2 (seed 123). Dino seals each run, exports to an archive, then compares.",
  runA: {
    label: "Run A — fraud_score_v1",
    detail: "seed 42 · train path stable",
    hash: "fa7f1ccc86efbecd…",
  },
  runB: {
    label: "Run B — fraud_score_v2",
    detail: "seed 123 · pipeline version bump",
    hash: "fc4a30f5bca098f4…",
  },
  commands: [
    {
      label: "install",
      code: `pip install "git+https://github.com/DinoDevCli/dino.git@v0.3.1"`,
    },
    {
      label: "seal run A",
      code: `dino proof run \\
  --command "python pipeline/run.py --seed seed-42" \\
  --scan ./pipeline --output-dir ./proof_v1 \\
  --pipeline fraud_score_v1 --group risk-team --tag demo \\
  --export ./archive`,
    },
    {
      label: "seal run B",
      code: `dino proof run \\
  --command "python pipeline/run.py --seed seed-123" \\
  --scan ./pipeline --output-dir ./proof_v2 \\
  --pipeline fraud_score_v2 --group risk-team --tag demo \\
  --export ./archive`,
    },
    {
      label: "compare",
      code: `dino proof index compare ./archive \\
  fa7f1ccc86efbecd fc4a30f5bca098f4`,
    },
  ],
  proofExcerpt: `{
  "schema": "dino.proof.bundle.v1",
  "status": "partial",
  "proof_hash": "fa7f1ccc86efbecd47674a659b2a04e3…",
  "parts": {
    "capsule_replay_ok": true,
    "scan_ok": true,
    "drift_bucket": "aligned"
  },
  "audit": {
    "verdict": "PROOF_PARTIAL",
    "reasons": ["capsule_sealed", "scan_clean", "map_skipped"]
  }
}`,
  indexExcerpt: `{
  "schema": "dino.proof.index.v1",
  "proofs": [
    {
      "hash": "fc4a30f5bca098f4…",
      "pipeline": "fraud_score_v2",
      "group": "risk-team",
      "verdict": "PROOF_PARTIAL"
    },
    {
      "hash": "fa7f1ccc86efbecd…",
      "pipeline": "fraud_score_v1",
      "group": "risk-team",
      "verdict": "PROOF_PARTIAL"
    }
  ]
}`,
  compareExcerpt: `{
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
}`,
  compareCallout:
    "changed: true — pipeline_version_diff detects fraud_score_v1 → fraud_score_v2. That delta is the audit signal your dashboard or CI gate consumes.",
  makeHint: "Reproduce locally: make demo (tests/simulation) — golden files included.",
};

export const ACCESS = {
  label: "Early Access",
  title: "What you get",
  free: {
    name: "Free (forever)",
    items: [
      "Leakage scan for Python pipelines",
      "MIT core on GitHub",
      "No account, no cloud",
    ],
  },
  early: {
    name: "Early Access (60–90 days)",
    items: [
      "Full Proof pack — free Team Key",
      "proof run / verify / export (path · HTTP · S3)",
      "proof_index.json · compare · metrics · layout",
      "Team labels: --pipeline · --group · --tag",
      "Direct feedback channel with the maintainers",
    ],
  },
  checklist: [
    'Email early@dinodevcli.dev with subject "Early Access Request"',
    "Name your team / project (risk, fraud, ML governance, research)",
    "Receive a free Team Key",
    "Run: dino upgrade --pack proof --key YOUR_TEAM_KEY",
    "Start your first proof run against a real pipeline",
  ],
  cta: "Request Early Access",
  note: "Pricing will be introduced after Early Access. No checkout now.",
};

export const FAQ = [
  {
    q: "Is Dino a SaaS or dashboard?",
    a: "No. Dino is a local audit engine. It emits proof artifacts and contracts; you own dashboards and storage.",
  },
  {
    q: "How do I get Early Access?",
    a: "Email early@dinodevcli.dev or open a GitHub issue titled “Early Access Request”. We onboard 5–10 teams with free Team Keys.",
  },
  {
    q: "Does any data leave my environment?",
    a: "No — offline by default. Optional HTTP/S3 export targets your infrastructure, not a Dino cloud.",
  },
  {
    q: "Is Dino deterministic?",
    a: "Yes — content-addressed proof_hash and capsule replay within a sealed environment.",
  },
];

export const FOOTER = {
  line: "Early Access · MIT License · Local audit motor — not a platform.",
};

export const DOC_LINKS = [
  { label: "Proof Contract", path: "docs/PROOF_CONTRACT.md" },
  { label: "Proof Export", path: "docs/PROOF_EXPORT.md" },
  { label: "Proof Index", path: "docs/PROOF_INDEX.md" },
  { label: "CLI Reference", path: "docs/CLI_E2E_REFERENCE.md" },
  { label: "Examples", path: "docs/EXAMPLES.md" },
  { label: "Dashboard Integration", path: "docs/INTEGRATION_DASHBOARDS.md" },
  { label: "Production Simulation", path: "tests/simulation/README.md" },
];
