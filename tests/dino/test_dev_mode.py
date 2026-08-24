"""Developer Mode (--dev) relaxes EMPTY_SCAN_ROOTS only."""

from __future__ import annotations

import json
from pathlib import Path

from tests.dino.conftest import FIXTURES, run

WORK = Path(__file__).resolve().parent / "_work_dev_mode"
WORK.mkdir(parents=True, exist_ok=True)
MISSING = "/tmp/dino_no_such_scan_root_xyz"


def test_scan_dev_relaxes_empty_roots() -> None:
    code, out, err = run(["--dev", "scan", "leakage", MISSING])
    assert code == 0
    report = json.loads(out)
    assert report["ok"] is True
    assert report["dev"] is True
    finding = next(f for f in report["findings"] if f["rule"] == "EMPTY_SCAN_ROOTS")
    assert finding["severity"] == "WARN"
    assert "Developer Mode" in err


def test_scan_dev_still_fails_on_leakage() -> None:
    leaky = FIXTURES / "scan" / "forbidden_import.py"
    code, out, _ = run(["--dev", "scan", "leakage", str(leaky)])
    assert code == 1
    report = json.loads(out)
    assert report["ok"] is False
    assert any(f["rule"] == "LEAKY_IMPORT" for f in report["findings"])


def test_proof_run_dev_allows_missing_scan() -> None:
    outdir = WORK / "proof_dev"
    code, out, err = run(
        [
            "--dev",
            "proof",
            "run",
            "--output-dir",
            str(outdir),
            "--command",
            "echo",
            "dev_ok",
            "--scan",
            MISSING,
        ]
    )
    assert code == 0, out
    proof = json.loads(out)
    assert proof["ok"] is True
    assert proof["parts"]["dev_mode"] is True
    assert proof["parts"]["scan_ok"] is True
    assert "Developer Mode" in err


def test_proof_run_missing_scan_still_fails_closed() -> None:
    outdir = WORK / "proof_closed"
    code, out, _ = run(
        [
            "proof",
            "run",
            "--output-dir",
            str(outdir),
            "--command",
            "echo",
            "closed",
            "--scan",
            MISSING,
        ]
    )
    assert code == 1
    proof = json.loads(out)
    assert proof["ok"] is False
    assert proof["parts"]["scan_ok"] is False
    assert "dev_mode" not in proof["parts"]
