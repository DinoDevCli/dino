"""Gap-closure tests — real capsule exec, bundle replay, supersede, proof, scan rules."""

from __future__ import annotations

import json
from pathlib import Path

from tests.dino.conftest import FIXTURES, ROOT, run, twice

WORK = Path(__file__).resolve().parent / "_gap_work"
WORK.mkdir(parents=True, exist_ok=True)


def test_capsule_run_captures_stdout_and_reexec() -> None:
    outdir = WORK / "capsule_exec"
    code, out, _ = run(
        ["capsule", "run", "--output-dir", str(outdir), "--command", "echo", "gap_seal"]
    )
    assert code == 0
    payload = json.loads(out)
    assert payload["replay_ok"] is True
    assert payload["exec_ok"] is True
    assert payload["hash_ok"] is True
    cap = json.loads((outdir / "capsule.json").read_text(encoding="utf-8"))
    assert "gap_seal" in cap["output"]
    assert cap["exit_code"] == 0
    assert "stderr" in cap
    twice(["capsule", "run", "--output-dir", str(outdir), "--command", "echo", "gap_seal"])


def test_capsule_run_accepts_quoted_command_string() -> None:
    """Users often pass --command \"echo ok\"; that must still seal as argv."""
    outdir = WORK / "capsule_quoted"
    code, out, _ = run(
        ["capsule", "run", "--output-dir", str(outdir), "--command", "echo quoted_ok"]
    )
    assert code == 0
    cap = json.loads((outdir / "capsule.json").read_text(encoding="utf-8"))
    assert cap["command"] == ["echo", "quoted_ok"]
    assert "quoted_ok" in cap["output"]


def test_capsule_missing_binary_returns_clear_error() -> None:
    outdir = WORK / "capsule_missing_bin"
    code, out, _ = run(
        [
            "capsule",
            "run",
            "--output-dir",
            str(outdir),
            "--command",
            "dino_no_such_binary_xyz",
        ]
    )
    assert code == 2
    err = json.loads(out)
    assert err["type"] == "invalid_args"
    assert "command not found" in err["detail"]
    assert "dino_no_such_binary_xyz" in err["detail"]


def test_capsule_replay_detects_tamper() -> None:
    outdir = WORK / "capsule_tamper"
    run(["capsule", "run", "--output-dir", str(outdir), "--command", "echo", "orig"])
    cap_path = outdir / "capsule.json"
    cap = json.loads(cap_path.read_text(encoding="utf-8"))
    cap["output"] = "tampered\n"
    cap_path.write_text(json.dumps(cap, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    code, out, _ = run(
        ["capsule", "replay", "--capsule", str(cap_path), "--output-dir", str(outdir / "r")]
    )
    assert code == 1
    payload = json.loads(out)
    assert payload["replay_ok"] is False
    assert payload["hash_ok"] is False


def test_bundle_replay_regression() -> None:
    base = FIXTURES / "bundle" / "baseline_counts.json"
    cur = FIXTURES / "bundle" / "current_counts.json"
    code, out, _ = run(
        ["bundle", "replay", "--baseline", str(base), "--current", str(cur)]
    )
    assert code == 0
    payload = json.loads(out)
    assert payload["passed"] is True
    assert payload["true_delta"] == 1
    twice(["bundle", "replay", "--baseline", str(base), "--current", str(cur)])


def test_verify_supersede_with_files() -> None:
    contract = FIXTURES / "verify" / "contract_release.json"
    previous = FIXTURES / "verify" / "contract_previous.json"
    code, out, _ = run(
        [
            "verify",
            "supersede",
            "--runtime-verdict",
            "REJECTED",
            "--release-verdict",
            "APPROVED",
            "--contract",
            str(contract),
            "--previous",
            str(previous),
        ]
    )
    assert code == 0
    payload = json.loads(out)
    assert payload["decision"]["runtime_supersedes"] is True
    assert payload["decision"]["supersedes"] == "release-0"
    assert payload["chain_ok"] is True


def test_scan_shift_and_seedless() -> None:
    path = FIXTURES / "scan" / "shift_and_seedless.py"
    code, out, _ = run(["scan", "leakage", str(path)])
    assert code == 1
    payload = json.loads(out)
    rules = {f["rule"] for f in payload["findings"]}
    assert "SHIFT_NEGATIVE" in rules
    assert "SEEDLESS_SPLIT" in rules


def test_scan_target_in_features() -> None:
    path = FIXTURES / "scan" / "target_in_features.py"
    code, out, _ = run(["scan", "leakage", str(path)])
    assert code == 1
    rules = {f["rule"] for f in json.loads(out)["findings"]}
    assert "TARGET_IN_FEATURES" in rules


def test_map_plan_and_drift() -> None:
    small = FIXTURES / "map" / "repo_small"
    clean = FIXTURES / "map" / "repo_clean"
    code, out, _ = run(["map", "plan", str(small)])
    assert code == 0
    plan = json.loads(out)
    assert plan["complete"] is True
    assert plan["steps"]
    code, out, _ = run(["map", "drift", str(small), "--baseline", str(clean)])
    assert code == 0
    drift = json.loads(out)
    assert drift["distance"] >= 1
    assert drift["bucket"] in {"controlled_drift", "severe_drift", "aligned"}


def test_scan_missing_path_fails_closed() -> None:
    code, out, _ = run(["scan", "leakage", "/tmp/dino_no_such_scan_root_xyz"])
    assert code == 1
    report = json.loads(out)
    assert report["ok"] is False
    assert report["files_scanned"] == 0
    assert any(f["rule"] == "EMPTY_SCAN_ROOTS" for f in report["findings"])


def test_proof_run_and_verify() -> None:
    outdir = WORK / "proof_chain"
    repo = ROOT / "dino" / "common"
    scan = FIXTURES / "scan" / "clean_code.py"
    code, out, _ = run(
        [
            "proof",
            "run",
            "--output-dir",
            str(outdir),
            "--command",
            "echo",
            "proof_ok",
            "--repo",
            str(repo),
            "--scan",
            str(scan),
        ]
    )
    assert code == 0
    proof = json.loads(out)
    assert proof["ok"] is True
    assert proof["schema"] == "dino.proof.bundle.v1"
    assert proof["status"] in {"passed", "partial"}
    assert proof["parts"]["capsule_replay_ok"] is True
    assert proof["parts"]["scan_ok"] is True
    assert proof["parts"]["map_score"] is not None
    assert "schemas" in proof
    assert proof["audit"]["verdict"] in {"PROOF_PASSED", "PROOF_PARTIAL"}
    proof_path = outdir / "proof.json"
    assert proof_path.is_file()
    code, out, _ = run(["proof", "verify", "--proof", str(proof_path)])
    assert code == 0
    assert json.loads(out)["ok"] is True
    assert json.loads(out)["audit"]["verdict"] == "PROOF_VERIFY_PASSED"
