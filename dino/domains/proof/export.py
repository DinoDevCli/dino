"""Proof export / upload — local dir, HTTP POST, or S3 (no dashboard required)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .index import (
    INDEX_FILENAME,
    INDEX_SCHEMA,
    build_index_entry,
    empty_index,
    index_file_path,
    load_index,
    save_index,
    upsert_entry,
    utc_now_iso,
)

EXPORT_SCHEMA = "dino.proof.export.v1"


@dataclass(frozen=True)
class IndexMeta:
    pipeline: str = ""
    group: str = ""
    tags: tuple[str, ...] = ()

    @classmethod
    def from_namespace(cls, args) -> "IndexMeta":
        raw_tags = getattr(args, "tag", None) or []
        return cls(
            pipeline=str(getattr(args, "pipeline", "") or "").strip(),
            group=str(getattr(args, "group", "") or "").strip(),
            tags=tuple(str(t).strip() for t in raw_tags if str(t).strip()),
        )


@dataclass(frozen=True)
class Destination:
    scheme: str  # file | http | https | s3
    raw: str
    path: str  # local path, URL path, or s3 key prefix
    netloc: str = ""  # host or bucket


def parse_destination(raw: str) -> Destination:
    text = (raw or "").strip()
    if not text:
        raise ValueError("export destination must be non-empty")

    # Bare paths / relative dirs (no scheme)
    if "://" not in text:
        p = Path(text).expanduser()
        return Destination(scheme="file", raw=text, path=str(p))

    parsed = urlparse(text)
    scheme = (parsed.scheme or "").lower()
    if scheme in {"http", "https"}:
        if not parsed.netloc:
            raise ValueError(f"invalid HTTP export URL: {text}")
        return Destination(scheme=scheme, raw=text, path=parsed.path or "/", netloc=parsed.netloc)
    if scheme == "s3":
        bucket = parsed.netloc
        key = (parsed.path or "/").lstrip("/")
        if not bucket:
            raise ValueError(f"invalid S3 URI (need s3://bucket/prefix): {text}")
        return Destination(scheme="s3", raw=text.rstrip("/"), path=key, netloc=bucket)
    if scheme == "file":
        return Destination(scheme="file", raw=text, path=parsed.path or text)
    raise ValueError(
        f"unsupported export scheme {scheme!r}; use path, http(s)://…, or s3://bucket/prefix"
    )


def _load_proof(output_dir: Path) -> dict[str, Any]:
    path = output_dir / "proof.json"
    if not path.is_file():
        raise ValueError(f"proof.json missing under {output_dir}")
    return json.loads(path.read_text(encoding="utf-8"))


def collect_artifact_files(output_dir: Path, proof: dict[str, Any]) -> dict[str, Path]:
    """Map relative artifact paths → absolute files that exist."""
    files: dict[str, Path] = {"proof.json": output_dir / "proof.json"}
    artifacts = proof.get("artifacts") or {}
    for rel in artifacts.values():
        if not rel:
            continue
        p = output_dir / str(rel)
        if p.is_file():
            files[str(rel).replace("\\", "/")] = p
    # Always include capsule replay if present
    for extra in ("capsule/replay.json", "scan.json", "map_verify.json"):
        p = output_dir / extra
        if p.is_file() and extra not in files:
            files[extra] = p
    return files


def build_export_envelope(
    proof: dict[str, Any],
    files: dict[str, Path],
    *,
    index_entry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """JSON body dashboards can ingest in one POST."""
    artifacts: dict[str, Any] = {}
    for rel, path in sorted(files.items()):
        if rel == "proof.json":
            continue
        artifacts[rel] = json.loads(path.read_text(encoding="utf-8"))
    envelope: dict[str, Any] = {
        "schema": EXPORT_SCHEMA,
        "proof_hash": proof.get("proof_hash"),
        "proof": proof,
        "artifacts": artifacts,
    }
    if index_entry is not None:
        envelope["index_entry"] = index_entry
    return envelope


def _make_index_entry(
    proof: dict[str, Any],
    files: dict[str, Path],
    *,
    meta: IndexMeta,
    bundle_path: str,
) -> dict[str, Any]:
    return build_index_entry(
        proof,
        sorted(files.keys()),
        pipeline=meta.pipeline,
        group=meta.group,
        tags=list(meta.tags),
        path=bundle_path,
    )


def _update_file_index(archive_root: Path, entry: dict[str, Any]) -> dict[str, Any]:
    from .index import link_layout_entry

    idx_path = index_file_path(archive_root)
    index = load_index(idx_path)
    upsert_entry(index, entry)
    save_index(idx_path, index)
    layout = link_layout_entry(archive_root, entry)
    return {
        "ok": True,
        "index_path": str(idx_path),
        "proof_count": len(index.get("proofs") or []),
        "entry": entry,
        "layout": layout,
    }


def _target_subdir(dest_path: str, proof_hash: str) -> str:
    short = (proof_hash or "noproof")[:16]
    base = dest_path.rstrip("/")
    return f"{base}/{short}" if base else short


def _export_file(
    output_dir: Path,
    proof: dict[str, Any],
    files: dict[str, Path],
    dest: Destination,
    *,
    meta: IndexMeta,
) -> dict[str, Any]:
    proof_hash = str(proof.get("proof_hash") or "")
    bundle_rel = _target_subdir("", proof_hash).strip("/")
    target = Path(_target_subdir(dest.path, proof_hash)).expanduser().resolve()
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
    for rel, src in files.items():
        out = target / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, out)
    entry = _make_index_entry(proof, files, meta=meta, bundle_path=bundle_rel)
    envelope = build_export_envelope(proof, files, index_entry=entry)
    (target / "export.json").write_text(
        json.dumps(envelope, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    archive_root = Path(dest.path).expanduser().resolve()
    index_report = _update_file_index(archive_root, entry)
    return {
        "ok": True,
        "scheme": "file",
        "destination": str(target),
        "proof_hash": proof_hash,
        "files": sorted(files),
        "index": index_report,
    }


def _export_http(
    proof: dict[str, Any],
    files: dict[str, Path],
    dest: Destination,
    *,
    meta: IndexMeta,
) -> dict[str, Any]:
    proof_hash = str(proof.get("proof_hash") or "")
    entry = _make_index_entry(proof, files, meta=meta, bundle_path=proof_hash[:16])
    envelope = build_export_envelope(proof, files, index_entry=entry)
    body = json.dumps(envelope, separators=(",", ":"), sort_keys=True, ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "dino-cli/0.3",
        "X-Dino-Proof-Hash": proof_hash,
        "X-Dino-Export-Schema": EXPORT_SCHEMA,
        "X-Dino-Index-Schema": "dino.proof.index.v1",
    }
    token = os.environ.get("DINO_EXPORT_HTTP_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(dest.raw, data=body, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60.0) as resp:
            status = getattr(resp, "status", 200)
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise ValueError(f"HTTP export failed ({exc.code}): {detail or exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise ValueError(f"HTTP export failed: {exc.reason}") from exc
    return {
        "ok": True,
        "scheme": dest.scheme,
        "destination": dest.raw,
        "proof_hash": proof_hash,
        "http_status": status,
        "response_preview": raw[:200],
        "files": sorted(files),
        "index": {"ok": True, "entry": entry, "mode": "inline_envelope"},
    }


def _s3_index_key(prefix: str) -> str:
    base = prefix.rstrip("/")
    return f"{base}/{INDEX_FILENAME}" if base else INDEX_FILENAME


def _normalize_index_data(data: dict[str, Any]) -> dict[str, Any]:
    proofs = data.get("proofs") if isinstance(data.get("proofs"), list) else []
    return {
        "schema": INDEX_SCHEMA,
        "updated_at": str(data.get("updated_at") or utc_now_iso()),
        "proofs": [p for p in proofs if isinstance(p, dict)],
    }


def _merge_s3_index(client, bucket: str, prefix: str, entry: dict[str, Any]) -> dict[str, Any]:
    import tempfile

    idx_key = _s3_index_key(prefix)
    index = empty_index()
    try:
        obj = client.get_object(Bucket=bucket, Key=idx_key)
        raw = obj["Body"].read().decode("utf-8", errors="replace")
        index = _normalize_index_data(json.loads(raw))
    except Exception:
        pass
    upsert_entry(index, entry)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tmp:
        save_index(Path(tmp.name), index)
        tmp_path = tmp.name
    try:
        client.upload_file(tmp_path, bucket, idx_key)
    finally:
        Path(tmp_path).unlink(missing_ok=True)
    return {
        "ok": True,
        "index_path": f"s3://{bucket}/{idx_key}",
        "proof_count": len(index.get("proofs") or []),
        "entry": entry,
    }


def _export_s3(
    proof: dict[str, Any],
    files: dict[str, Path],
    dest: Destination,
    *,
    meta: IndexMeta,
) -> dict[str, Any]:
    proof_hash = str(proof.get("proof_hash") or "")
    prefix = _target_subdir(dest.path, proof_hash)
    uri_base = f"s3://{dest.netloc}/{prefix}".rstrip("/")
    bundle_rel = proof_hash[:16]
    entry = _make_index_entry(proof, files, meta=meta, bundle_path=bundle_rel)
    envelope = build_export_envelope(proof, files, index_entry=entry)

    try:
        import boto3  # type: ignore
    except ImportError:
        boto3 = None  # type: ignore

    uploaded: list[str] = []
    if boto3 is not None:
        client = boto3.client("s3")
        for rel, src in files.items():
            key = f"{prefix}/{rel}".lstrip("/")
            client.upload_file(str(src), dest.netloc, key)
            uploaded.append(f"s3://{dest.netloc}/{key}")
        import tempfile

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tmp:
            json.dump(envelope, tmp, indent=2, sort_keys=True, ensure_ascii=False)
            tmp_path = tmp.name
        try:
            key = f"{prefix}/export.json".lstrip("/")
            client.upload_file(tmp_path, dest.netloc, key)
            uploaded.append(f"s3://{dest.netloc}/{key}")
        finally:
            Path(tmp_path).unlink(missing_ok=True)
        index_report = _merge_s3_index(client, dest.netloc, dest.path, entry)
        return {
            "ok": True,
            "scheme": "s3",
            "destination": uri_base,
            "proof_hash": proof_hash,
            "backend": "boto3",
            "files": uploaded,
            "index": index_report,
        }

    aws = shutil.which("aws")
    if not aws:
        raise ValueError(
            "S3 export needs either the 'boto3' package or the AWS CLI (`aws`). "
            "pip install boto3  — or —  install awscli and configure credentials."
        )
    import tempfile

    archive_prefix = dest.path.rstrip("/")
    idx_uri = f"s3://{dest.netloc}/{_s3_index_key(archive_prefix)}"
    with tempfile.TemporaryDirectory(prefix="dino-export-") as tmp:
        stage = Path(tmp)
        bundle_stage = stage / bundle_rel
        bundle_stage.mkdir(parents=True, exist_ok=True)
        for rel, src in files.items():
            out = bundle_stage / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, out)
        (bundle_stage / "export.json").write_text(
            json.dumps(envelope, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        completed = subprocess.run(
            [aws, "s3", "sync", str(bundle_stage), uri_base],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            raise ValueError(
                f"aws s3 sync failed: {(completed.stderr or completed.stdout or '').strip()[:500]}"
            )
        local_index = stage / INDEX_FILENAME
        subprocess.run([aws, "s3", "cp", idx_uri, str(local_index)], capture_output=True, check=False)
        index = load_index(local_index) if local_index.is_file() else empty_index()
        upsert_entry(index, entry)
        save_index(local_index, index)
        up = subprocess.run([aws, "s3", "cp", str(local_index), idx_uri], capture_output=True, text=True)
        if up.returncode != 0:
            raise ValueError(f"aws s3 cp index failed: {(up.stderr or up.stdout or '').strip()[:500]}")
    return {
        "ok": True,
        "scheme": "s3",
        "destination": uri_base,
        "proof_hash": proof_hash,
        "backend": "aws-cli",
        "files": sorted(files) + ["export.json"],
        "index": {
            "ok": True,
            "index_path": idx_uri,
            "proof_count": len(index.get("proofs") or []),
            "entry": entry,
        },
    }


def export_proof_dir(
    output_dir: Path,
    destination: str,
    *,
    meta: IndexMeta | None = None,
) -> dict[str, Any]:
    """
    Upload / copy a sealed proof directory to ``destination``.

    Updates ``proof_index.json`` at the archive root (file/S3) or sends
    ``index_entry`` inline (HTTP).
    """
    meta = meta or IndexMeta()
    output_dir = Path(output_dir).resolve()
    proof = _load_proof(output_dir)
    files = collect_artifact_files(output_dir, proof)
    dest = parse_destination(destination)
    proof_hash = str(proof.get("proof_hash") or "")

    if dest.scheme == "file":
        result = _export_file(output_dir, proof, files, dest, meta=meta)
    elif dest.scheme in {"http", "https"}:
        result = _export_http(proof, files, dest, meta=meta)
    elif dest.scheme == "s3":
        result = _export_s3(proof, files, dest, meta=meta)
    else:
        raise ValueError(f"unsupported scheme: {dest.scheme}")

    result["schema"] = EXPORT_SCHEMA
    result["source_dir"] = str(output_dir)
    return result
