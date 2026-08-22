"""Unified CLI output — Deterministic Proof for Python Decision Pipelines."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from typing import Any

from dino import __version__

_LINE = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"


def _normalize_result(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    if isinstance(value, dict):
        return value
    if isinstance(value, (list, tuple)):
        return list(value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return {"value": str(value)}


def success_envelope(domain: str, command: str, result: Any) -> dict[str, Any]:
    return {
        "domain": domain,
        "command": command,
        "version": __version__,
        "timestamp": None,
        "result": _normalize_result(result),
    }


def error_envelope(domain: str, command: str, error_type: str, detail: str) -> dict[str, Any]:
    return {
        "domain": domain,
        "command": command,
        "version": __version__,
        "timestamp": None,
        "error": {"type": error_type, "detail": detail},
    }


def dumps_envelope(envelope: dict[str, Any]) -> str:
    return json.dumps(envelope, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def format_text_payload(payload: str) -> str:
    return payload.rstrip("\n")


def format_text_success(domain: str, command: str, payload: str) -> str:
    body = format_text_payload(payload)
    return "\n".join(
        [
            f"🔍 {domain} {command}",
            _LINE,
            body,
            _LINE,
            "✅ Done",
            "",
        ]
    )


def format_text_error(error_type: str, detail: str) -> str:
    return f"❌ Error: {error_type}\n{detail.rstrip()}\n"


def _result_to_text(result: Any) -> str:
    normalized = _normalize_result(result)
    if isinstance(normalized, str):
        return normalized
    if isinstance(normalized, dict):
        return json.dumps(normalized, indent=2, sort_keys=True, ensure_ascii=False)
    if isinstance(normalized, list):
        if all(isinstance(x, str) for x in normalized):
            return "\n".join(normalized)
        return json.dumps(normalized, indent=2, sort_keys=True, ensure_ascii=False)
    return str(normalized)


class Output:
    def __init__(self, *, domain: str, command: str, json_mode: bool = False) -> None:
        self.domain = domain
        self.command = command
        self.json_mode = json_mode

    def emit_success(self, result: Any) -> None:
        if self.json_mode:
            sys.stdout.write(dumps_envelope(success_envelope(self.domain, self.command, result)))
            return
        sys.stdout.write(format_text_success(self.domain, self.command, _result_to_text(result)))

    def emit_error(self, error_type: str, detail: str, *, stream: Any = None) -> None:
        if self.json_mode:
            sys.stdout.write(dumps_envelope(error_envelope(self.domain, self.command, error_type, detail)))
            return
        target = stream or sys.stderr
        target.write(format_text_error(error_type, detail))
