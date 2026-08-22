"""Execute a command into a sealed capsule (real subprocess capture)."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from dino.common.utils import write_json

from .capsule import make_capsule
from .replay import replay


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
    if not command:
        raise ValueError("command must be non-empty")
    import os

    sealed: dict[str, str] = {}
    for key in ("PATH", "LANG", "LC_ALL", "SYSTEMROOT", "COMSPEC"):
        if key in os.environ:
            sealed[key] = os.environ[key]
    if env:
        sealed.update({str(k): str(v) for k, v in env.items()})
    completed = subprocess.run(
        list(command),
        input=stdin.encode("utf-8"),
        capture_output=True,
        env=sealed,
        cwd=str(cwd) if cwd else None,
        timeout=timeout,
        check=False,
    )
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
        captured = {"stdout": recorded_output, "stderr": "", "exit_code": 0}
    else:
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
