"""§3 Determinism matrix — kept product domains only."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.dino.conftest import FIXTURES, ROOT, run, ten_times_identical

WORK = Path(__file__).resolve().parent / "_matrix_work"


@pytest.fixture(scope="module", autouse=True)
def _ensure_work_dir() -> None:
    WORK.mkdir(parents=True, exist_ok=True)


def _cmd_map_verify() -> str:
    repo = FIXTURES / "brain" / "repo_small"
    if not repo.is_dir():
        repo = ROOT / "dino" / "common"
    return run(["map", "verify", "--repo", str(repo)])[1]


def _cmd_capsule_doctor() -> str:
    outdir = WORK / "capsule_doctor"
    return run(["capsule", "doctor", "--output-dir", str(outdir)])[1]


def _cmd_scan_grammar() -> str:
    return run(["scan", "grammar"])[1]


def _cmd_verify_drift() -> str:
    return run(["verify", "drift", "--distance", "0"])[1]


MATRIX = [
    ("map_verify", _cmd_map_verify),
    ("capsule_doctor", _cmd_capsule_doctor),
    ("scan_grammar", _cmd_scan_grammar),
    ("verify_drift", _cmd_verify_drift),
]


@pytest.mark.parametrize("name,fn", MATRIX, ids=[m[0] for m in MATRIX])
def test_command_output_stable_10x(name: str, fn) -> None:
    ten_times_identical(fn)


@pytest.mark.parametrize("name,fn", MATRIX, ids=[m[0] for m in MATRIX])
def test_no_timestamps_in_output(name: str, fn) -> None:
    out = fn()
    assert "Traceback" not in out
    import re

    assert not re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", out)
    payload = json.loads(out)
    assert payload is not None
