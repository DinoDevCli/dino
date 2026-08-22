"""§4 Fixture tests — kept domains."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import pytest

from tests.dino.conftest import FIXTURES, run

WORK = Path(__file__).resolve().parent / "_fixture_work"

DOMAIN_COMMANDS: dict[str, list[tuple[str, Callable[[], tuple[int, str, str]]]]] = {}


def _register(domain: str, *cases: tuple[str, Callable[[], tuple[int, str, str]]]) -> None:
    DOMAIN_COMMANDS[domain] = list(cases)


_register(
    "verify",
    ("drift", lambda: run(["verify", "drift", "--distance", "0"])),
    ("binary", lambda: run(["verify", "binary", str(FIXTURES / "verify" / "valid_attest.json")])),
)

_register(
    "scan",
    ("grammar", lambda: run(["scan", "grammar"])),
    ("leakage_forbidden", lambda: run(["scan", "leakage", str(FIXTURES / "scan" / "forbidden_import.py")])),
    ("leakage_clean", lambda: run(["scan", "leakage", str(FIXTURES / "scan" / "clean_code.py")])),
)

_register(
    "map",
    ("analyze", lambda: run(["map", "analyze", str(FIXTURES / "map" / "repo_small")])),
)


@pytest.fixture(scope="module", autouse=True)
def _work() -> None:
    WORK.mkdir(parents=True, exist_ok=True)


@pytest.mark.parametrize("domain", sorted(DOMAIN_COMMANDS))
def test_domain_has_fixture_tree(domain: str) -> None:
    alt = FIXTURES / {
        "scan": "scan",
        "verify": "verify",
        "map": "map",
        "flight": "flight",
        "bundle": "bundle",
        "capsule": "map",
        "proof": "scan",
    }.get(domain, domain)
    assert alt.exists(), f"missing fixtures for {domain}"


@pytest.mark.parametrize("domain,cases", DOMAIN_COMMANDS.items())
def test_domain_commands_no_traceback(domain: str, cases: list) -> None:
    for name, fn in cases:
        code, out, err = fn()
        assert "Traceback" not in out + err, f"{domain}/{name}"


@pytest.mark.parametrize("domain,cases", DOMAIN_COMMANDS.items())
def test_domain_commands_deterministic(domain: str, cases: list) -> None:
    for name, fn in cases:
        assert fn() == fn(), f"{domain}/{name}"
