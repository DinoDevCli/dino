"""Shared helpers for production simulation — isolated license per test via fixtures."""

from __future__ import annotations

import io
import json
import sys
from contextlib import redirect_stderr, redirect_stdout

from dino.cli import main


def run(argv: list[str], *, json_mode: bool = True) -> tuple[int, str, str]:
    cmd = list(argv)
    if json_mode and "--json" not in cmd:
        cmd = ["--json", *cmd]
    out, err = io.StringIO(), io.StringIO()
    old = list(sys.argv)
    try:
        sys.argv = ["dino", *cmd]
        with redirect_stdout(out), redirect_stderr(err):
            code = main(cmd)
    finally:
        sys.argv = old
    stdout = out.getvalue()
    text = stdout.strip()
    if text.startswith("{"):
        try:
            payload = json.loads(text)
            if "result" in payload:
                stdout = (
                    json.dumps(payload["result"], indent=2, sort_keys=True, ensure_ascii=False)
                    + "\n"
                )
            elif "error" in payload:
                stdout = (
                    json.dumps(payload["error"], indent=2, sort_keys=True, ensure_ascii=False)
                    + "\n"
                )
        except json.JSONDecodeError:
            pass
    return int(code), stdout, err.getvalue()
