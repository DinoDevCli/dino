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
    assert "Core Workflow:" in text
    assert "Pipeline Operations:" in text
    assert "System & Packs:" in text
    assert "Early Access (Proof Pack)" in text
    assert "dinodevcli@gmail.com" in text
    assert "open-source scan engine" in text
    assert "https://github.com/DinoDevCli/dino#early-access" in text


def test_proof_run_and_compare_help_mention_early_access() -> None:
    for argv in (
        ["proof", "run", "--help"],
        ["proof", "index", "compare", "--help"],
        ["run", "--help"],
    ):
        code, out, err = run(argv, json_mode=False)
        assert code == 0, f"{argv}: {err}\n{out}"
        text = out + err
        assert "Early Access (Proof Pack)" in text
        assert "CI compare gate" in text
        assert "dinodevcli@gmail.com" in text


def test_compare_help_distinct_hash_metavars() -> None:
    code, out, err = run(["proof", "index", "compare", "--help"], json_mode=False)
    assert code == 0, err
    text = out + err
    assert "HASH_A" in text
    assert "HASH_B" in text
    assert "usage:" in text
    # usage line should not show duplicate bare HASH HASH
    usage = next((ln for ln in text.splitlines() if ln.startswith("usage:")), "")
    assert "HASH_A" in usage and "HASH_B" in usage


def test_packs_mentions_proof_pack_help() -> None:
    code, out, err = run(["packs"], json_mode=False)
    assert code == 0, err
    text = out + err
    assert "Early Access / Proof Pack" in text
    assert "dinodevcli@gmail.com" in text


def test_run_alias_matches_proof_run() -> None:
    code, out, err = run(
        ["run", "--command", "echo", "alias-ok", "--output-dir", "./_cli_run_alias"],
        json_mode=True,
    )
    assert code == 0, f"{err}\n{out}"


def test_run_trailing_command() -> None:
    code, out, err = run(
        ["run", "--output-dir", "./_cli_run_trail", "--", "echo", "trail-ok"],
        json_mode=True,
    )
    assert code == 0, f"{err}\n{out}"


@pytest.mark.parametrize("domain", DOMAINS)
def test_domain_help(domain: str) -> None:
    code, out, err = run([domain, "--help"], json_mode=False)
    assert code == 0, f"{domain}: {err}\n{out}"
    assert "Traceback" not in out + err
