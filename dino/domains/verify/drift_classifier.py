"""
Axiom 1 — semantic drift classes for decision trace (fixed vocabulary).
"""
from __future__ import annotations

from typing import Any, Literal

DriftClass = Literal[
    "aligned",
    "controlled_drift",
    "severe_drift",
    "synthetic_world",
    "unmeasured",
]

DRIFT_CLASS_DESCRIPTIONS: dict[str, str] = {
    "aligned": "World matches G_golden (distance 0)",
    "controlled_drift": "Permitted evolution within tau",
    "severe_drift": "Material edge-set change beyond tau",
    "synthetic_world": "Engine compile — no golden comparison",
    "unmeasured": "Insufficient graph — distance undefined",
}


def classify_drift(
    *,
    distance: int,
    tau: int = 5,
    graph_truth: str = "",
) -> DriftClass:
    if graph_truth == "engine_synthetic":
        return "synthetic_world"
    if graph_truth == "insufficient" or distance < 0:
        return "unmeasured"
    if distance == 0:
        return "aligned"
    if distance <= tau:
        return "controlled_drift"
    return "severe_drift"


def drift_class_payload(
    *,
    distance: int,
    tau: int = 5,
    graph_truth: str = "",
    taxonomy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    dc = classify_drift(distance=distance, tau=tau, graph_truth=graph_truth)
    payload: dict[str, Any] = {
        "drift_class": dc,
        "drift_class_description": DRIFT_CLASS_DESCRIPTIONS[dc],
        "distance": distance,
        "tau": tau,
        "structural_drift_class": (taxonomy or {}).get("structural_drift_class", "unmeasured"),
        "semantic_drift_class": (taxonomy or {}).get("semantic_drift_class", "unmeasured"),
        "topological_drift_class": (taxonomy or {}).get("topological_drift_class", "unmeasured"),
    }
    if taxonomy:
        payload["structural_drift"] = taxonomy.get("structural_drift")
        payload["semantic_drift"] = taxonomy.get("semantic_drift")
        payload["topological_drift"] = taxonomy.get("topological_drift")
        payload["graph_hash"] = taxonomy.get("graph_hash")
    return payload
