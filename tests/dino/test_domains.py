from __future__ import annotations

import io
import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from dino.cli import main
from tests.dino.conftest import FIXTURES, ROOT, _unwrap_envelope, twice


def run(argv: list[str]) -> tuple[int, str, str]:
    cmd = ["--json", *argv]
    out, err = io.StringIO(), io.StringIO()
    old = list(sys.argv)
    try:
        sys.argv = ["dino", *cmd]
        with redirect_stdout(out), redirect_stderr(err):
            code = main(cmd)
    finally:
        sys.argv = old
    return int(code), _unwrap_envelope(out.getvalue()), err.getvalue()


class VerifyTests(unittest.TestCase):
    def test_attest_and_binary(self) -> None:
        att = FIXTURES / "attest" / "valid_attest.json"
        anchor = FIXTURES / "attest" / "trust_anchor.json"
        code, out, _ = run(["verify", "attest", str(att), "--trust-anchor", str(anchor)])
        self.assertIn(code, (0, 1))
        json.loads(out)
        twice(["verify", "attest", str(att), "--trust-anchor", str(anchor)])
        code, out, _ = run(["verify", "binary", str(att)])
        json.loads(out)
        twice(["verify", "binary", str(att)])

    def test_drift(self) -> None:
        code, out, _ = run(["verify", "drift", "--distance", "0"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["bucket"], "aligned")
        twice(["verify", "drift", "--distance", "12", "--tau", "5"])


class MapTests(unittest.TestCase):
    def test_verify_deterministic(self) -> None:
        repo = FIXTURES / "brain" / "repo_small"
        if not repo.is_dir():
            repo = ROOT / "dino"
        argv = ["map", "verify", "--repo", str(repo)]
        code, out, _ = run(argv)
        self.assertEqual(code, 0)
        self.assertIn("overall_quality_score", json.loads(out))
        twice(argv)

    def test_analyze(self) -> None:
        repo = ROOT / "dino" / "common"
        code, out, _ = run(["map", "analyze", str(repo)])
        self.assertEqual(code, 0)
        json.loads(out)


class CapsuleTests(unittest.TestCase):
    def test_doctor_fixed_path(self) -> None:
        outdir = Path(__file__).resolve().parent / "_work_capsule" / "doctor"
        argv = ["capsule", "doctor", "--output-dir", str(outdir)]
        code, out, _ = run(argv)
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["output_dir"], str(outdir.resolve()))
        twice(argv)

    def test_run_replay(self) -> None:
        outdir = Path(__file__).resolve().parent / "_work_capsule" / "exec"
        code, out, _ = run(["capsule", "run", "--output-dir", str(outdir), "--command", "echo", "ok"])
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(out)["replay_ok"])
        cap = outdir / "capsule.json"
        code, out, _ = run(["capsule", "replay", "--capsule", str(cap), "--output-dir", str(outdir)])
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(out)["replay_ok"])


class ScanTests(unittest.TestCase):
    def test_grammar(self) -> None:
        code, out, _ = run(["scan", "grammar"])
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["status"], "ok")
        twice(["scan", "grammar"])

    def test_leakage_forbidden(self) -> None:
        path = FIXTURES / "alpha" / "forbidden_import.py"
        code, out, _ = run(["scan", "leakage", str(path)])
        self.assertEqual(code, 1)
        payload = json.loads(out)
        self.assertFalse(payload["ok"])
        self.assertTrue(payload["findings"])


class ProofCompanionTests(unittest.TestCase):
    def test_flight_summary(self) -> None:
        arts = FIXTURES / "canary" / "artifacts"
        if not arts.is_dir():
            self.skipTest("fixture missing")
        work = Path(__file__).resolve().parent / "_work_flight.json"
        argv = ["flight", "summary", "--artifacts-dir", str(arts), "--output", str(work)]
        code, out, _ = run(argv)
        self.assertEqual(code, 0)
        json.loads(out)
        twice(argv)

    def test_bundle_create(self) -> None:
        rundata = FIXTURES / "artifact" / "rundata.json"
        if not rundata.is_file():
            self.skipTest("fixture missing")
        work = Path(__file__).resolve().parent / "_work_bundle.json"
        argv = ["bundle", "create", "--rundata", str(rundata), "--output", str(work)]
        code, out, _ = run(argv)
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["status"], "ok")
        twice(argv)


if __name__ == "__main__":
    unittest.main()
