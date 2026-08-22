"""Structural drift between two graph snapshots. No wall-clock."""

from __future__ import annotations

from typing import Any


def _ids(graph: dict[str, Any]) -> set[str]:
    return {n["id"] for n in graph.get("nodes") or []}


def _edge_keys(graph: dict[str, Any]) -> set[tuple[str, str]]:
    return {(e["from"], e["to"]) for e in graph.get("edges") or []}


def classify(distance: int, *, tau: int = 5) -> str:
    if distance < 0:
        return "unmeasured"
    if distance == 0:
        return "aligned"
    if distance <= tau:
        return "controlled_drift"
    return "severe_drift"


def compare(current: dict[str, Any], baseline: dict[str, Any], *, tau: int = 5) -> dict[str, Any]:
    n_cur, n_base = _ids(current), _ids(baseline)
    e_cur, e_base = _edge_keys(current), _edge_keys(baseline)
    added_nodes = sorted(n_cur - n_base)
    removed_nodes = sorted(n_base - n_cur)
    added_edges = sorted(f"{a}->{b}" for a, b in sorted(e_cur - e_base))
    removed_edges = sorted(f"{a}->{b}" for a, b in sorted(e_base - e_cur))
    distance = len(added_nodes) + len(removed_nodes) + len(added_edges) + len(removed_edges)
    return {
        "schema": "dino.map.drift.v1",
        "distance": distance,
        "tau": tau,
        "bucket": classify(distance, tau=tau),
        "added_nodes": added_nodes,
        "removed_nodes": removed_nodes,
        "added_edges": added_edges,
        "removed_edges": removed_edges,
        "current_hash": current.get("graph_hash"),
        "baseline_hash": baseline.get("graph_hash"),
    }
