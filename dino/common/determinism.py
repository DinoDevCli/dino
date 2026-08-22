"""Canonical JSON and hash helpers. No wall-clock unless DINO_CLOCK is set."""

from __future__ import annotations

import hashlib
import json
import os
from typing import Any


def canonical_dumps(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(canonical_dumps(obj).encode("utf-8")).hexdigest()


def stable_clock() -> str:
    """Empty unless callers pin DINO_CLOCK (tests never set this)."""
    return os.environ.get("DINO_CLOCK", "")
