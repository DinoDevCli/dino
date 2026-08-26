"""Production-grade E2E simulation: a real team using Dino on a fraud pipeline.

Not unit tests. Simulates:
  extract → transform → model → report
  + proof / export / index / compare / metrics / layout
  + Early Access Team Keys (valid + expired)
  + Free mode lock
  + Determinism across many runs
  + HTTP export, failure cases, stress dataset
"""

from __future__ import annotations

import json
import shlex
import shutil
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread
from unittest.mock import patch

import pytest

from dino.early_access import issue_key
from dino.license import (
    DEFAULT_LICENSE,
    activate_pack,
    get_active_packs,
    is_domain_active,
    save_license,
)
from tests.simulation.conftest import run

SIM = Path(__file__).resolve().parent
PIPE_DIR = SIM / "pipeline"
RUN_PY = PIPE_DIR / "run.py"
PY = sys.executable

DETERMINISM_RUNS = 10
STRESS_ROWS = 10_000


@pytest.fixture
def sim_home(tmp_path, monkeypatch):
    """Isolated license home + clean work dirs."""
    lic_dir = tmp_path / ".dino"
    lic_dir.mkdir()
    monkeypatch.setattr("dino.license.LICENSE_DIR", lic_dir)
    monkeypatch.setattr("dino.license.LICENSE_PATH", lic_dir / "license.json")
    monkeypatch.setenv("DINO_EA_SIGNING_SECRET", "sim-secret-production-e2e")
    # Clear offline allowlist so Early Access keys are the real path
    monkeypatch.delenv("DINO_OFFLINE_LICENSE_KEYS", raising=False)
    monkeypatch.delenv("DINO_LICENSE_SKIP_REMOTE", raising=False)
    save_license(dict(DEFAULT_LICENSE))
    work = tmp_path / "work"
    proof_out = tmp_path / "proof_out"
    archive = tmp_path / "archive"
    for p in (work, proof_out, archive):
        p.mkdir()
    return {
        "lic_dir": lic_dir,
        "work": work,
        "proof_out": proof_out,
        "archive": archive,
        "pipe": PIPE_DIR,
    }


def _pipeline_cmd(work: Path, *, rows: int = 500, extra: list[str] | None = None) -> list[str]:
    cmd = [
        PY,
        str(RUN_PY),
        "--workdir",
        str(work),
        "--rows",
        str(rows),
        "--seed",
        "dino-sim",
    ]
    if extra:
        cmd.extend(extra)
    return cmd


def _proof_run(
    *,
    work: Path,
    proof_out: Path,
    archive: Path | None,
    rows: int = 500,
    pipeline: str = "fraud_score_sim",
    group: str = "risk-team",
    tags: list[str] | None = None,
    extra_pipe: list[str] | None = None,
) -> tuple[int, dict, str]:
    tags = tags or ["prod", "sim"]
    # Single string so pipeline flags (--workdir, …) are not eaten by dino argparse
    cmd = shlex.join(_pipeline_cmd(work, rows=rows, extra=extra_pipe))
    argv = [
        "proof",
        "run",
        "--command",
        cmd,
        "--scan",
        str(PIPE_DIR),
        "--output-dir",
        str(proof_out),
        "--pipeline",
        pipeline,
        "--group",
        group,
    ]
    for tag in tags:
        argv.extend(["--tag", tag])
    if archive is not None:
        argv.extend(["--export", str(archive)])
    code, out, err = run(argv)
    payload = {}
    if out.strip().startswith("{"):
        payload = json.loads(out)
    return code, payload, err


def _unlock_ea(team: str = "risk-sim", days: int = 90) -> str:
    key = issue_key(team=team, days=days)
    activate_pack("proof", key=key)
    return key


# ---------------------------------------------------------------------------
# 1–2: Full team workflow
# ---------------------------------------------------------------------------


