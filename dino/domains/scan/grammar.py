"""Minimal expression grammar for candidate generation. Not a trading language."""

from __future__ import annotations

import re
from typing import Any

from dino.common.determinism import canonical_hash

VERSION = "ALPHA_GRAMMAR_V1"

TOKEN = re.compile(r"\s*([A-Za-z_][A-Za-z0-9_]*|\d+|[(),+\-*/])")


def tokenize(src: str) -> list[str]:
    return [m.group(1) for m in TOKEN.finditer(src)]


def audit(src: str) -> dict[str, Any]:
    tokens = tokenize(src)
    ok = bool(src.strip()) and bool(tokens)
    if tokens and tokens[0] in {")", ",", "*", "/", "+"}:
        ok = False
    depth = 0
    prev = ""
    for t in tokens:
        if t == "(":
            depth += 1
        elif t == ")":
            depth -= 1
            if depth < 0:
                ok = False
        if prev in "+-*/" and t in "+-*/":
            ok = False
        prev = t
    if depth != 0:
        ok = False
    payload = {"ok": ok, "tokens": tokens, "source": src, "version": VERSION}
    payload["fingerprint"] = canonical_hash({"ok": ok, "tokens": tokens, "source": src, "version": VERSION})
    return payload


def smoke() -> dict[str, Any]:
    valid = ["sum(a, b)", "x + 1", "scale(x)"]
    invalid = ["+", "foo(", "))"]
    return {
        "status": "ok",
        "version": VERSION,
        "backend": "dino.domains.scan.grammar",
        "valid": [audit(s)["ok"] for s in valid],
        "invalid": [not audit(s)["ok"] for s in invalid],
    }
