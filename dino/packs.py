"""Dino packs — free (unique niche) + proof (sellable)."""

from __future__ import annotations

from typing import Any

# Product surface after competitive cut:
#   KEEP free:  scan          (causal leakage / grammar — no real competitor)
#   KEEP proof: capsule, map, bundle, flight, verify
#   CUT:        trace, audit, guard, fence, pulse, gate, auditx
#               (lose to Burp/httpx, Evidently, gitleaks, curl, syft, custom scripts)

PACKS: dict[str, dict[str, Any]] = {
    "free": {
        "tier": "free",
        "price_hint": "€0",
        "domains": ["scan"],
        "description": (
            "Free — grammar smoke + causal leakage scan for research pipelines."
        ),
    },
    "proof": {
        "tier": "paid",
        "price_hint": "€49 once",
        "domains": ["capsule", "map", "bundle", "flight", "verify", "proof"],
        "description": (
            "Proof Pack — capsule, map, bundle, flight, verify, and proof chain."
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
