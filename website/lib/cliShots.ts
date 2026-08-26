/** Static CLI shots for the hero — golden excerpts, no autoplay GIF. */

export type CliShot = {
  id: string;
  tab: string;
  title: string;
  command: string;
  body: string;
  /** Ranges in `body` to accent (exact substrings). */
  accents?: string[];
};

export const CLI_SHOTS: CliShot[] = [
  {
    id: "seal",
    tab: "Seal",
    title: "dino · proof seal",
    command:
      'dino run \\\n  --command "python pipeline/run.py --seed seed-42" \\\n  --scan ./pipeline \\\n  --pipeline fraud_score_v1 \\\n  --export ./archive',
    body: `sealed fraud_score_v1
proof_dir  ./archive/b9f1892e7b78d78f
verdict    PROOF_PARTIAL
reasons    capsule_sealed, scan_clean, map_skipped`,
    accents: ["PROOF_PARTIAL", "sealed fraud_score_v1"],
  },
  {
    id: "compare",
    tab: "Compare",
    title: "dino · proof compare",
    command:
      "dino proof index compare ./archive <hash_v1> <hash_v2>",
    body: `{
  "schema": "dino.proof.index.compare.v1",
  "changed": true,
  "pipeline_version_diff": {
    "from": "fraud_score_v1",
    "to": "fraud_score_v2"
  },
  "verdict_diff": {
    "from": "PROOF_PARTIAL",
    "to": "PROOF_PARTIAL"
  }
}`,
    accents: ['"changed": true', "fraud_score_v1", "fraud_score_v2"],
  },
  {
    id: "index",
    tab: "Index",
    title: "dino · proof index",
    command: "dino proof index metrics ./archive",
    body: `{
  "schema": "dino.proof.index.metrics.v1",
  "total": 2,
  "passed": 2,
  "pipelines": [
    "fraud_score_v1",
    "fraud_score_v2"
  ]
}`,
    accents: ["fraud_score_v1", "fraud_score_v2"],
  },
];

export const CLI_SHOTS_CAPTION =
  "Static captures · tests/simulation/golden · fraud_score v1 → v2";
