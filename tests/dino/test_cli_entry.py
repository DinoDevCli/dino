"""§1 CLI entry-point tests."""

from __future__ import annotations

import json
import shutil

import pytest

from dino import __version__
from tests.dino.conftest import DOMAINS_V3, ROOT, run, run_cli_subprocess, run_module, twice


def test_which_dino_points_at_venv_or_install() -> None:
    dino = shutil.which("dino")
    if dino is None:
        # Editable install may only expose the module entry; accept python -m.
        code, out, err = run_cli_subprocess(["version"], json_mode=False)
        assert code == 0, err
        assert out.strip() == __version__
        return
    assert __import__("pathlib").Path(dino).is_file()


def test_dino_help_lists_v3_domains() -> None:
    code, out, err = run_cli_subprocess(["--help"], json_mode=False)
    assert code == 0, err
    text = out.lower()
    for domain in DOMAINS_V3:
        assert domain in text


def test_dino_version_subcommand() -> None:
    code, out, err = run(["version"], json_mode=False)
    assert code == 0, err
    assert out.strip() == __version__


def test_python_m_dino_cli_matches_dino() -> None:
    a = run(["version"], json_mode=False)
    b = run_cli_subprocess(["version"], json_mode=False)
    assert a[0] == b[0] == 0
    assert a[1] == b[1]


@pytest.mark.parametrize("domain", ["scan", "map"])
def test_python_m_domain_module_self_test(domain: str) -> None:
    code, out, err = run_module(domain, "--self-test")
    assert code == 0, err or out
    assert "Traceback" not in out + err
    payload = json.loads(out)
    assert payload.get("ok") is True
