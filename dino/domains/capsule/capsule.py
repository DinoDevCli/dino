"""Sealed execution capsule — content-addressed, no run counters."""

from __future__ import annotations

from typing import Any

from dino.common.determinism import canonical_dumps, canonical_hash


SCHEMA = "dino.capsule.capsule.v1"


def make_capsule(
    *,
    command: list[str],
    stdin: str = "",
    env: dict[str, str] | None = None,
    output: str = "",
    stderr: str = "",
    exit_code: int = 0,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a sealed capsule. `output` is canonical stdout (legacy field name)."""
    body = {
        "schema": SCHEMA,
        "command": list(command),
        "stdin": stdin,
        "env": dict(sorted((env or {}).items())),
        "output": output,
        "stderr": stderr,
        "exit_code": int(exit_code),
        "extra": extra or {},
    }
    body["capsule_hash"] = canonical_hash(body)
    return body


def dumps(capsule: dict[str, Any]) -> str:
    return canonical_dumps(capsule)


def loads(raw: str) -> dict[str, Any]:
    import json

    return json.loads(raw)
