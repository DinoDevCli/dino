"""Deterministic --self-test for each domain package."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Callable

from dino import __version__
from dino.common.determinism import canonical_hash


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _fixtures() -> Path:
    root = _repo_root()
    cand = root / "tests" / "dino" / "fixtures"
    if cand.is_dir():
        return cand
    return root / "tests" / "fixtures"


def _emit(payload: dict) -> int:
    sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return 0 if payload.get("ok") else 1


def _bundle() -> dict:
    from dino.domains.bundle.run_artifact_writer import build_run_payload_v1_1

    p = build_run_payload_v1_1(
        core_version="0.3.0",
        execution_graph=["a"],
        signals={},
        decision="pass",
        explainability={},
        evidence={},
    )
    return {"domain": "bundle", "ok": p.get("schema_version") == "1.1.0"}


def _flight() -> dict:
    arts = _fixtures() / "flight" / "artifacts"
    n = len(list(arts.glob("engine_j_canary_*.json"))) if arts.is_dir() else 0
    return {"domain": "flight", "ok": n > 0, "records": n}


def _verify() -> dict:
    from dino.domains.verify.drift_classifier import classify_drift

    return {"domain": "verify", "ok": classify_drift(distance=0) == "aligned"}


def _map() -> dict:
    from dino.domains.map.graph import build_graph
    from dino.domains.map.verify import verify_repo

    root = _repo_root() / "dino" / "common"
    graph = build_graph(root)
    report = verify_repo(str(root))
    return {
        "domain": "map",
        "ok": bool(graph.get("graph_hash")) and "overall_quality_score" in report,
        "graph_hash": graph.get("graph_hash"),
    }


def _capsule() -> dict:
    from dino.domains.capsule.execute import execute

    with tempfile.TemporaryDirectory() as td:
        result = execute(["echo", "ok"], output_dir=Path(td))
    return {
        "domain": "capsule",
        "ok": bool(result.get("replay_ok")) and bool(result.get("exec_ok", True)),
        "hash": result.get("capsule_hash"),
    }


def _proof() -> dict:
    from dino.domains.proof.chain import build_proof

    out = Path(__file__).resolve().parents[1] / "domains" / "proof" / "_self_test_out"
    if out.exists():
        import shutil

        shutil.rmtree(out)
    proof = build_proof(output_dir=out, command=["echo", "proof"])
    return {
        "domain": "proof",
        "ok": bool(proof.get("ok")),
        "proof_hash": proof.get("proof_hash"),
        "capsule_hash": (proof.get("parts") or {}).get("capsule_hash"),
    }


def _scan() -> dict:
    from dino.domains.scan.grammar import smoke
    from dino.domains.scan.leakage import scan_paths

    g = smoke()
    clean = _fixtures() / "scan" / "clean_code.py"
    leak = scan_paths([clean]) if clean.is_file() else None
    return {
        "domain": "scan",
        "ok": g.get("status") == "ok" and (leak.ok if leak else True),
    }


DOMAIN_SELF_TESTS: dict[str, Callable[[], dict]] = {
    "scan": _scan,
    "capsule": _capsule,
    "map": _map,
    "bundle": _bundle,
    "flight": _flight,
    "verify": _verify,
    "proof": _proof,
}


def run_self_test(domain: str) -> int:
    fn = DOMAIN_SELF_TESTS.get(domain)
    if fn is None:
        sys.stderr.write(f"unknown domain: {domain}\n")
        return 2
    payload = fn()
    payload["self_test_hash"] = canonical_hash(
        {k: v for k, v in payload.items() if k != "self_test_hash"}
    )
    payload["dino_version"] = __version__
    return _emit(payload)
