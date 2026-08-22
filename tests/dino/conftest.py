"""Shared helpers for Dino CLI tests."""

from __future__ import annotations

import io
import json
import subprocess
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import pytest

from dino import __version__
from dino.cli import main
from dino.license import DEFAULT_LICENSE, activate_pack, save_license
from dino.packs import PACKS

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests" / "fixtures"
if not FIXTURES.is_dir():
    FIXTURES = ROOT / "tests" / "dino" / "fixtures"
DINO_ROOT = ROOT / "dino"

DOMAINS_V3 = {
    "scan",
    "bundle",
    "flight",
    "verify",
    "map",
    "capsule",
    "proof",
}


@pytest.fixture(autouse=True)
def _all_packs_unlocked(tmp_path, monkeypatch):
    """Isolate license and unlock all packs so domain tests exercise code paths."""
    lic_dir = tmp_path / ".dino"
    lic_dir.mkdir(exist_ok=True)
    monkeypatch.setattr("dino.license.LICENSE_DIR", lic_dir)
    monkeypatch.setattr("dino.license.LICENSE_PATH", lic_dir / "license.json")
    save_license(dict(DEFAULT_LICENSE))
    for pack in PACKS:
        activate_pack(pack, key="test")


def run(argv: list[str], *, json_mode: bool = True) -> tuple[int, str, str]:
    cmd = list(argv)
    if json_mode and "--json" not in cmd:
        cmd = ["--json", *cmd]
    out, err = io.StringIO(), io.StringIO()
    old = list(sys.argv)
    try:
        sys.argv = ["dino", *cmd]
        with redirect_stdout(out), redirect_stderr(err):
            code = main(cmd)
    finally:
        sys.argv = old
    stdout = out.getvalue()
    stdout = _unwrap_envelope(stdout)
    return int(code), stdout, err.getvalue()


def _unwrap_envelope(stdout: str) -> str:
    text = stdout.strip()
    if not text.startswith("{"):
        return stdout
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return stdout
    if "result" in payload:
        return json.dumps(payload["result"], indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if "error" in payload:
        return json.dumps(payload["error"], indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    return stdout


def run_module(domain: str, *argv: str) -> tuple[int, str, str]:
    cmd = [sys.executable, "-m", f"dino.domains.{domain}", *argv]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    return proc.returncode, proc.stdout, proc.stderr


def run_cli_subprocess(argv: list[str], *, json_mode: bool = True) -> tuple[int, str, str]:
    cmd = [sys.executable, "-m", "dino.cli"]
    if json_mode:
        cmd.append("--json")
    cmd.extend(argv)
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    stdout = _unwrap_envelope(proc.stdout)
    return proc.returncode, stdout, proc.stderr


def twice(argv: list[str], *, json_mode: bool = True) -> None:
    a = run(argv, json_mode=json_mode)
    b = run(argv, json_mode=json_mode)
    assert a[0] == b[0], (a, b)
    assert a[1] == b[1], (a[1], b[1])
    assert a[2] == b[2], (a[2], b[2])


def ten_times_identical(fn) -> None:
    outputs = [fn() for _ in range(10)]
    first = outputs[0]
    for i, out in enumerate(outputs[1:], start=2):
        assert out == first, f"run {i} differed from run 1"
