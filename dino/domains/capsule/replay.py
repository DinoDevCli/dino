"""Replay a capsule: recompute hash and optionally re-execute the sealed command."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .capsule import make_capsule


def replay(
    capsule: dict[str, Any],
    *,
    reexec: bool = True,
    cwd: Path | None = None,
    timeout: float | None = 60.0,
) -> dict[str, Any]:
    rebuilt = make_capsule(
        command=list(capsule.get("command") or []),
        stdin=str(capsule.get("stdin") or ""),
        env=dict(capsule.get("env") or {}),
        output=str(capsule.get("output") or ""),
        stderr=str(capsule.get("stderr") or ""),
        exit_code=int(capsule.get("exit_code") or 0),
        extra=dict(capsule.get("extra") or {}),
    )
    expected = str(capsule.get("capsule_hash") or "")
    got = str(rebuilt.get("capsule_hash") or "")
    hash_ok = expected == got and bool(expected)

    exec_ok = True
    live: dict[str, Any] | None = None
    if reexec and rebuilt.get("command"):
        from .execute import run_command

        live = run_command(
            list(rebuilt["command"]),
            stdin=str(rebuilt.get("stdin") or ""),
            env=dict(rebuilt.get("env") or {}) or None,
            cwd=cwd,
            timeout=timeout,
        )
        exec_ok = (
            live["stdout"] == rebuilt.get("output", "")
            and live["stderr"] == rebuilt.get("stderr", "")
            and int(live["exit_code"]) == int(rebuilt.get("exit_code") or 0)
        )

    return {
        "schema": "dino.capsule.replay.v1",
        "replay_ok": bool(hash_ok and exec_ok),
        "hash_ok": hash_ok,
        "exec_ok": exec_ok,
        "expected_hash": expected,
        "recomputed_hash": got,
        "live": live,
        "capsule": rebuilt,
    }
