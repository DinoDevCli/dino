"""Regression tests — kept surface only."""

from __future__ import annotations

import json

from tests.dino.conftest import FIXTURES, run, twice


def test_binary_no_importerror() -> None:
    att = FIXTURES / "verify" / "valid_attest.json"
    code, out, err = run(["verify", "binary", str(att)])
    assert "ImportError" not in out + err
    json.loads(out)
    twice(["verify", "binary", str(att)])


def test_scan_grammar_ok() -> None:
    code, out, _ = run(["scan", "grammar"])
    assert code == 0
    assert json.loads(out)["status"] == "ok"
    twice(["scan", "grammar"])


def test_verify_drift_aligned() -> None:
    code, out, _ = run(["verify", "drift", "--distance", "0"])
    assert code == 0
    assert json.loads(out)["bucket"] == "aligned"
    twice(["verify", "drift", "--distance", "0"])
