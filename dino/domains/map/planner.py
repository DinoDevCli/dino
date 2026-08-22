"""Deterministic build planner: topological order of the import graph."""

from __future__ import annotations

from typing import Any


def _adj(graph: dict[str, Any]) -> tuple[dict[str, list[str]], dict[str, int]]:
    nodes = [n["id"] for n in graph.get("nodes") or []]
    indeg = {n: 0 for n in nodes}
    adj: dict[str, list[str]] = {n: [] for n in nodes}
    for edge in graph.get("edges") or []:
        src, dst = edge["from"], edge["to"]
        if src not in adj or dst not in indeg:
            continue
        adj[src].append(dst)
        indeg[dst] += 1
    for k in adj:
        adj[k] = sorted(set(adj[k]))
    return adj, indeg


def cycles(graph: dict[str, Any]) -> list[list[str]]:
    adj, _ = _adj(graph)
    seen: set[str] = set()
    stack: set[str] = set()
    found: list[list[str]] = []

    def dfs(node: str, path: list[str]) -> None:
        if node in stack:
            cyc = path[path.index(node) :] + [node]
            found.append(cyc)
            return
        if node in seen:
            return
        seen.add(node)
        stack.add(node)
        for nxt in adj.get(node, []):
            dfs(nxt, path + [nxt])
        stack.remove(node)

    for n in sorted(adj):
        dfs(n, [n])
    # unique by frozenset
    uniq: list[list[str]] = []
    keys: set[tuple[str, ...]] = set()
    for c in found:
        key = tuple(sorted(set(c)))
        if key not in keys:
            keys.add(key)
            uniq.append(c)
    return uniq


def plan(graph: dict[str, Any]) -> dict[str, Any]:
    adj, indeg = _adj(graph)
    ready = sorted(n for n, d in indeg.items() if d == 0)
    order: list[str] = []
    remaining = dict(indeg)
    while ready:
        node = ready.pop(0)
        order.append(node)
        for nxt in adj.get(node, []):
            remaining[nxt] -= 1
            if remaining[nxt] == 0:
                ready.append(nxt)
                ready.sort()
    cyc = cycles(graph) if len(order) < len(remaining) else []
    return {
        "schema": "dino.map.plan.v1",
        "steps": order,
        "blocked_cycles": cyc,
        "complete": len(order) == len(remaining),
    }
