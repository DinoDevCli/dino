"""Early Access Team Keys — HMAC-signed, expiry-aware (no Lemon required).

Format: ``dinoea.v1.<payload_b64>.<sig_b64>``

Payload (JSON): ``{"pack":"proof","team":"...","exp":<unix_ts>}``

Signing secret: env ``DINO_EA_SIGNING_SECRET`` (required to issue; verify uses same).
For CI / local sim: set a known secret and issue keys with ``issue_key``.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import time
from typing import Any

PREFIX = "dinoea.v1."
SIGNING_SECRET_ENV = "DINO_EA_SIGNING_SECRET"
# Fallback only for tests / local simulation — never use in production issuance.
DEFAULT_SIM_SECRET = "dino-early-access-sim-secret"


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(text: str) -> bytes:
    pad = "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(text + pad)


def signing_secret() -> bytes:
    raw = os.environ.get(SIGNING_SECRET_ENV, "").strip()
    if not raw:
        raw = DEFAULT_SIM_SECRET
    return raw.encode("utf-8")


def is_early_access_key(key: str) -> bool:
    return (key or "").strip().startswith(PREFIX)


def issue_key(
    *,
    team: str,
    days: int = 90,
    pack: str = "proof",
    now: float | None = None,
) -> str:
    """Generate a signed Early Access Team Key."""
    team = (team or "").strip()
    if not team:
        raise ValueError("team name required")
    if days < 0:
        raise ValueError("days must be >= 0")
    ts = int(now if now is not None else time.time())
    payload = {
        "pack": pack,
        "team": team,
        "exp": ts + int(days) * 86400,
        "iat": ts,
    }
    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    sig = hmac.new(signing_secret(), body, hashlib.sha256).digest()
    return f"{PREFIX}{_b64url(body)}.{_b64url(sig)}"


def verify_key(key: str, *, now: float | None = None) -> dict[str, Any]:
    """
    Verify signature and expiry.

    Returns meta dict with status ``active`` or raises ValueError if invalid/expired.
    """
    key = (key or "").strip()
    if not is_early_access_key(key):
        raise ValueError("not an Early Access key")
    rest = key[len(PREFIX) :]
    if "." not in rest:
        raise ValueError("malformed Early Access key")
    payload_b64, sig_b64 = rest.rsplit(".", 1)
    try:
        body = _b64url_decode(payload_b64)
        sig = _b64url_decode(sig_b64)
    except (ValueError, OSError) as exc:
        raise ValueError("malformed Early Access key encoding") from exc

    expected = hmac.new(signing_secret(), body, hashlib.sha256).digest()
    if not hmac.compare_digest(sig, expected):
        raise ValueError("Early Access key signature invalid")

    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Early Access key payload invalid") from exc

    if not isinstance(payload, dict):
        raise ValueError("Early Access key payload invalid")
    exp = int(payload.get("exp") or 0)
    ts = int(now if now is not None else time.time())
    if exp <= ts:
        raise ValueError(
            f"Early Access key expired at {exp} (team={payload.get('team')})"
        )

    return {
        "provider": "early_access",
        "key": key,
        "status": "active",
        "expires_at": exp,
        "team": str(payload.get("team") or ""),
        "pack": str(payload.get("pack") or "proof"),
        "meta": payload,
    }


def key_expiry(key: str) -> int | None:
    """Return exp unix ts without verifying signature (for diagnostics)."""
    if not is_early_access_key(key):
        return None
    try:
        rest = key[len(PREFIX) :]
        payload_b64 = rest.rsplit(".", 1)[0]
        payload = json.loads(_b64url_decode(payload_b64).decode("utf-8"))
        return int(payload.get("exp") or 0)
    except (ValueError, OSError, json.JSONDecodeError, UnicodeDecodeError):
        return None
