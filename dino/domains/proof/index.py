"""Proof index manifest — dino.proof.index.v1 (no dashboard, just JSON)."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

INDEX_SCHEMA = "dino.proof.index.v1"
INDEX_FILENAME = "proof_index.json"
COMPARE_SCHEMA = "dino.proof.index.compare.v1"
METRICS_SCHEMA = "dino.proof.index.metrics.v1"
LAYOUT_DIRS = frozenset({"pipelines", "groups", "tags"})
_SAFE_SEGMENT = re.compile(r"[^A-Za-z0-9._\-]+")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def empty_index() -> dict[str, Any]:
    return {"schema": INDEX_SCHEMA, "updated_at": utc_now_iso(), "proofs": []}


def load_index(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return empty_index()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return empty_index()
    if not isinstance(data, dict):
        return empty_index()
    proofs = data.get("proofs")
    if not isinstance(proofs, list):
        proofs = []
    return {
        "schema": INDEX_SCHEMA,
        "updated_at": str(data.get("updated_at") or utc_now_iso()),
        "proofs": [p for p in proofs if isinstance(p, dict)],
    }


def save_index(path: Path, index: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": INDEX_SCHEMA,
        "updated_at": utc_now_iso(),
        "proofs": sorted(
            list(index.get("proofs") or []),
            key=lambda p: (str(p.get("timestamp") or ""), str(p.get("hash") or "")),
            reverse=True,
        ),
    }
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


def _leakage_label(scan_ok: bool | None) -> str:
    if scan_ok is True:
        return "none"
    if scan_ok is False:
        return "failed"
    return "skipped"


def _drift_label(bucket: str | None) -> str:
    if not bucket or bucket == "aligned":
        return "none"
    return str(bucket)


def _default_pipeline(proof: dict[str, Any]) -> str:
    cmd = proof.get("command") or []
    if isinstance(cmd, list) and cmd:
        return " ".join(str(x) for x in cmd)
    return "unknown"


def build_index_entry(
    proof: dict[str, Any],
    artifact_names: list[str],
    *,
    pipeline: str = "",
    group: str = "",
    tags: list[str] | None = None,
    path: str = "",
    timestamp: str | None = None,
) -> dict[str, Any]:
    """One row for proof_index.json — dashboard/compliance friendly."""
    parts = proof.get("parts") or {}
    audit = proof.get("audit") or {}
    proof_hash = str(proof.get("proof_hash") or "")
    tags_norm = sorted({str(t).strip() for t in (tags or []) if str(t).strip()})
    entry: dict[str, Any] = {
        "hash": proof_hash,
        "timestamp": timestamp or utc_now_iso(),
        "pipeline": (pipeline or "").strip() or _default_pipeline(proof),
        "drift": _drift_label(parts.get("drift_bucket")),
        "leakage": _leakage_label(parts.get("scan_ok")),
        "supersede": False,
        "status": proof.get("status"),
        "verdict": audit.get("verdict"),
        "artifacts": sorted(artifact_names),
    }
    if group.strip():
        entry["group"] = group.strip()
    if tags_norm:
        entry["tags"] = tags_norm
    if path:
        entry["path"] = path
    return entry


def upsert_entry(index: dict[str, Any], entry: dict[str, Any]) -> dict[str, Any]:
    proofs = list(index.get("proofs") or [])
    key = str(entry.get("hash") or "")
    proofs = [p for p in proofs if str(p.get("hash") or "") != key]
    proofs.append(entry)
    index["proofs"] = proofs
    index["updated_at"] = utc_now_iso()
    return index


def rebuild_index_from_archive(archive_root: Path) -> dict[str, Any]:
    """Scan ``archive_root/<hash16>/proof.json`` and rebuild the manifest."""
    archive_root = archive_root.resolve()
    index = empty_index()
    if not archive_root.is_dir():
        return index

    entries: list[dict[str, Any]] = []
    for child in sorted(archive_root.iterdir()):
        if not child.is_dir() or child.name in LAYOUT_DIRS:
            continue
        proof_path = child / "proof.json"
        if not proof_path.is_file():
            continue
        proof = json.loads(proof_path.read_text(encoding="utf-8"))
        rel_artifacts = sorted(
            str(p.relative_to(child)).replace("\\", "/")
            for p in child.rglob("*.json")
            if p.name != "export.json"
        )
        # Prefer existing index_entry metadata from export.json when present
        pipeline = ""
        group = ""
        tags: list[str] = []
        export_path = child / "export.json"
        if export_path.is_file():
            try:
                env = json.loads(export_path.read_text(encoding="utf-8"))
                ie = env.get("index_entry") if isinstance(env, dict) else None
                if isinstance(ie, dict):
                    pipeline = str(ie.get("pipeline") or "")
                    group = str(ie.get("group") or "")
                    tags = list(ie.get("tags") or [])
            except (OSError, json.JSONDecodeError):
                pass
        entries.append(
            build_index_entry(
                proof,
                rel_artifacts,
                pipeline=pipeline,
                group=group,
                tags=tags,
                path=child.name,
                timestamp=utc_now_iso(),
            )
        )
    index["proofs"] = sorted(entries, key=lambda e: (e.get("timestamp"), e.get("hash")), reverse=True)
    index["updated_at"] = utc_now_iso()
    return index


def index_file_path(archive_root: Path) -> Path:
    return archive_root.resolve() / INDEX_FILENAME


def find_entry(index: dict[str, Any], ref: str) -> dict[str, Any] | None:
    """Resolve full hash, hash prefix, or path slug."""
    ref = (ref or "").strip()
    if not ref:
        return None
    proofs = list(index.get("proofs") or [])
    for p in proofs:
        if str(p.get("hash") or "") == ref:
            return p
    for p in proofs:
        h = str(p.get("hash") or "")
        if h.startswith(ref) or str(p.get("path") or "") == ref:
            return p
    matches = [p for p in proofs if str(p.get("hash") or "").startswith(ref)]
    if len(matches) == 1:
        return matches[0]
    return None


def compare_entries(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    """CLI compare contract — deltas only, no UI."""
    arts_a = set(a.get("artifacts") or [])
    arts_b = set(b.get("artifacts") or [])
    tags_a = set(a.get("tags") or [])
    tags_b = set(b.get("tags") or [])
    changed = (
        a.get("drift") != b.get("drift")
        or a.get("leakage") != b.get("leakage")
        or a.get("supersede") != b.get("supersede")
        or a.get("pipeline") != b.get("pipeline")
        or a.get("verdict") != b.get("verdict")
        or a.get("status") != b.get("status")
        or arts_a != arts_b
        or tags_a != tags_b
        or a.get("group") != b.get("group")
    )
    return {
        "schema": COMPARE_SCHEMA,
        "a": {"hash": a.get("hash"), "path": a.get("path"), "timestamp": a.get("timestamp")},
        "b": {"hash": b.get("hash"), "path": b.get("path"), "timestamp": b.get("timestamp")},
        "changed": changed,
        "drift_delta": {"from": a.get("drift"), "to": b.get("drift")},
        "leakage_delta": {"from": a.get("leakage"), "to": b.get("leakage")},
        "supersede_status": {"a": bool(a.get("supersede")), "b": bool(b.get("supersede"))},
        "artifacts_diff": {
            "only_a": sorted(arts_a - arts_b),
            "only_b": sorted(arts_b - arts_a),
            "shared": sorted(arts_a & arts_b),
        },
        "pipeline_version_diff": {"from": a.get("pipeline"), "to": b.get("pipeline")},
        "verdict_diff": {"from": a.get("verdict"), "to": b.get("verdict")},
        "status_diff": {"from": a.get("status"), "to": b.get("status")},
        "group_diff": {"from": a.get("group"), "to": b.get("group")},
        "tags_diff": {
            "only_a": sorted(tags_a - tags_b),
            "only_b": sorted(tags_b - tags_a),
            "shared": sorted(tags_a & tags_b),
        },
    }


def compare_refs(index: dict[str, Any], ref_a: str, ref_b: str) -> dict[str, Any]:
    a = find_entry(index, ref_a)
    b = find_entry(index, ref_b)
    if a is None:
        raise ValueError(f"proof not found in index: {ref_a}")
    if b is None:
        raise ValueError(f"proof not found in index: {ref_b}")
    return compare_entries(a, b)


def metrics_summary(index: dict[str, Any]) -> dict[str, Any]:
    """Aggregate health numbers for dashboards/alerts — JSON only."""
    proofs = list(index.get("proofs") or [])
    drift_counts: dict[str, int] = {}
    leakage_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    pipelines: set[str] = set()
    groups: set[str] = set()
    tags: set[str] = set()
    for p in proofs:
        drift = str(p.get("drift") or "none")
        leak = str(p.get("leakage") or "skipped")
        status = str(p.get("status") or "unknown")
        drift_counts[drift] = drift_counts.get(drift, 0) + 1
        leakage_counts[leak] = leakage_counts.get(leak, 0) + 1
        status_counts[status] = status_counts.get(status, 0) + 1
        if p.get("pipeline"):
            pipelines.add(str(p["pipeline"]))
        if p.get("group"):
            groups.add(str(p["group"]))
        for t in p.get("tags") or []:
            tags.add(str(t))

    passed = status_counts.get("passed", 0) + status_counts.get("partial", 0)
    failed = status_counts.get("failed", 0)
    return {
        "schema": METRICS_SCHEMA,
        "total": len(proofs),
        "passed": passed,
        "failed": failed,
        "partial": status_counts.get("partial", 0),
        "status": dict(sorted(status_counts.items())),
        "drift_none": drift_counts.get("none", 0),
        "drift_minor": drift_counts.get("controlled_drift", 0) + drift_counts.get("minor", 0),
        "drift_severe": drift_counts.get("severe_drift", 0) + drift_counts.get("severe", 0),
        "drift": dict(sorted(drift_counts.items())),
        "leakage_detected": leakage_counts.get("failed", 0),
        "leakage": dict(sorted(leakage_counts.items())),
        "pipelines": sorted(pipelines),
        "groups": sorted(groups),
        "tags": sorted(tags),
    }


def safe_segment(name: str) -> str:
    text = (name or "").strip()
    if not text:
        return "_"
    cleaned = _SAFE_SEGMENT.sub("_", text).strip("._")
    return cleaned[:80] or "_"


def _link_or_copy(src: Path, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_symlink():
        dest.unlink()
    elif dest.exists():
        if dest.is_file():
            dest.unlink()
        elif dest.is_dir() and (dest / ".dino_layout_ref").is_file():
            (dest / ".dino_layout_ref").unlink(missing_ok=True)
            try:
                dest.rmdir()
            except OSError:
                return "exists"
        else:
            return "exists"
    try:
        os.symlink(src, dest, target_is_directory=True)
        return "symlink"
    except OSError:
        try:
            dest.mkdir(parents=True, exist_ok=True)
            (dest / ".dino_layout_ref").write_text(str(src) + "\n", encoding="utf-8")
            return "ref"
        except OSError:
            return "failed"


def link_layout_entry(archive_root: Path, entry: dict[str, Any]) -> dict[str, Any]:
    """
    Maintain browse layout (symlinks when possible):

      <archive>/pipelines/<pipeline>/<hash16>/
      <archive>/groups/<group>/<hash16>/
      <archive>/tags/<tag>/<hash16>/
    """
    archive_root = archive_root.resolve()
    path_slug = str(entry.get("path") or (str(entry.get("hash") or "")[:16]))
    bundle = archive_root / path_slug
    if not bundle.is_dir():
        return {"ok": False, "reason": "bundle_missing", "path": path_slug}

    links: list[str] = []
    pipeline = str(entry.get("pipeline") or "").strip()
    if pipeline:
        dest = archive_root / "pipelines" / safe_segment(pipeline) / path_slug
        mode = _link_or_copy(bundle, dest)
        links.append(f"pipelines/{safe_segment(pipeline)}/{path_slug}:{mode}")

    group = str(entry.get("group") or "").strip()
    if group:
        dest = archive_root / "groups" / safe_segment(group) / path_slug
        mode = _link_or_copy(bundle, dest)
        links.append(f"groups/{safe_segment(group)}/{path_slug}:{mode}")

    for tag in entry.get("tags") or []:
        t = str(tag).strip()
        if not t:
            continue
        dest = archive_root / "tags" / safe_segment(t) / path_slug
        mode = _link_or_copy(bundle, dest)
        links.append(f"tags/{safe_segment(t)}/{path_slug}:{mode}")

    return {"ok": True, "path": path_slug, "links": links}


def refresh_layout(archive_root: Path, index: dict[str, Any] | None = None) -> dict[str, Any]:
    archive_root = archive_root.resolve()
    if index is None:
        index = load_index(index_file_path(archive_root))
    reports = [link_layout_entry(archive_root, e) for e in index.get("proofs") or []]
    return {
        "ok": True,
        "archive": str(archive_root),
        "linked": sum(1 for r in reports if r.get("ok")),
        "entries": reports,
    }