class TestFullTeamWorkflow:
    def test_proof_export_index_compare_metrics_layout_verify(self, sim_home) -> None:
        _unlock_ea()
        work, proof_out, archive = sim_home["work"], sim_home["proof_out"], sim_home["archive"]

        code, payload, err = _proof_run(work=work, proof_out=proof_out, archive=archive)
        assert code == 0, err
        assert payload.get("ok") is True
        proof_hash = payload["proof_hash"]
        hash16 = proof_hash[:16]

        assert (proof_out / "proof.json").is_file()
        assert (proof_out / "scan.json").is_file()
        assert (work / "report.json").is_file()

        bundle = archive / hash16
        assert (bundle / "proof.json").is_file()
        assert (bundle / "export.json").is_file()
        assert (archive / "proof_index.json").is_file()

        export_body = json.loads((bundle / "export.json").read_text(encoding="utf-8"))
        assert export_body["schema"] == "dino.proof.export.v1"
        assert export_body["index_entry"]["pipeline"] == "fraud_score_sim"

        for kind, name in (
            ("pipelines", "fraud_score_sim"),
            ("groups", "risk-team"),
            ("tags", "prod"),
            ("tags", "sim"),
        ):
            target = archive / kind / name / hash16
            assert target.exists() or target.is_symlink(), f"missing layout {target}"

        code, out, _ = run(["proof", "index", "show", str(archive)])
        assert code == 0
        index = json.loads(out)
        assert index["schema"] == "dino.proof.index.v1"
        assert len(index["proofs"]) == 1

        code, out, _ = run(["proof", "index", "metrics", str(archive)])
        assert code == 0
        metrics = json.loads(out)
        assert metrics["schema"] == "dino.proof.index.metrics.v1"
        assert metrics["total"] == 1
        assert metrics["passed"] == 1

        code, out, _ = run(["proof", "index", "compare", str(archive), proof_hash, hash16])
        assert code == 0
        assert json.loads(out)["changed"] is False

        code, out, _ = run(["proof", "index", "layout", str(archive)])
        assert code == 0
        assert json.loads(out).get("ok") is True

        code, out, _ = run(["proof", "index", "rebuild", str(archive)])
        assert code == 0
        assert json.loads(out).get("proof_count") == 1

        code, out, _ = run(["proof", "verify", "--proof", str(proof_out / "proof.json")])
        assert code == 0, out
        verify = json.loads(out)
        assert verify.get("ok") is True or verify.get("proof_hash_ok") is True

    def test_http_export(self, sim_home) -> None:
        _unlock_ea()
        work, proof_out = sim_home["work"], sim_home["proof_out"]
        received: dict = {}

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):  # noqa: N802
                length = int(self.headers.get("Content-Length", "0"))
                body = self.rfile.read(length)
                received["body"] = json.loads(body.decode("utf-8"))
                received["hash"] = self.headers.get("X-Dino-Proof-Hash")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"ok":true}')

            def log_message(self, *_args):
                return

        server = HTTPServer(("127.0.0.1", 0), Handler)
        port = server.server_address[1]
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            cmd = shlex.join(_pipeline_cmd(work))
            code, out, err = run(
                [
                    "proof",
                    "run",
                    "--command",
                    cmd,
                    "--scan",
                    str(PIPE_DIR),
                    "--output-dir",
                    str(proof_out),
                    "--pipeline",
                    "fraud_http",
                    "--group",
                    "risk-team",
                    "--export",
                    f"http://127.0.0.1:{port}/api/proofs",
                ]
            )
            assert code == 0, err
            assert received["body"]["schema"] == "dino.proof.export.v1"
            assert received["hash"] == received["body"]["proof_hash"]
            assert "index_entry" in received["body"]
        finally:
            server.shutdown()

    def test_s3_export_mocked(self, sim_home) -> None:
        _unlock_ea()
        work, proof_out = sim_home["work"], sim_home["proof_out"]

        code, payload, err = _proof_run(
            work=work, proof_out=proof_out, archive=None, pipeline="fraud_s3"
        )
        assert code == 0, err

        with patch(
            "dino.domains.proof.export._export_s3",
            return_value={
                "ok": True,
                "scheme": "s3",
                "destination": "s3://team-bucket/proofs/" + payload["proof_hash"][:16],
                "proof_hash": payload["proof_hash"],
            },
        ) as mocked:
            from dino.domains.proof.export import export_proof_dir

            report = export_proof_dir(proof_out, "s3://team-bucket/proofs")
            assert report["ok"] is True
            assert report["scheme"] == "s3"
            mocked.assert_called_once()


# ---------------------------------------------------------------------------
# 3: Determinism (many runs)
# ---------------------------------------------------------------------------


class TestDeterminism:
    def test_ten_runs_identical_proof_hash(self, sim_home) -> None:
        _unlock_ea()
        work, archive = sim_home["work"], sim_home["archive"]
        hashes: list[str] = []

        for i in range(DETERMINISM_RUNS):
            proof_out = sim_home["proof_out"].parent / f"proof_out_{i}"
            if proof_out.exists():
                shutil.rmtree(proof_out)
            proof_out.mkdir()
            # shared workdir — pipeline is deterministic
            if work.exists():
                shutil.rmtree(work)
            work.mkdir()
            code, payload, err = _proof_run(
                work=work, proof_out=proof_out, archive=archive, pipeline="fraud_score_sim"
            )
            assert code == 0, f"run {i}: {err}"
            hashes.append(payload["proof_hash"])

        assert len(set(hashes)) == 1, f"non-deterministic hashes: {hashes}"

        code, out, _ = run(["proof", "index", "show", str(archive)])
        index = json.loads(out)
        # Content-addressed: identical proofs collapse to one entry
        assert len(index["proofs"]) == 1
        assert index["proofs"][0]["hash"] == hashes[0]

        code, out, _ = run(["proof", "index", "metrics", str(archive)])
        assert code == 0
        metrics = json.loads(out)
        assert metrics["total"] == 1
        assert metrics["passed"] == 1

        code, out, _ = run(
            ["proof", "index", "compare", str(archive), hashes[0], hashes[0][:16]]
        )
        assert code == 0
        assert json.loads(out)["changed"] is False


