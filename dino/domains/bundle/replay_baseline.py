"""Lab replay baseline for regression."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ReplayBaseline:
    target_id: str
    true_count: int = 0
    verified_count: int = 0
    endpoint_count: int = 0
    xhr_count: int = 0
    dual_session_diffs: int = 0
    mutation_count: int = 0
    phi_summary: dict[str, Any] = field(default_factory=dict)
    psi_summary: dict[str, Any] = field(default_factory=dict)
    evidence_summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_id": self.target_id,
            "true_count": self.true_count,
            "verified_count": self.verified_count,
            "endpoint_count": self.endpoint_count,
            "xhr_count": self.xhr_count,
            "dual_session_diffs": self.dual_session_diffs,
            "mutation_count": self.mutation_count,
            "phi_summary": self.phi_summary,
            "psi_summary": self.psi_summary,
            "evidence_summary": self.evidence_summary,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ReplayBaseline:
        endpoint_count = data.get("endpoint_count")
        if endpoint_count is None and isinstance(data.get("endpoints"), list):
            endpoint_count = len(data["endpoints"])
        return cls(
            target_id=str(data.get("target_id", "pocketbase")),
            true_count=int(data.get("true_count", 0)),
            verified_count=int(data.get("verified_count", 0)),
            endpoint_count=int(endpoint_count or 0),
            xhr_count=int(data.get("xhr_count", 0)),
            dual_session_diffs=int(data.get("dual_session_diffs", 0)),
            mutation_count=int(data.get("mutation_count", 0)),
            phi_summary=dict(data.get("phi_summary") or {}),
            psi_summary=dict(data.get("psi_summary") or {}),
            evidence_summary=dict(data.get("evidence_summary") or {}),
        )


def load_baseline(path: str | Path) -> ReplayBaseline | None:
    p = Path(path)
    if not p.is_file():
        return None
    return ReplayBaseline.from_dict(json.loads(p.read_text(encoding="utf-8")))


def save_baseline(path: str | Path, baseline: ReplayBaseline) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(baseline.to_dict(), indent=2) + "\n", encoding="utf-8")
    return p


def build_baseline_from_dump(target_id: str, dump: dict[str, Any]) -> ReplayBaseline:
    verified = dump.get("verified_hotspots") or dump.get("top_10_hotspots") or []
    true_count = sum(1 for h in verified if str(h.get("verdict", "")).upper() == "TRUE")
    endpoints = dump.get("endpoint_count") or len({h.get("url") for h in verified if h.get("url")})
    accel = dump.get("acceleration") or {}
    dual = (accel.get("dual_session_idor") or {}).get("high_impact_count", 0)
    amp = dump.get("mutation_amplifier") or {}
    return ReplayBaseline(
        target_id=target_id,
        true_count=true_count,
        verified_count=len(verified),
        endpoint_count=int(endpoints),
        xhr_count=int(dump.get("xhr_count", 0)),
        dual_session_diffs=int(dual),
        mutation_count=int(amp.get("output_count", 0)),
        phi_summary={"passed": true_count, "total": len(verified)},
        psi_summary={"avg": dump.get("avg_psi", 0.0)},
        evidence_summary={"chains": len(verified)},
    )


def compare_regression(current: ReplayBaseline, baseline: ReplayBaseline) -> dict[str, Any]:
    endpoint_ratio = current.endpoint_count / max(baseline.endpoint_count, 1)
    passed = current.true_count >= baseline.true_count and endpoint_ratio >= 0.8
    return {
        "passed": passed,
        "true_delta": current.true_count - baseline.true_count,
        "endpoint_delta": current.endpoint_count - baseline.endpoint_count,
        "endpoint_ratio": round(endpoint_ratio, 3),
        "baseline": baseline.to_dict(),
        "current": current.to_dict(),
    }
