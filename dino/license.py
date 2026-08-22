"""Local license stub for Dino packs (~/.dino/license.json)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .packs import ALL_DOMAINS, DOMAIN_TO_PACKS, PACKS, resolve_pack_name

LICENSE_DIR = Path.home() / ".dino"
LICENSE_PATH = LICENSE_DIR / "license.json"

DEFAULT_LICENSE: dict[str, Any] = {
    "schema": "dino_license_v2",
    "active_packs": ["free"],
    "keys": {},
}


def _normalize_packs(packs: list[Any]) -> list[str]:
    out: list[str] = []
    for raw in packs:
        name = resolve_pack_name(str(raw))
        if name not in PACKS:
            continue
        if name not in out:
            out.append(name)
    if not out:
        out = ["free"]
    if "free" not in out:
        out.insert(0, "free")
    return out


def load_license() -> dict[str, Any]:
    if not LICENSE_PATH.is_file():
        return dict(DEFAULT_LICENSE)
    try:
        data = json.loads(LICENSE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return dict(DEFAULT_LICENSE)
    if not isinstance(data, dict):
        return dict(DEFAULT_LICENSE)
    packs = data.get("active_packs")
    if not isinstance(packs, list):
        packs = list(DEFAULT_LICENSE["active_packs"])
    keys = data.get("keys")
    if not isinstance(keys, dict):
        keys = {}
    norm_keys = {resolve_pack_name(str(k)): str(v) for k, v in keys.items()}
    return {
        "schema": data.get("schema", "dino_license_v2"),
        "active_packs": _normalize_packs(packs),
        "keys": {k: v for k, v in norm_keys.items() if k in PACKS},
    }


def save_license(data: dict[str, Any]) -> Path:
    LICENSE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": data.get("schema", "dino_license_v2"),
        "active_packs": _normalize_packs(list(data.get("active_packs") or [])),
        "keys": {
            resolve_pack_name(str(k)): str(v)
            for k, v in dict(data.get("keys") or {}).items()
            if resolve_pack_name(str(k)) in PACKS
        },
    }
    LICENSE_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return LICENSE_PATH


def get_active_packs() -> list[str]:
    return list(load_license().get("active_packs") or ["free"])


def is_pack_active(pack: str) -> bool:
    return resolve_pack_name(pack) in get_active_packs()


def is_domain_active(domain: str) -> bool:
    if domain not in ALL_DOMAINS:
        return True  # unknown domains are not gated
    active = set(get_active_packs())
    for pack in DOMAIN_TO_PACKS.get(domain, []):
        if pack in active:
            return True
    return False


def activate_pack(pack: str, key: str = "") -> dict[str, Any]:
    name = resolve_pack_name(pack)
    if name not in PACKS:
        raise ValueError(f"Unknown pack: {pack}. Known: {', '.join(sorted(PACKS))}")
    lic = load_license()
    packs = list(lic.get("active_packs") or [])
    if name not in packs:
        packs.append(name)
    lic["active_packs"] = packs
    keys = dict(lic.get("keys") or {})
    if key:
        keys[name] = key
    lic["keys"] = keys
    save_license(lic)
    return lic


def required_packs_for_domain(domain: str) -> list[str]:
    return list(DOMAIN_TO_PACKS.get(domain, []))
