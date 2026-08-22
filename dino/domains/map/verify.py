"""Deterministic quality scores from graph structure only. No runtime telemetry."""

from __future__ import annotations

from typing import Any

from .drift import compare
from .graph import build_graph
from .planner import cycles, plan


def _safe_div(num: float, den: float) -> float:
    if den <= 0:
        return 0.0
    return num / den


def score_graph(graph: dict[str, Any], *, baseline: dict[str, Any] | None = None) -> dict[str, Any]:
    node_count = int(graph.get("node_count") or 0)
    edge_count = int(graph.get("edge_count") or 0)
    cyc = cycles(graph)
    planned = plan(graph)
    fanout = 0
    for node in graph.get("nodes") or []:
        fanout = max(fanout, len(node.get("imports") or []))
    cycle_penalty = min(1.0, len(cyc) * 0.25)
    completeness = 1.0 if planned["complete"] else 0.5
    size_score = min(1.0, _safe_div(node_count, 50.0))
    connectivity = min(1.0, _safe_div(edge_count, max(1, node_count)))
    determinism = 1.0  # structural hash is the contract
    drift_report = None
    drift_score = 1.0
    if baseline is not None:
        drift_report = compare(graph, baseline)
        drift_score = 1.0 if drift_report["distance"] == 0 else max(0.0, 1.0 - drift_report["distance"] / 20.0)
    overall = round(
        0.40 * determinism
        + 0.20 * drift_score
        + 0.15 * completeness
        + 0.10 * (1.0 - cycle_penalty)
        + 0.10 * connectivity
        + 0.05 * size_score,
        6,
    )
    bucket = "stable"
    if cycle_penalty > 0 or not planned["complete"]:
        bucket = "watch"
    if drift_report and drift_report["bucket"] == "severe_drift":
        bucket = "critical"
    return {
        "schema": "dino.map.verify.v1",
        "overall_quality_score": overall,
        "drift_bucket": bucket,
        "score_inputs": {
            "determinism": determinism,
            "drift": round(drift_score, 6),
            "completeness": completeness,
            "cycle_penalty": cycle_penalty,
            "connectivity": round(connectivity, 6),
            "size": round(size_score, 6),
        },
        "node_count": node_count,
        "edge_count": edge_count,
        "cycles": cyc,
        "plan_complete": planned["complete"],
        "graph_hash": graph.get("graph_hash"),
        "max_fanout": fanout,
        "drift": drift_report,
        "kernel_contract_details": {"skipped": False, "reason": "embedded"},
    }


def verify_repo(root: str, *, baseline: dict[str, Any] | None = None) -> dict[str, Any]:
    from pathlib import Path

    graph = build_graph(Path(root))
    planned = plan(graph)
    report = score_graph(graph, baseline=baseline)
    report["plan"] = {"steps": planned["steps"], "complete": planned["complete"]}
    return report
