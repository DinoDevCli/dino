"""Dino packs — Free Snapshot Mode + Proof Pack System Mode."""

from __future__ import annotations

from typing import Any

# Product surface after competitive cut:
#   KEEP free:  scan, proof (local run), capsule (run/replay)
#   KEEP proof: map, bundle, flight, verify + proof system features
#   CUT:        trace, audit, guard, fence, pulse, gate, auditx
#               (lose to Burp/httpx, Evidently, gitleaks, curl, syft, custom scripts)

PACKS: dict[str, dict[str, Any]] = {
    "free": {
        "tier": "free",
        "price_hint": "forever · Snapshot Mode",
        "domains": ["scan", "proof", "capsule"],
        "description": (
            "Free Snapshot Mode — local scan, local proof run (no export), "
            "and local capsule run/replay."
        ),
    },
    "proof": {
        "tier": "ea",
        "price_hint": "Proof Pack · Team Key",
        "domains": ["capsule", "map", "bundle", "flight", "verify", "proof"],
        "description": (
            "Proof Pack (System Mode) — history, comparison, CI gates, "
            "export (Path/HTTP/S3), team metadata, map, bundle, verify, flight."
        ),
    },
}

PACK_ALIASES: dict[str, str] = {
    "community": "free",
    "devops": "free",
    "domain": "free",
    "research": "free",
    "pro": "proof",
    "enterprise": "proof",
    "trust": "proof",
}

DOMAIN_TO_PACKS: dict[str, list[str]] = {}
for _pack, _meta in PACKS.items():
    for _dom in _meta["domains"]:
        DOMAIN_TO_PACKS.setdefault(_dom, []).append(_pack)

ALL_DOMAINS = sorted(DOMAIN_TO_PACKS.keys())


def resolve_pack_name(name: str) -> str:
    key = name.strip().lower()
    return PACK_ALIASES.get(key, key)


def required_packs_for_domain(domain: str) -> list[str]:
    return list(DOMAIN_TO_PACKS.get(domain, []))
