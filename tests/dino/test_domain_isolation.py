"""§2 Domain isolation — python -m dino.domains.<domain> --self-test."""

from __future__ import annotations

import pytest

from tests.dino.conftest import DINO_ROOT, run_module, ten_times_identical

DOMAINS = [
    "scan",
    "bundle",
    "flight",
    "verify",
    "map",
    "capsule",
    "proof",
]

FORBIDDEN = ("dinodev", "archovive", "brain_tools", "causal_features", "run_v20_causal")


@pytest.mark.parametrize("domain", DOMAINS)
def test_domain_self_test_exit_zero(domain: str) -> None:
    code, out, err = run_module(domain, "--self-test")
    assert code == 0, f"{domain}: {err}\n{out}"
    assert "Traceback" not in out + err


@pytest.mark.parametrize("domain", DOMAINS)
def test_domain_self_test_deterministic(domain: str) -> None:
    def once() -> str:
        _, out, _ = run_module(domain, "--self-test")
        return out

    ten_times_identical(once)


@pytest.mark.parametrize("domain", DOMAINS)
def test_domain_no_forbidden_imports(domain: str) -> None:
    domain_dir = DINO_ROOT / "domains" / domain
    for py in domain_dir.rglob("*.py"):
        text = py.read_text(encoding="utf-8")
        for needle in FORBIDDEN:
            assert needle not in text, f"{py} references {needle}"
