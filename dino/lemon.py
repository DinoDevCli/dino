"""Lemon Squeezy license validation for paid Dino packs."""

from __future__ import annotations

import os
import socket
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

LEMON_ACTIVATE_URL = "https://api.lemonsqueezy.com/v1/licenses/activate"
LEMON_VALIDATE_URL = "https://api.lemonsqueezy.com/v1/licenses/validate"

# Offline / CI allowlist: comma-separated keys that skip remote calls.
OFFLINE_KEYS_ENV = "DINO_OFFLINE_LICENSE_KEYS"
# When set to "1", skip remote and accept any non-empty key (local hacking only).
SKIP_REMOTE_ENV = "DINO_LICENSE_SKIP_REMOTE"


def _offline_keys() -> set[str]:
    raw = os.environ.get(OFFLINE_KEYS_ENV, "")
    return {part.strip() for part in raw.split(",") if part.strip()}


def _skip_remote() -> bool:
    return os.environ.get(SKIP_REMOTE_ENV, "").strip() in {"1", "true", "yes"}


def default_instance_name() -> str:
    host = socket.gethostname() or "dino"
    return f"dino@{host}"[:100]


def _post_form(url: str, fields: dict[str, str], *, timeout: float = 20.0) -> dict[str, Any]:
    body = urllib.parse.urlencode(fields).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "dino-cli/0.3",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            import json

            data = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            data = {}
        err = data.get("error") or data.get("message") or f"HTTP {exc.code}"
        raise ValueError(f"Lemon Squeezy license API error: {err}") from exc
    except urllib.error.URLError as exc:
        raise ValueError(
            "Could not reach Lemon Squeezy to validate the license key. "
            "Check network access, then retry: dino upgrade --pack proof --key YOUR_KEY"
        ) from exc

    import json

    try:
        return json.loads(raw) if raw else {}
    except json.JSONDecodeError as exc:
        raise ValueError("Lemon Squeezy returned invalid JSON") from exc


def validate_proof_key(key: str, *, instance_name: str | None = None) -> dict[str, Any]:
    """
    Validate / activate a Proof-pack license key.

    Order: Early Access signed key → offline allowlist → Lemon Squeezy.
    Returns a small meta dict suitable for storing under license.json.
    """
    key = (key or "").strip()
    if not key:
        raise ValueError("license key must be non-empty")

    from dino.early_access import is_early_access_key, verify_key

    if is_early_access_key(key):
        meta = verify_key(key)
        meta["instance_name"] = instance_name or default_instance_name()
        return meta

    if _skip_remote() or key in _offline_keys():
        return {
            "provider": "offline",
            "key": key,
            "status": "active",
            "instance_name": instance_name or default_instance_name(),
        }

    name = instance_name or default_instance_name()
    data = _post_form(
        LEMON_ACTIVATE_URL,
        {"license_key": key, "instance_name": name},
    )
    if data.get("activated"):
        lic = data.get("license_key") or {}
        return {
            "provider": "lemonsqueezy",
            "key": key,
            "status": str(lic.get("status") or "active"),
            "instance_id": (data.get("instance") or {}).get("id"),
            "instance_name": name,
            "meta": data.get("meta") or {},
        }

    # Already at activation limit or previously activated: validate the key itself.
    checked = _post_form(LEMON_VALIDATE_URL, {"license_key": key})
    if checked.get("valid"):
        lic = checked.get("license_key") or {}
        return {
            "provider": "lemonsqueezy",
            "key": key,
            "status": str(lic.get("status") or "active"),
            "instance_id": (checked.get("instance") or {}).get("id"),
            "instance_name": name,
            "meta": checked.get("meta") or {},
        }

    err = checked.get("error") or data.get("error") or "activation failed"
    raise ValueError(f"License key rejected: {err}")
