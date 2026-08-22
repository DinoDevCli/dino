"""§6 Path purity."""

from __future__ import annotations

import pytest

from tests.dino.conftest import DINO_ROOT

FORBIDDEN = ["dinodev", "archovive", "brain_tools", "causal_features", "run_v20_causal"]


@pytest.mark.parametrize("needle", FORBIDDEN)
def test_no_forbidden_strings_in_dino_tree(needle: str) -> None:
    hits: list[str] = []
    for path in DINO_ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in {".py", ".md", ".json", ".yaml", ".yml", ".toml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if needle in text:
            hits.append(str(path.relative_to(DINO_ROOT)))
    assert hits == [], f"{needle} found in: {hits}"
