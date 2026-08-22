"""§14 CLI help sweep."""

from __future__ import annotations

import pytest

from tests.dino.conftest import DOMAINS_V3, run

DOMAINS = sorted(DOMAINS_V3)


def test_top_level_help() -> None:
    code, out, err = run(["--help"], json_mode=False)
    assert code == 0, err
    assert "Traceback" not in out + err


@pytest.mark.parametrize("domain", DOMAINS)
def test_domain_help(domain: str) -> None:
    code, out, err = run([domain, "--help"], json_mode=False)
    assert code == 0, f"{domain}: {err}\n{out}"
    assert "Traceback" not in out + err
