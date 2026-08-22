"""§5 Cross-domain isolation — kept domains."""

from __future__ import annotations

import ast

import pytest

from tests.dino.conftest import DINO_ROOT


@pytest.mark.parametrize(
    "domain,forbidden",
    [
        ("scan", {"map", "capsule", "verify", "bundle"}),
        ("bundle", {"map", "capsule"}),
        ("capsule", {"map", "scan"}),
    ],
)
def test_no_cross_domain_imports(domain: str, forbidden: set[str]) -> None:
    root = DINO_ROOT / "domains" / domain
    for py in root.rglob("*.py"):
        tree = ast.parse(py.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            mod = None
            if isinstance(node, ast.ImportFrom) and node.module:
                mod = node.module
            if mod and mod.startswith("dino.domains."):
                other = mod.split(".")[2]
                assert other == domain, f"{py} imports dino.domains.{other}"
                assert other not in forbidden
