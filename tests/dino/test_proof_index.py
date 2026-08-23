"""Proof index manifest tests."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from dino.domains.proof.export import IndexMeta, export_proof_dir
from dino.domains.proof.index import INDEX_FILENAME, load_index, rebuild_index_from_archive
from tests.dino.conftest import FIXTURES, ROOT, run

WORK = Path(__file__).resolve().parent / "_export_work"
WORK.mkdir(parents=True, exist_ok=True)


def _seal(outdir: Path) -> dict:
    code, out, _ = run(
        [
            "proof",
            "run",
            "--output-dir",
            str(outdir),
            "--command",
            "echo",
            "idx_ok",
            "--scan",
            str(FIXTURES / "scan" / "clean_code.py"),
            "--repo",
            str(ROOT / "dino" / "common"),
        ]
    )
    assert code == 0
    return json.loads(out)


def test_export_writes_proof_index() -> None:
    src = WORK / "index_src"
    dest = WORK / "index_dest"
    if dest.exists():
        shutil.rmtree(dest)
    _seal(src)
    report = export_proof_dir(
        src,
        str(dest),
        meta=IndexMeta(pipeline="fraud_score_v4", group="risk", tags=("prod",)),
    )
    idx_path = dest / INDEX_FILENAME
    assert idx_path.is_file()
    assert report["index"]["proof_count"] == 1
    index = load_index(idx_path)
    assert index["schema"] == "dino.proof.index.v1"
    row = index["proofs"][0]
    assert row["pipeline"] == "fraud_score_v4"
    assert row["group"] == "risk"
    assert row["tags"] == ["prod"]
    assert row["leakage"] == "none"
    assert row["drift"] == "none"
    assert row["path"]


def test_export_index_upserts_by_hash() -> None:
    src = WORK / "index_src2"
    dest = WORK / "index_dest2"
    if dest.exists():
        shutil.rmtree(dest)
    _seal(src)
    export_proof_dir(src, str(dest))
    export_proof_dir(src, str(dest))
    index = load_index(dest / INDEX_FILENAME)
    assert len(index["proofs"]) == 1


def test_proof_index_cli_show_and_rebuild() -> None:
    archive = WORK / "index_cli"
    if archive.exists():
        shutil.rmtree(archive)
    src = WORK / "index_cli_src"
    _seal(src)
    export_proof_dir(src, str(archive), meta=IndexMeta(pipeline="p1"))
    code, out, _ = run(["proof", "index", "show", str(archive)])
    assert code == 0
    payload = json.loads(out)
    assert payload["schema"] == "dino.proof.index.v1"
    assert len(payload["proofs"]) == 1

    (archive / INDEX_FILENAME).unlink()
    code, out, _ = run(["proof", "index", "rebuild", str(archive)], json_mode=False)
    assert code == 0
    assert "Rebuilt" in out
    assert (archive / INDEX_FILENAME).is_file()
    rebuilt = rebuild_index_from_archive(archive)
    assert len(rebuilt["proofs"]) == 1


def test_http_export_includes_index_entry() -> None:
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from threading import Thread

    received: dict = {}

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:  # noqa: N802
            length = int(self.headers.get("Content-Length", "0"))
            received["body"] = json.loads(self.rfile.read(length).decode("utf-8"))
            self.send_response(201)
            self.end_headers()

        def log_message(self, *_args) -> None:
            return

    server = HTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        src = WORK / "index_http_src"
        _seal(src)
        export_proof_dir(
            src,
            f"http://127.0.0.1:{port}/api/proofs",
            meta=IndexMeta(pipeline="http_pipe"),
        )
        assert "index_entry" in received["body"]
        assert received["body"]["index_entry"]["pipeline"] == "http_pipe"
    finally:
        server.shutdown()
