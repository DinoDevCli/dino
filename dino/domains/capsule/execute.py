"""Execute a command into a sealed capsule (real subprocess capture)."""

from __future__ import annotations

import shlex
import subprocess
from pathlib import Path
from typing import Any

from dino.common.utils import write_json

from .capsule import make_capsule
from .replay import replay


def normalize_command(command: list[str] | str) -> list[str]:
    """Accept argv list or a single shell-like string (e.g. ``\"echo ok\"``)."""
    if isinstance(command, str):
        parts = shlex.split(command)
    else:
        parts = [str(x) for x in command]
    if len(parts) == 1 and (" " in parts[0] or "\t" in parts[0]):
        parts = shlex.split(parts[0])
    if not parts:
        raise ValueError("command must be non-empty")
    return parts


def _normalize_text(raw: bytes | str) -> str:
    if isinstance(raw, bytes):
        text = raw.decode("utf-8", errors="replace")
    else:
        text = raw
    return text.replace("\r\n", "\n").replace("\r", "\n")


def run_command(
    command: list[str],
    *,
    stdin: str = "",
    env: dict[str, str] | None = None,
    cwd: Path | None = None,
    timeout: float | None = 60.0,
) -> dict[str, Any]:
    """Run command with sealed env (PATH retained; no ambient secret leakage)."""
    command = normalize_command(command)
    import os

    sealed: dict[str, str] = {}
    for key in ("PATH", "LANG", "LC_ALL", "SYSTEMROOT", "COMSPEC"):
        if key in os.environ:
            sealed[key] = os.environ[key]
    if env:
        sealed.update({str(k): str(v) for k, v in env.items()})
    try:
        completed = subprocess.run(
            list(command),
            input=stdin.encode("utf-8"),
            capture_output=True,
            env=sealed,
            cwd=str(cwd) if cwd else None,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        raise ValueError(
            f"command not found: {command[0]!r}. "
            "Pass argv tokens (e.g. --command echo ok), "
            "or one shell-like string (e.g. --command \"echo ok\")."
        ) from exc
    except OSError as exc:
        raise ValueError(f"failed to execute {command!r}: {exc}") from exc
    return {
        "stdout": _normalize_text(completed.stdout),
        "stderr": _normalize_text(completed.stderr),
        "exit_code": int(completed.returncode),
    }


def execute(
    command: list[str],
    *,
    output_dir: Path,
    stdin: str = "",
    env: dict[str, str] | None = None,
    recorded_output: str | None = None,
    cwd: Path | None = None,
    timeout: float | None = 60.0,
    reexec_on_seal: bool = True,
) -> dict[str, Any]:
    """
    Seal a real command run into capsule.json and verify replay.

    If recorded_output is set, skip live capture (legacy/test injection).
    Otherwise subprocess runs once to capture stdout/stderr/exit_code.
    """
    if recorded_output is not None:
        command = normalize_command(command)
        captured = {"stdout": recorded_output, "stderr": "", "exit_code": 0}
    else:
        command = normalize_command(command)
        captured = run_command(command, stdin=stdin, env=env, cwd=cwd, timeout=timeout)

    capsule = make_capsule(
        command=command,
        stdin=stdin,
        env=env,
        output=captured["stdout"],
        stderr=captured["stderr"],
        exit_code=captured["exit_code"],
    )
    output_dir = output_dir.resolve()
    write_json(output_dir / "capsule.json", capsule)
    report = replay(capsule, reexec=reexec_on_seal, cwd=cwd, timeout=timeout)
    write_json(output_dir / "replay.json", report)
    return {
        "output_dir": str(output_dir),
        "capsule_hash": capsule["capsule_hash"],
        "replay_ok": report["replay_ok"],
        "exit_code": capsule["exit_code"],
        "stdout_bytes": len(capsule["output"].encode("utf-8")),
        "stderr_bytes": len(capsule["stderr"].encode("utf-8")),
        "hash_ok": report.get("hash_ok"),
        "exec_ok": report.get("exec_ok"),
    }
