#!/usr/bin/env python3
"""Public binary attestation verify — stdlib graph replay, no external OS package."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from dino.common.determinism import canonical_hash

VERIFY_SCHEMA = "dino_verify_binary_v1"


def _trust_surface(att: dict[str, Any]) -> dict[str, Any]:
    return att.get("trust_surface") or {}


def _extract_hashes(att: dict[str, Any]) -> dict[str, str]:
    ts = _trust_surface(att)
    validation = att.get("validation") or {}
    policy = att.get("policy") or validation.get("policy") or {}
    return {
        "H_verdict": str(ts.get("H_verdict") or att.get("H_verdict") or ""),
        "compiler_graph_hash": str(
            att.get("compiler_graph_hash")
            or ts.get("compiler_graph_hash")
            or att.get("graph_hash")
            or ts.get("graph_hash")
            or ""
        ),
        "pipeline_hash": str(att.get("pipeline_hash") or ts.get("pipeline_hash") or ""),
        "policy_verdict_hash": str(
            policy.get("policy_verdict_hash") or ts.get("policy_verdict_hash") or ""
        ),
    }


def compile_repo_stdlib(repo: Path) -> dict[str, Any]:
    nodes: list[dict[str, str]] = []
    skip = {".git", "__pycache__", ".venv", "node_modules", "dist", "build"}
    exts = {".py": "python", ".go": "go", ".java": "java", ".ts": "typescript", ".tf": "terraform"}
    for path in sorted(repo.rglob("*")):
        if not path.is_file():
            continue
        if any(part in skip for part in path.parts):
            continue
        if path.suffix not in exts:
            continue
        rel = str(path.relative_to(repo))
        nodes.append({"node_id": f"file:{rel}", "path": rel, "language": exts[path.suffix]})
    nodes.sort(key=lambda x: x["node_id"])
    graph_hash = canonical_hash({"compiler_graph_v1": {"nodes": nodes, "edges": []}})
    return {"graph_hash": graph_hash, "node_count": len(nodes), "edge_count": 0}


def verify_attestation_binary(
    att: dict[str, Any],
    *,
    repo_path: Path,
    transparency_log: Path | None = None,
) -> dict[str, Any]:
    hashes = _extract_hashes(att)
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"check": name, "passed": ok, "detail": detail})

    add("H_verdict_present", bool(hashes["H_verdict"]), hashes["H_verdict"][:16] or "missing")
    add(
        "compiler_graph_hash_present",
        bool(hashes["compiler_graph_hash"]),
        hashes["compiler_graph_hash"][:16] or "missing",
    )
    add("pipeline_hash_present", bool(hashes["pipeline_hash"]), hashes["pipeline_hash"][:16] or "missing")
    add(
        "policy_verdict_hash_present",
        bool(hashes["policy_verdict_hash"]),
        hashes["policy_verdict_hash"][:16] or "missing",
    )

    compile_out = compile_repo_stdlib(repo_path)
    recomputed = str(compile_out.get("graph_hash") or "")
    graph_ok = bool(hashes["compiler_graph_hash"]) and recomputed == hashes["compiler_graph_hash"]
    add(
        "compiler_graph_hash_replay",
        graph_ok,
        f"recomputed={recomputed[:16]} expected={hashes['compiler_graph_hash'][:16]}",
    )

    log_ok = True
    log_detail = "transparency_log_optional"
    if transparency_log and transparency_log.is_file():
        log_ok = False
        att_hash = canonical_hash(
            {
                "attestation_verify_v1": True,
                "H_verdict": hashes["H_verdict"],
                "compiler_graph_hash": hashes["compiler_graph_hash"],
            }
        )
        for line in transparency_log.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("attestation_hash") == att_hash or entry.get("compiler_graph_hash") == hashes[
                "compiler_graph_hash"
            ]:
                log_ok = True
                break
        log_detail = "transparency_entry_found" if log_ok else "transparency_entry_missing"
    add("transparency_log", log_ok, log_detail)

    passed = all(c["passed"] for c in checks)
    return {
        "schema_id": VERIFY_SCHEMA,
        "version": "1.0.0",
        "verdict": "PASS" if passed else "FAIL",
        "passed": passed,
        "repo": str(repo_path.resolve()),
        "compiler_binary": "stdlib_embedded",
        "checks": checks,
        "hashes": hashes,
        "recomputed_compiler_graph_hash": recomputed,
        "node_count": compile_out.get("node_count"),
        "edge_count": compile_out.get("edge_count"),
        "verify_hash": canonical_hash({"verify_v1": checks, "passed": passed}),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Public binary verifier")
    parser.add_argument("attestation", type=Path)
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--log", type=Path, default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    att_path = args.attestation
    if not att_path.is_file():
        print(f"FAIL: attestation not found: {args.attestation}", file=sys.stderr)
        return 2
    att = json.loads(att_path.read_text(encoding="utf-8"))
    repo = args.repo or Path(str(att.get("repo") or "."))
    if not repo.is_dir():
        repo = Path.cwd()
    report = verify_attestation_binary(att, repo_path=repo, transparency_log=args.log)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"binary-verify: {report['verdict']}")
        for c in report["checks"]:
            mark = "PASS" if c["passed"] else "FAIL"
            print(f"  [{mark}] {c['check']}: {c['detail']}")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
