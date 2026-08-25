"""§14 CLI help sweep."""

from __future__ import annotations

import pytest

from tests.dino.conftest import DOMAINS_V3, run

DOMAINS = sorted(DOMAINS_V3)


def test_top_level_help() -> None:
    code, out, err = run(["--help"], json_mode=False)
    assert code == 0, err
    assert "Traceback" not in out + err
    text = out + err
    assert "Optional features (Proof Pack)" in text
    assert "dinodevcli@gmail.com" in text
    assert "open-source scan engine" in text


def test_proof_run_and_compare_help_mention_proof_pack() -> None:
    for argv in (["proof", "run", "--help"], ["proof", "index", "compare", "--help"]):
        code, out, err = run(argv, json_mode=False)
        assert code == 0, f"{argv}: {err}\n{out}"
        text = out + err
        assert "Optional features (Proof Pack)" in text
        assert "CI compare gate" in text
        assert "dinodevcli@gmail.com" in text


def test_packs_mentions_proof_pack_help() -> None:
    code, out, err = run(["packs"], json_mode=False)
    assert code == 0, err
    text = out + err
    assert "Optional features / Proof Pack" in text
    assert "dinodevcli@gmail.com" in text


@pytest.mark.parametrize("domain", DOMAINS)
def test_domain_help(domain: str) -> None:
    code, out, err = run([domain, "--help"], json_mode=False)
    assert code == 0, f"{domain}: {err}\n{out}"
    assert "Traceback" not in out + err