# ---------------------------------------------------------------------------
# 4 + 6: Early Access Team Keys
# ---------------------------------------------------------------------------


class TestEarlyAccessKeys:
    def test_issue_sign_activate_unlocks_proof(self, sim_home) -> None:
        code, out, err = run(
            ["issue-key", "--team", "fraud-lab", "--days", "30"], json_mode=True
        )
        assert code == 0, err
        key = json.loads(out)["key"]
        assert key.startswith("dinoea.v1.")

        code, out, err = run(
            ["upgrade", "--pack", "proof", "--key", key], json_mode=False
        )
        assert code == 0, err
        assert "proof" in get_active_packs()
        assert is_domain_active("proof") is True
        assert is_domain_active("scan") is True

        work, proof_out, archive = sim_home["work"], sim_home["proof_out"], sim_home["archive"]
        code, payload, err = _proof_run(work=work, proof_out=proof_out, archive=archive)
        assert code == 0, err
        assert payload.get("ok") is True

        code, out, _ = run(["proof", "index", "metrics", str(archive)])
        assert code == 0

    def test_expired_key_rejects_upgrade_and_locks_proof(self, sim_home) -> None:
        # Issue already-expired key (days=0 with now in the past via issue_key now)
        key = issue_key(team="expired-team", days=0, now=1_000_000.0)
        # days=0 with now → exp = now, verify uses current time → expired
        with pytest.raises(ValueError, match="expired"):
            activate_pack("proof", key=key)

        assert "proof" not in get_active_packs()
        assert is_domain_active("proof") is True  # Snapshot Mode via free pack
        assert is_domain_active("map") is False
        assert is_domain_active("scan") is True

        code, out, err = run(
            [
                "proof",
                "run",
                "--command",
                "echo ok",
                "--scan",
                str(PIPE_DIR),
                "--output-dir",
                str(sim_home["proof_out"]),
            ]
        )
        # Free Snapshot Mode: local proof run still works without Proof Pack
        assert code == 0, err

        # Free scan still works
        code, out, err = run(["scan", "leakage", str(PIPE_DIR / "model.py")])
        assert code == 0, err

        # System Mode (export) is gated — friendly message, exit 0
        code, out, err = run(
            [
                "proof",
                "run",
                "--command",
                "echo ok",
                "--scan",
                str(PIPE_DIR),
                "--output-dir",
                str(sim_home["proof_out"]),
                "--export",
                str(sim_home["archive"]),
            ],
            json_mode=False,
        )
        assert code == 0
        assert "dino.dev/upgrade" in (out + err).lower() or "Proof Pack" in (out + err)

    def test_active_key_expires_later_auto_deactivates(self, sim_home, monkeypatch) -> None:
        import time

        import dino.early_access as ea
        import dino.license as lic

        now = time.time()
        key = issue_key(team="ticking", days=1, now=now)
        activate_pack("proof", key=key)
        assert is_domain_active("proof") is True

        real_verify = ea.verify_key

        def past_expiry(key_arg, *, now=None):
            return real_verify(key_arg, now=now or (time.time() + 86400 * 2))

        monkeypatch.setattr(ea, "verify_key", past_expiry)
        packs = lic.get_active_packs()
        assert "proof" not in packs
        assert is_domain_active("proof") is True  # free Snapshot Mode
        assert is_domain_active("map") is False
        assert is_domain_active("scan") is True


# ---------------------------------------------------------------------------
# 5: Free mode (permanent)
# ---------------------------------------------------------------------------


