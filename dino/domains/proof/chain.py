"""Proof chain — normative implementation of docs/PROOF_CONTRACT.md."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from dino.common.determinism import canonical_hash
from dino.common.utils import write_json

SCHEMA = "dino.proof.bundle.v1"
SCHEMAS = {
    "proof": SCHEMA,
    "capsule": "dino.capsule.capsule.v1",
    "scan": "dino.scan.leakage.v1",
    "map": "dino.map.verify.v1",
    "drift": "dino.verify.drift_class.v1",
}

HASH_EXCLUDE = frozenset({"proof_hash", "ok", "output_dir"})


def _audit(verdict: str, summary: str, reasons: list[str]) -> dict[str, Any]:
    return {"verdict": verdict, "summary": summary, "reasons": list(reasons)}


def _status_for(*, capsule_ok: bool, scan_ok: bool | None, map_ok: bool | None) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if not capsule_ok:
        reasons.append("capsule_failed")
        return "failed", reasons
    reasons.append("capsule_sealed")

    if scan_ok is False:
        reasons.append("scan_failed")
        return "failed", reasons
    if scan_ok is True:
        reasons.append("scan_clean")
    else:
        reasons.append("scan_skipped")

    if map_ok is False:
        reasons.append("map_failed")
        return "failed", reasons
    if map_ok is True:
        reasons.append("map_scored")
    else:
        reasons.append("map_skipped")

    if "scan_skipped" in reasons or "map_skipped" in reasons:
        return "partial", reasons
    return "passed", reasons


def build_proof(
    *,
    output_dir: Path,
    command: list[str],
    repo: Path | None = None,
    scan_roots: list[Path] | None = None,
    stdin: str = "",
) -> dict[str, Any]:
    from dino.domains.capsule.execute import execute
    from dino.domains.map.verify import verify_repo
    from dino.domains.scan.leakage import scan_paths as run_scan
    from dino.domains.verify.drift_classifier import classify_drift

    if not command:
        raise ValueError("command must be non-empty")

    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    capsule_dir = output_dir / "capsule"
    capsule_dir.mkdir(parents=True, exist_ok=True)

    capsule_result = execute(list(command), output_dir=capsule_dir, stdin=stdin)
    capsule_ok = bool(capsule_result.get("replay_ok"))

    scan_report: dict[str, Any] | None = None
    scan_ok: bool | None = None
    if scan_roots:
        report = run_scan([Path(p) for p in scan_roots])
        scan_report = report.to_dict()
        scan_report["schema"] = SCHEMAS["scan"]
        write_json(output_dir / "scan.json", scan_report)
        scan_ok = bool(scan_report.get("ok"))

    map_report: dict[str, Any] | None = None
    map_ok: bool | None = None
    if repo is not None and Path(repo).exists():
        map_report = verify_repo(str(repo))
        write_json(output_dir / "map_verify.json", map_report)
        map_ok = "overall_quality_score" in map_report
    elif repo is not None:
        map_ok = False

    drift_bucket = classify_drift(distance=0)
    if map_report and isinstance(map_report.get("drift"), dict):
        drift_bucket = map_report["drift"].get("bucket") or drift_bucket

    status, reasons = _status_for(capsule_ok=capsule_ok, scan_ok=scan_ok, map_ok=map_ok)
    if status == "passed":
        verdict, summary = "PROOF_PASSED", "All requested proof parts succeeded."
    elif status == "partial":
        verdict, summary = "PROOF_PARTIAL", "Capsule sealed; one or more optional parts were skipped."
    else:
        verdict, summary = "PROOF_FAILED", "Proof failed: " + ", ".join(reasons)

    parts = {
        "capsule_hash": capsule_result.get("capsule_hash"),
        "capsule_replay_ok": capsule_ok,
        "scan_ok": scan_ok,
        "map_score": None if map_report is None else map_report.get("overall_quality_score"),
        "map_graph_hash": None if map_report is None else map_report.get("graph_hash"),
        "drift_bucket": drift_bucket,
    }
    artifacts = {
        "capsule": "capsule/capsule.json",
        "scan": "scan.json" if scan_report is not None else None,
        "map_verify": "map_verify.json" if map_report is not None else None,
    }
    proof: dict[str, Any] = {
        "schema": SCHEMA,
        "schemas": dict(SCHEMAS),
        "command": list(command),
        "parts": parts,
        "artifacts": artifacts,
        "status": status,
        "audit": _audit(verdict, summary, reasons),
    }
    proof["proof_hash"] = canonical_hash({k: v for k, v in proof.items() if k not in HASH_EXCLUDE})
    proof["ok"] = status in {"passed", "partial"}
    proof["output_dir"] = str(output_dir)
    write_json(output_dir / "proof.json", proof)
    return proof


def verify_proof(proof_path: Path) -> dict[str, Any]:
    import json

    from dino.common.utils import read_json
    from dino.domains.capsule.replay import replay

    proof = json.loads(proof_path.read_text(encoding="utf-8"))
    schema = proof.get("schema") or proof.get("schemas", {}).get("proof")
    schema_ok = schema == SCHEMA

    body = {k: v for k, v in proof.items() if k not in HASH_EXCLUDE}
    expected = str(proof.get("proof_hash") or "")
    got = canonical_hash(body)
    hash_ok = expected == got and bool(expected)

    rel = (proof.get("artifacts") or {}).get("capsule") or ""
    base = Path(proof.get("output_dir") or proof_path.parent)
    capsule_path = Path(rel) if Path(rel).is_absolute() and Path(rel).is_file() else (base / rel)
    capsule_ok = False
    capsule_report: dict[str, Any] | None = None
    if capsule_path.is_file():
        capsule_report = replay(read_json(capsule_path), reexec=True)
        capsule_ok = bool(capsule_report.get("replay_ok"))

    ok = schema_ok and hash_ok and capsule_ok
    reasons: list[str] = []
    if not schema_ok:
        reasons.append("schema_mismatch")
    if not hash_ok:
        reasons.append("proof_hash_mismatch")
    if not capsule_ok:
        reasons.append("capsule_replay_failed")
    if ok:
        reasons.append("verify_ok")
        audit = _audit("PROOF_VERIFY_PASSED", "Proof hash and capsule re-exec verified.", reasons)
    else:
        audit = _audit("PROOF_VERIFY_FAILED", "Proof verification failed: " + ", ".join(reasons), reasons)

    return {
        "schema": "dino.proof.verify.v1",
        "schemas": dict(SCHEMAS),
        "proof_schema_ok": schema_ok,
        "proof_hash_ok": hash_ok,
        "expected_proof_hash": expected,
        "recomputed_proof_hash": got,
        "capsule_replay_ok": capsule_ok,
        "capsule": capsule_report,
        "status": "passed" if ok else "failed",
        "ok": ok,
        "audit": audit,
    }


def run_proof_doctor(*, output_dir: Path | None = None) -> dict[str, Any]:
    """Enterprise health check for the full proof stack."""
    import sys
    import tempfile

    from dino.domains.capsule.execute import execute
    from dino.domains.map.verify import verify_repo
    from dino.domains.scan.grammar import smoke
    from dino.domains.verify.drift_classifier import classify_drift
    from dino.license import get_active_packs, is_domain_active
    from dino.packs import ALL_DOMAINS

    checks: list[dict[str, Any]] = []

    def add(name: str, passed: bool, detail: str) -> None:
        checks.append({"check": name, "passed": passed, "detail": detail})

    add(
        "python_major_minor",
        sys.version_info[:2] >= (3, 10),
        f"{sys.version_info.major}.{sys.version_info.minor}",
    )
    add("proof_schema", SCHEMA == "dino.proof.bundle.v1", SCHEMA)

    g = smoke()
    add("scan_grammar", g.get("status") == "ok", g.get("version", ""))

    add("drift_aligned", classify_drift(distance=0) == "aligned", "distance=0")

    repo = Path(__file__).resolve().parents[2] / "common"
    if repo.is_dir():
        report = verify_repo(str(repo))
        add("map_verify", "overall_quality_score" in report, str(report.get("overall_quality_score")))
    else:
        add("map_verify", False, f"missing {repo}")

    active = get_active_packs()
    add("license_packs", "free" in active, ",".join(active))
    proof_on = is_domain_active("proof") and is_domain_active("capsule")
    add("pack_proof_domains", proof_on, f"proof={is_domain_active('proof')}")

    out = (output_dir or Path(tempfile.mkdtemp(prefix="dino_proof_doctor_"))).resolve()
    out.mkdir(parents=True, exist_ok=True)
    sealed = execute(["echo", "doctor"], output_dir=out / "capsule")
    add("capsule_seal", bool(sealed.get("replay_ok")), str(sealed.get("capsule_hash", ""))[:16])

    proof = build_proof(output_dir=out / "proof", command=["echo", "doctor"])
    add("proof_run", bool(proof.get("ok")), proof.get("status", ""))
    verify = verify_proof(Path(proof["output_dir"]) / "proof.json")
    add("proof_verify", bool(verify.get("ok")), verify.get("audit", {}).get("verdict", ""))

    domains = {d: is_domain_active(d) for d in ALL_DOMAINS}
    ok = all(c["passed"] for c in checks)
    report = {
        "schema": "dino.proof.doctor.v1",
        "ok": ok,
        "status": "passed" if ok else "failed",
        "checks": checks,
        "domains": domains,
        "active_packs": active,
        "audit": _audit(
            "PROOF_DOCTOR_PASSED" if ok else "PROOF_DOCTOR_FAILED",
            "Proof stack healthy." if ok else "One or more doctor checks failed.",
            [c["check"] for c in checks if not c["passed"]] or ["all_passed"],
        ),
    }
    report["report_hash"] = canonical_hash({k: v for k, v in report.items() if k != "report_hash"})
    write_json(out / "doctor.json", report)
    report["output_dir"] = str(out)
    return report


def format_audit_banner(result: dict[str, Any]) -> str:
    audit = result.get("audit") or {}
    verdict = audit.get("verdict", "PROOF_UNKNOWN")
    summary = audit.get("summary", "")
    status = result.get("status", "")
    icon = "✅" if result.get("ok") else "❌"
    if status == "partial":
        icon = "⚠️"
    lines = [
        f"{icon} {verdict}",
        summary,
        f"status={status}  proof_hash={(result.get('proof_hash') or result.get('recomputed_proof_hash') or '')[:16]}",
    ]
    reasons = audit.get("reasons") or []
    if reasons:
        lines.append("reasons: " + ", ".join(reasons))
    return "\n".join(lines)
