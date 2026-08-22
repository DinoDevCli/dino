"""Deterministic import graph for a source tree. Stdlib AST only."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from dino.common.determinism import canonical_hash


SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", "dist", "build"}


def _iter_py(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*.py")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    return files


def _module_name(root: Path, path: Path) -> str:
    rel = path.relative_to(root).with_suffix("")
    parts = list(rel.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts) or path.stem


def _imports(tree: ast.AST) -> list[str]:
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.append(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module.split(".")[0])
    return sorted(set(names))


def build_graph(root: Path) -> dict[str, Any]:
    root = root.resolve()
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, str]] = []
    local: dict[str, str] = {}
    for path in _iter_py(root):
        name = _module_name(root, path)
        local[name.split(".")[0]] = name
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError) as exc:
            nodes.append({"id": name, "path": str(path.relative_to(root)), "imports": [], "error": str(exc)})
            continue
        imported = _imports(tree)
        nodes.append({"id": name, "path": str(path.relative_to(root)), "imports": imported})
    node_ids = {n["id"] for n in nodes}
    prefixes = {n["id"].split(".")[0] for n in nodes}
    for node in nodes:
        for imp in node.get("imports") or []:
            if imp in prefixes or any(nid == imp or nid.startswith(imp + ".") for nid in node_ids):
                target = imp if imp in node_ids else next(
                    (nid for nid in sorted(node_ids) if nid == imp or nid.startswith(imp + ".")),
                    imp,
                )
                edges.append({"from": node["id"], "to": target})
    nodes.sort(key=lambda n: n["id"])
    edges.sort(key=lambda e: (e["from"], e["to"]))
    payload = {"nodes": nodes, "edges": edges}
    return {
        "schema": "dino.map.graph.v1",
        "root": str(root),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "graph_hash": canonical_hash(payload),
        **payload,
    }
