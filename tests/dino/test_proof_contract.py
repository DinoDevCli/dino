"""End-to-end proof contract tests (docs/PROOF_CONTRACT.md)."""

from __future__ import annotations

import json
from pathlib import Path

from dino.domains.proof.chain import SCHEMA, SCHEMAS, build_proof, verify_proof
from tests.dino.conftest import FIXTURES, ROOT, run

WORK = Path(__file__).resolve().parent / "_proof_e2e"
WORK.mkdir(parents=True, exist_ok=True)


def test_proof_run_end_to_end() -> None:
    outdir = WORK / "e2e_full"
    code, out, _ = run(
        [
            "proof",
            "run",
            "--output-dir",
            str(outdir),
            "--command",
            "echo",
            "e2e",
            "--repo",
            str(ROOT / "dino" / "common"),
            "--scan",
            str(FIXTURES / "alpha" / "clean_code.py"),
        ]
    )
    assert code == 0
    proof = json.loads(out)
    assert proof["schema"] == SCHEMA
    assert proof["schemas"] == SCHEMAS
    assert proof["status"] == "passed"
    assert proof["ok"] is True
    assert proof["audit"]["verdict"] == "PROOF_PASSED"
    assert proof["parts"]["capsule_replay_ok"] is True
    assert proof["parts"]["scan_ok"] is True
    assert proof["parts"]["map_score"] is not None
    assert (outdir / "proof.json").is_file()
    assert (outdir / "capsule" / "capsule.json").is_file()
    assert (outdir / "scan.json").is_file()
    assert (outdir / "map_verify.json").is_file()


def test_proof_verify_pass() -> None:
    outdir = WORK / "verify_pass"
    proof = build_proof(output_dir=outdir, command=["echo", "verify_pass"])
    code, out, _ = run(["proof", "verify", "--proof", str(outdir / "proof.json")])
    assert code == 0
    report = json.loads(out)
    assert report["ok"] is True
    assert report["status"] == "passed"
    assert report["audit"]["verdict"] == "PROOF_VERIFY_PASSED"
    assert report["proof_hash_ok"] is True
    assert report["capsule_replay_ok"] is True
    assert proof["proof_hash"] == report["expected_proof_hash"]


def test_proof_verify_fail() -> None:
    outdir = WORK / "verify_fail"
    build_proof(output_dir=outdir, command=["echo", "tamper_me"])
    path = outdir / "proof.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["command"] = ["echo", "tampered"]
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    code, out, _ = run(["proof", "verify", "--proof", str(path)])
    assert code == 1
    report = json.loads(out)
    assert report["ok"] is False
    assert report["audit"]["verdict"] == "PROOF_VERIFY_FAILED"
    assert report["proof_hash_ok"] is False


def test_proof_json_contract() -> None:
    outdir = WORK / "contract_shape"
    proof = build_proof(output_dir=outdir, command=["echo", "contract"])
    required = {
        "schema",
        "schemas",
        "command",
        "parts",
        "artifacts",
        "proof_hash",
        "ok",
        "status",
        "audit",
        "output_dir",
    }
    assert required <= set(proof)
    assert proof["schema"] == "dino.proof.bundle.v1"
    assert set(proof["schemas"]) == set(SCHEMAS)
    for key in ("capsule_hash", "capsule_replay_ok", "scan_ok", "map_score", "map_graph_hash", "drift_bucket"):
        assert key in proof["parts"]
    assert proof["artifacts"]["capsule"] == "capsule/capsule.json"
    assert proof["status"] == "partial"  # no scan/repo
    assert proof["audit"]["verdict"] == "PROOF_PARTIAL"
    assert "reasons" in proof["audit"]
    # Hash excludes output_dir
    again = verify_proof(outdir / "proof.json")
    assert again["ok"] is True


def test_proof_doctor() -> None:
    code, out, _ = run(["proof", "doctor", "--output-dir", str(WORK / "doctor")])
    assert code == 0
    report = json.loads(out)
    assert report["ok"] is True
    assert report["schema"] == "dino.proof.doctor.v1"
    assert report["audit"]["verdict"] == "PROOF_DOCTOR_PASSED"
    names = {c["check"] for c in report["checks"]}
    assert "capsule_seal" in names
    assert "proof_verify" in names


def test_proof_run_fails_on_scan() -> None:
    outdir = WORK / "scan_fail"
    code, out, _ = run(
        [
            "proof",
            "run",
            "--output-dir",
            str(outdir),
            "--command",
            "echo",
            "x",
            "--scan",
            str(FIXTURES / "alpha" / "forbidden_import.py"),
        ]
    )
    assert code == 1
    proof = json.loads(out)
    assert proof["status"] == "failed"
    assert proof["audit"]["verdict"] == "PROOF_FAILED"
    assert "scan_failed" in proof["audit"]["reasons"]
