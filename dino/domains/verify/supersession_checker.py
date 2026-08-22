"""Runtime verdict supersession — contract revision when post-release exposure overrides gate."""
from __future__ import annotations

from typing import Any


def apply_runtime_supersession(
    contract_doc: dict[str, Any],
    *,
    previous_doc: dict[str, Any] | None,
    runtime_verdict: str,
    release_verdict: str,
) -> dict[str, Any]:
    """
    Gate produces revision=0.
    Runtime override (DENY/WARN vs APPROVED release) produces revision=1, supersedes=<old_id>.
    """
    out = dict(contract_doc)
    decision = dict(out.get("decision") or {})
    runtime_v = str(runtime_verdict or "ALLOW").upper()
    release_v = str(release_verdict or decision.get("verdict") or "").upper()
    # Aliases: REJECTED/BLOCK/FAIL map to DENY for CLI ergonomics
    if runtime_v in {"REJECTED", "BLOCK", "FAIL", "DENIED"}:
        runtime_v = "DENY"
    if release_v in {"PASS", "OK"}:
        release_v = "APPROVED"

    prev_decision = (previous_doc or {}).get("decision") or {}
    prev_id = str(prev_decision.get("decision_id") or prev_decision.get("decision_hash") or "")
    prev_revision = int(prev_decision.get("revision") or 0)

    runtime_overrides = (
        runtime_v in ("DENY", "WARN")
        and release_v == "APPROVED"
        and runtime_v != "ALLOW"
    )

    if runtime_overrides and prev_id:
        decision["revision"] = prev_revision + 1
        decision["supersedes"] = prev_id
        decision["runtime_supersedes"] = True
    else:
        decision.setdefault("revision", 0)
        decision.setdefault("supersedes", None)
        decision["runtime_supersedes"] = False

    exposure = dict(out.get("runtime_exposure") or {})
    exposure["runtime_supersedes"] = decision["runtime_supersedes"]
    out["runtime_exposure"] = exposure
    out["decision"] = decision
    return out


def verify_supersession_chain(
    contract_doc: dict[str, Any],
    *,
    previous_doc: dict[str, Any] | None,
) -> tuple[bool, str]:
    """Detect supersession chain tampering."""
    decision = contract_doc.get("decision") or {}
    supersedes = decision.get("supersedes")
    revision = int(decision.get("revision") or 0)

    if not supersedes:
        if revision != 0:
            return False, "revision must be 0 when supersedes is absent"
        return True, "ok"

    if not previous_doc:
        return False, "supersedes set but no previous contract provided"

    prev = previous_doc.get("decision") or {}
    prev_id = str(prev.get("decision_id") or prev.get("decision_hash") or "")
    if supersedes != prev_id:
        return False, "supersedes does not match previous decision_id"

    prev_revision = int(prev.get("revision") or 0)
    if revision != prev_revision + 1:
        return False, "revision must increment by 1 on supersession"

    return True, "ok"
