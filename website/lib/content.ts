/** Documentary landing copy — aligned with README Free vs Proof Pack. */

export const SITE = {
  version: "1.0.0",
  brand: "Dino",
};

export const HERO = {
  eyebrow: "EARLY ACCESS · v1.0.0",
  title: "Same code, same data, same environment — different outputs?",
  subhead:
    "Dino seals every Python pipeline run into a proof, then tells you — deterministically — whether anything actually changed.",
  primaryCta: "Get started free",
  secondaryCta: "View on GitHub",
};

export const PROBLEM = {
  paragraphs: [
    "Two runs of the same pipeline. Same code, same data, same environment. Different outputs — and no way to prove why.",
    'Logs drift. Snapshots drift. Nobody can answer "did this actually change?" without re-reading everything by hand.',
  ],
};

export const HOW = {
  title: "Seal. Export. Compare.",
  steps: [
    {
      label: "Seal",
      detail: "`dino run` produces a content-addressed `proof.json`.",
    },
    {
      label: "Export",
      detail: "send it to Path, HTTP, or S3.",
    },
    {
      label: "Index",
      detail: "`proof_index.json` tracks every proof over time.",
    },
    {
      label: "Compare",
      detail: "`changed: true` or `false`. Deterministic, CI-friendly.",
    },
  ],
};

export const TIERS = {
  title: "Free vs Proof Pack",
  free: {
    header: "Free — Snapshot Mode",
    subhead: "Everything that runs locally, once, without history.",
    items: [
      "Run a sealed proof locally (`dino run`, `dino proof run`)",
      "Scan your code for leakage (`dino scan`)",
      "Replay a capsule locally (`dino capsule run`, `dino capsule replay`)",
    ],
    footer: "Free is for testing whether Dino detects drift in your pipeline.",
  },
  pack: {
    header: "Proof Pack — System Mode",
    subhead:
      "Everything that requires history, comparison, export, CI, or team metadata.",
    items: [
      "Proof index (compare, rebuild, metrics, layout)",
      "CI compare gate (exit 1 on drift)",
      "Export (Path + HTTP + S3)",
      "Bundle replay / verify / diff",
      "Map analyze / plan / drift / verify",
      "Team metadata (`--pipeline`, `--group`, `--tag`)",
      "Retention beyond 30 days",
    ],
    footer:
      "Proof Pack turns Dino from a snapshot tool into a pipeline stability system.",
  },
  requestKey: "Request a Team Key",
};

export const QUICKSTART = {
  title: "Quickstart",
  free: {
    label: "Free (Snapshot Mode)",
    code: `pip install "git+https://github.com/DinoDevCli/dino.git@v1.0.0"
dino scan .
dino run -- python my_pipeline.py`,
    note: "Not on PyPI as dino / dino-cli (name collision). Install from GitHub only.",
  },
  pack: {
    label: "Proof Pack (System Mode)",
    code: `dino upgrade --pack proof --key YOUR_KEY
dino proof index compare ./archive <HASH_A> <HASH_B>
dino proof export --proof-dir ./proof_out --to s3://my-bucket/proofs`,
    note: "Request a Team Key: dinodevcli@gmail.com",
  },
};

export const WHY = {
  title: "Why Dino?",
  intro: [
    "Python pipelines drift even when code, data, and the environment are identical.",
    "Dino seals each run and shows exactly what changed.",
  ],
  captureLabel: "It captures:",
  items: [
    {
      label: "Imports",
      detail: "which modules were loaded",
    },
    {
      label: "AST structure",
      detail: "how the code was parsed",
    },
    {
      label: "Data access",
      detail: "which files and inputs were touched",
    },
    {
      label: "Environment state",
      detail: "variables, versions, runtime context",
    },
    {
      label: "Artifacts",
      detail: "outputs produced by the run",
    },
    {
      label: "Runtime metadata",
      detail: "timing, seeds, execution details",
    },
  ],
  close:
    "Dino compares sealed runs with deterministic deltas — so you can see why two runs differ, not just that they differ.",
};

export const EARLY = {
  title: "Request a Team Key",
  line: "Start your 60-day Proof Pack trial. Email your team name to dinodevcli@gmail.com.",
  button: "Email for a Team Key",
  note: "Leakage scan stays free forever. Engine only — dashboards are external.",
};

export const SUPPORT =
  "Questions or issues? Open an Issue or Discussion on GitHub.";

export const DOC_LINKS = [
  { label: "Docs landing", path: "docs/index.md" },
  { label: "Engine contract", path: "docs/PROOF_CONTRACT.md" },
  { label: "Proof index", path: "docs/PROOF_INDEX.md" },
  { label: "Export envelopes", path: "docs/PROOF_EXPORT.md" },
  { label: "Quickstart", path: "docs/QUICKSTART.md" },
  { label: "Examples", path: "docs/EXAMPLES.md" },
  { label: "CLI reference", path: "docs/CLI_E2E_REFERENCE.md" },
  { label: "Licensing", path: "docs/LICENSING.md" },
];
