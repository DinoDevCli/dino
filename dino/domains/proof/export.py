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

EXPORT_SCHEMA = "dino.proof.export.v1"


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


def build_export_envelope(proof: dict[str, Any], files: dict[str, Path]) -> dict[str, Any]:
    """JSON body dashboards can ingest in one POST."""
    artifacts: dict[str, Any] = {}
    for rel, path in sorted(files.items()):
        if rel == "proof.json":
            continue
        artifacts[rel] = json.loads(path.read_text(encoding="utf-8"))
    return {
        "schema": EXPORT_SCHEMA,
        "proof_hash": proof.get("proof_hash"),
        "proof": proof,
        "artifacts": artifacts,
    }


def _target_subdir(dest_path: str, proof_hash: str) -> str:
    short = (proof_hash or "noproof")[:16]
    base = dest_path.rstrip("/")
    return f"{base}/{short}" if base else short


def _export_file(output_dir: Path, proof: dict[str, Any], files: dict[str, Path], dest: Destination) -> dict[str, Any]:
    proof_hash = str(proof.get("proof_hash") or "")
    target = Path(_target_subdir(dest.path, proof_hash)).expanduser().resolve()
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
    for rel, src in files.items():
        out = target / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, out)
    envelope = build_export_envelope(proof, files)
    (target / "export.json").write_text(
        json.dumps(envelope, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return {
        "ok": True,
        "scheme": "file",
        "destination": str(target),
        "proof_hash": proof_hash,
        "files": sorted(files),
    }


def _export_http(proof: dict[str, Any], files: dict[str, Path], dest: Destination) -> dict[str, Any]:
    envelope = build_export_envelope(proof, files)
    body = json.dumps(envelope, separators=(",", ":"), sort_keys=True, ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "dino-cli/0.3",
        "X-Dino-Proof-Hash": str(proof.get("proof_hash") or ""),
        "X-Dino-Export-Schema": EXPORT_SCHEMA,
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
        "proof_hash": proof.get("proof_hash"),
        "http_status": status,
        "response_preview": raw[:200],
        "files": sorted(files),
    }


def _export_s3(files: dict[str, Path], dest: Destination, proof_hash: str) -> dict[str, Any]:
    prefix = _target_subdir(dest.path, proof_hash)
    uri_base = f"s3://{dest.netloc}/{prefix}".rstrip("/")

    # Prefer boto3 when installed; else AWS CLI.
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
        # export envelope
        envelope = build_export_envelope(
            json.loads(files["proof.json"].read_text(encoding="utf-8")),
            files,
        )
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
        return {
            "ok": True,
            "scheme": "s3",
            "destination": uri_base,
            "proof_hash": proof_hash,
            "backend": "boto3",
            "files": uploaded,
        }

    aws = shutil.which("aws")
    if not aws:
        raise ValueError(
            "S3 export needs either the 'boto3' package or the AWS CLI (`aws`). "
            "pip install boto3  — or —  install awscli and configure credentials."
        )
    # Stage to temp dir then sync
    import tempfile

    with tempfile.TemporaryDirectory(prefix="dino-export-") as tmp:
        stage = Path(tmp)
        for rel, src in files.items():
            out = stage / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, out)
        proof = json.loads(files["proof.json"].read_text(encoding="utf-8"))
        (stage / "export.json").write_text(
            json.dumps(build_export_envelope(proof, files), indent=2, sort_keys=True, ensure_ascii=False)
            + "\n",
            encoding="utf-8",
        )
        completed = subprocess.run(
            [aws, "s3", "sync", str(stage), uri_base],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            raise ValueError(
                f"aws s3 sync failed: {(completed.stderr or completed.stdout or '').strip()[:500]}"
            )
    return {
        "ok": True,
        "scheme": "s3",
        "destination": uri_base,
        "proof_hash": proof_hash,
        "backend": "aws-cli",
        "files": sorted(files) + ["export.json"],
    }


def export_proof_dir(output_dir: Path, destination: str) -> dict[str, Any]:
    """
    Upload / copy a sealed proof directory to ``destination``.

    Destinations:
      - local path: ``./proofs_out`` → ``./proofs_out/<proof_hash16>/``
      - HTTP(S): POST ``dino.proof.export.v1`` JSON envelope
      - S3: ``s3://bucket/prefix`` → ``s3://bucket/prefix/<proof_hash16>/``
    """
    output_dir = Path(output_dir).resolve()
    proof = _load_proof(output_dir)
    files = collect_artifact_files(output_dir, proof)
    dest = parse_destination(destination)
    proof_hash = str(proof.get("proof_hash") or "")

    if dest.scheme == "file":
        result = _export_file(output_dir, proof, files, dest)
    elif dest.scheme in {"http", "https"}:
        result = _export_http(proof, files, dest)
    elif dest.scheme == "s3":
        result = _export_s3(files, dest, proof_hash)
    else:
        raise ValueError(f"unsupported scheme: {dest.scheme}")

    result["schema"] = EXPORT_SCHEMA
    result["source_dir"] = str(output_dir)
    return result
