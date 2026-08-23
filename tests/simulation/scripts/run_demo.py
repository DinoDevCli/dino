#!/usr/bin/env python3
"""One-shot demo: seal fraud_score_v1 + v2, compare, optionally write golden files."""

from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", required=True)
    parser.add_argument("--pipeline", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--golden", type=Path, required=True)
    parser.add_argument("--write-golden", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(root))

    from dino.early_access import issue_key
    from dino.license import DEFAULT_LICENSE, activate_pack, save_license
    import dino.license as lic

    lic_dir = args.work / ".dino"
    lic_dir.mkdir(parents=True, exist_ok=True)
    lic.LICENSE_DIR = lic_dir
    lic.LICENSE_PATH = lic_dir / "license.json"
    save_license(dict(DEFAULT_LICENSE))
    activate_pack("proof", key=issue_key(team="demo", days=30))

    # Local CLI runner (same envelope unwrap as tests)
    import io
    from contextlib import redirect_stderr, redirect_stdout
    from dino.cli import main as dino_main

    def run(argv: list[str]) -> tuple[int, dict]:
        cmd = ["--json", *argv]
        out, err = io.StringIO(), io.StringIO()
        old = list(sys.argv)
        try:
            sys.argv = ["dino", *cmd]
            with redirect_stdout(out), redirect_stderr(err):
                code = dino_main(cmd)
        finally:
            sys.argv = old
        text = out.getvalue().strip()
        payload: dict = {}
        if text.startswith("{"):
            raw = json.loads(text)
            payload = raw.get("result") or raw.get("error") or raw
        return int(code), payload

    pipe = args.pipeline.resolve()
    run_py = pipe / "run.py"
    args.archive.mkdir(parents=True, exist_ok=True)

    hashes: dict[str, str] = {}
    for name, seed in (("v1", "seed-42"), ("v2", "seed-123")):
        work = args.work / name
        work.mkdir(parents=True, exist_ok=True)
        proof = args.work / f"proof_{name}"
        proof.mkdir(parents=True, exist_ok=True)
        cmd = shlex.join(
            [
                args.python,
                str(run_py),
                "--workdir",
                str(work),
                "--rows",
                "200",
                "--seed",
                seed,
            ]
        )
        code, payload = run(
            [
                "proof",
                "run",
                "--command",
                cmd,
                "--scan",
                str(pipe),
                "--output-dir",
                str(proof),
                "--pipeline",
                f"fraud_score_{name}",
                "--group",
                "risk-team",
                "--tag",
                "demo",
                "--export",
                str(args.archive),
            ]
        )
        if code != 0:
            print(f"proof run {name} failed: {payload}", file=sys.stderr)
            return code
        hashes[name] = str(payload["proof_hash"])
        print(f"sealed fraud_score_{name}  hash={hashes[name][:16]}…")

    code, cmp = run(
        ["proof", "index", "compare", str(args.archive), hashes["v1"], hashes["v2"]]
    )
    print(f"compare changed={cmp.get('changed')}  exit={code}")
    if cmp.get("pipeline_version_diff"):
        print(f"  pipeline: {cmp['pipeline_version_diff']}")

    code, metrics = run(["proof", "index", "metrics", str(args.archive)])
    print(f"metrics total={metrics.get('total')} pipelines={metrics.get('pipelines')}")

    index = json.loads((args.archive / "proof_index.json").read_text(encoding="utf-8"))
    proof_v1 = json.loads(
        (args.work / "proof_v1" / "proof.json").read_text(encoding="utf-8")
    )

    golden_payload = {
        "proof_excerpt": {
            "schema": proof_v1["schema"],
            "status": proof_v1["status"],
            "audit": proof_v1["audit"],
            "parts": {
                "capsule_replay_ok": proof_v1["parts"].get("capsule_replay_ok"),
                "scan_ok": proof_v1["parts"].get("scan_ok"),
                "drift_bucket": proof_v1["parts"].get("drift_bucket"),
            },
        },
        "index_excerpt": {
            "schema": index["schema"],
            "proof_count": len(index["proofs"]),
            "pipelines": sorted(
                {p.get("pipeline") for p in index["proofs"] if p.get("pipeline")}
            ),
        },
        "compare_excerpt": {
            "schema": cmp.get("schema"),
            "changed": cmp.get("changed"),
            "pipeline_version_diff": cmp.get("pipeline_version_diff"),
            "drift_delta": cmp.get("drift_delta"),
            "verdict_diff": cmp.get("verdict_diff"),
        },
        "metrics_excerpt": {
            "schema": metrics.get("schema"),
            "total": metrics.get("total"),
            "passed": metrics.get("passed"),
            "pipelines": metrics.get("pipelines"),
        },
    }

    if args.write_golden:
        args.golden.mkdir(parents=True, exist_ok=True)
        path = args.golden / "demo_excerpts.json"
        path.write_text(json.dumps(golden_payload, indent=2, sort_keys=True) + "\n")
        print(f"wrote golden {path}")
    elif (args.golden / "demo_excerpts.json").is_file():
        expected = json.loads(
            (args.golden / "demo_excerpts.json").read_text(encoding="utf-8")
        )
        # Compare stable schema fields (not absolute hashes — absolute paths differ)
        for key in ("proof_excerpt", "compare_excerpt", "metrics_excerpt", "index_excerpt"):
            exp = expected.get(key) or {}
            got = golden_payload.get(key) or {}
            for field in ("schema", "changed", "status", "total", "passed", "proof_count"):
                if field in exp and exp[field] != got.get(field):
                    print(
                        f"GOLDEN MISMATCH {key}.{field}: {got.get(field)!r} != {exp[field]!r}",
                        file=sys.stderr,
                    )
                    return 1
            if exp.get("pipeline_version_diff") != got.get("pipeline_version_diff"):
                print("GOLDEN MISMATCH pipeline_version_diff", file=sys.stderr)
                return 1
            if exp.get("pipelines") != got.get("pipelines"):
                print(
                    f"GOLDEN MISMATCH pipelines: {got.get('pipelines')} != {exp.get('pipelines')}",
                    file=sys.stderr,
                )
                return 1
        print("golden check: OK")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
