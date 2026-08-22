"""§13 Kept-domain determinism."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.dino.conftest import FIXTURES, ROOT, run, ten_times_identical

WORK = Path(__file__).resolve().parent / "_new_domains_work"


@pytest.fixture(scope="module", autouse=True)
def _work() -> None:
    WORK.mkdir(parents=True, exist_ok=True)


def test_map_verify_deterministic() -> None:
    repo = FIXTURES / "brain" / "repo_small"
    if not repo.is_dir():
        repo = ROOT / "dino" / "common"
    argv = ["map", "verify", "--repo", str(repo)]
    ten_times_identical(lambda: run(argv)[1])


def test_capsule_run_replay_deterministic() -> None:
    outdir = WORK / "capsule_exec"
    argv = ["capsule", "run", "--output-dir", str(outdir), "--command", "echo", "ok"]
    ten_times_identical(lambda: run(argv)[1])
    cap = outdir / "capsule.json"
    rep = ["capsule", "replay", "--capsule", str(cap), "--output-dir", str(outdir)]
    ten_times_identical(lambda: run(rep)[1])


def test_scan_grammar_deterministic() -> None:
    ten_times_identical(lambda: run(["scan", "grammar"])[1])
