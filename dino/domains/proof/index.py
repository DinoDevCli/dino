"""Proof index manifest — dino.proof.index.v1 (no dashboard, just JSON)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

INDEX_SCHEMA = "dino.proof.index.v1"
INDEX_FILENAME = "proof_index.json"


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
        if not child.is_dir():
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
        entries.append(
            build_index_entry(
                proof,
                rel_artifacts,
                path=child.name,
                timestamp=utc_now_iso(),
            )
        )
    index["proofs"] = sorted(entries, key=lambda e: (e.get("timestamp"), e.get("hash")), reverse=True)
    index["updated_at"] = utc_now_iso()
    return index


def index_file_path(archive_root: Path) -> Path:
    return archive_root.resolve() / INDEX_FILENAME