class TestFreeMode:
    def test_free_mode_snapshot_ok_system_gated(self, sim_home) -> None:
        # Default license is free only
        assert get_active_packs() == ["free"]

        code, out, err = run(["scan", "leakage", str(PIPE_DIR / "extract.py")])
        assert code == 0, err
        scan = json.loads(out)
        assert scan.get("ok") is True or "findings" in scan or "schema" in scan

        # Local proof run (Snapshot Mode) works without key
        code, out, err = run(
            [
                "proof",
                "run",
                "--command",
                "echo ok",
                "--scan",
                str(PIPE_DIR),
                "--output-dir",
                str(sim_home["proof_out"]),
            ]
        )
        assert code == 0, err

        # Export is System Mode — friendly gate, exit 0
        code, out, err = run(
            [
                "proof",
                "run",
                "--command",
                "echo ok",
                "--scan",
                str(PIPE_DIR),
                "--output-dir",
                str(sim_home["proof_out"]),
                "--export",
                str(sim_home["archive"]),
            ],
            json_mode=False,
        )
        assert code == 0
        assert "Proof Pack" in (out + err) or "dino.dev/upgrade" in (out + err)
        assert not (sim_home["archive"] / "proof_index.json").exists()

        code, out, err = run(
            ["proof", "index", "metrics", str(sim_home["archive"])],
            json_mode=False,
        )
        assert code == 0
        assert "Proof Pack" in (out + err) or "dino.dev/upgrade" in (out + err)


# ---------------------------------------------------------------------------
# 7: Stress
# ---------------------------------------------------------------------------


class TestStress:
    def test_10k_rows_pipeline_and_multi_export(self, sim_home) -> None:
        _unlock_ea()
        work, proof_out, archive = sim_home["work"], sim_home["proof_out"], sim_home["archive"]

        code, payload, err = _proof_run(
            work=work,
            proof_out=proof_out,
            archive=archive,
            rows=STRESS_ROWS,
            pipeline="fraud_stress",
        )
        assert code == 0, err
        report = json.loads((work / "report.json").read_text(encoding="utf-8"))
        assert report["n_rows"] == STRESS_ROWS
        assert (archive / "proof_index.json").is_file()

        # Second run with different seed via workdir change → different command args → different hash
        work2 = sim_home["work"].parent / "work2"
        work2.mkdir()
        proof2 = sim_home["proof_out"].parent / "proof2"
        proof2.mkdir()
        code2, payload2, err2 = _proof_run(
            work=work2,
            proof_out=proof2,
            archive=archive,
            rows=STRESS_ROWS,
            pipeline="fraud_stress_v2",
            extra_pipe=["--seed", "other-seed"],
        )
        assert code2 == 0, err2
        assert payload2["proof_hash"] != payload["proof_hash"]

        code, out, _ = run(
            [
                "proof",
                "index",
                "compare",
                str(archive),
                payload["proof_hash"],
                payload2["proof_hash"],
            ]
        )
        # Different pipelines → changed
        assert code == 1
        cmp = json.loads(out)
        assert cmp["changed"] is True

        code, out, _ = run(["proof", "index", "metrics", str(archive)])
        metrics = json.loads(out)
        assert metrics["total"] == 2


# ---------------------------------------------------------------------------
# 8: Failure cases
# ---------------------------------------------------------------------------


class TestFailureCases:
    def test_pipeline_exception_fails_proof(self, sim_home) -> None:
        _unlock_ea()
        work, proof_out, archive = sim_home["work"], sim_home["proof_out"], sim_home["archive"]
        code, payload, err = _proof_run(
            work=work,
            proof_out=proof_out,
            archive=archive,
            extra_pipe=["--fail"],
            pipeline="fraud_fail",
        )
        # Dino still seals the failed run (audit evidence) — exit_code recorded
        assert code == 0, err
        assert payload.get("ok") is True
        capsule = json.loads(
            (proof_out / "capsule" / "capsule.json").read_text(encoding="utf-8")
        )
        assert capsule.get("exit_code") != 0
        assert (work / "raw.csv").is_file()
        assert not (work / "report.json").exists()

    def test_export_http_unreachable(self, sim_home) -> None:
        _unlock_ea()
        work, proof_out = sim_home["work"], sim_home["proof_out"]
        cmd = shlex.join(_pipeline_cmd(work))
        code, out, err = run(
            [
                "proof",
                "run",
                "--command",
                cmd,
                "--scan",
                str(PIPE_DIR),
                "--output-dir",
                str(proof_out),
                "--pipeline",
                "fraud_bad_http",
                "--group",
                "risk-team",
                "--export",
                "http://127.0.0.1:1/nope",
            ]
        )
        assert code != 0

    def test_missing_team_key(self, sim_home) -> None:
        code, out, err = run(["upgrade", "--pack", "proof"], json_mode=False)
        assert code == 2
        assert "key" in err.lower() or "key" in out.lower()

    def test_no_artifacts_still_seals(self, sim_home) -> None:
        """Pipeline succeeds without report.json — Dino still seals the run."""
        _unlock_ea()
        work, proof_out, archive = sim_home["work"], sim_home["proof_out"], sim_home["archive"]
        code, payload, err = _proof_run(
            work=work,
            proof_out=proof_out,
            archive=archive,
            extra_pipe=["--no-artifacts"],
            pipeline="fraud_no_artifacts",
        )
        assert code == 0, err
        assert payload.get("ok") is True
        assert not (work / "report.json").exists()
