"""Proof export / upload tests."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread

from dino.domains.proof.export import build_export_envelope, export_proof_dir, parse_destination
from tests.dino.conftest import FIXTURES, ROOT, run

WORK = Path(__file__).resolve().parent / "_export_work"
WORK.mkdir(parents=True, exist_ok=True)


def _seal_proof(outdir: Path) -> dict:
    code, out, _ = run(
        [
            "proof",
            "run",
            "--output-dir",
            str(outdir),
            "--command",
            "echo",
            "export_ok",
            "--scan",
            str(FIXTURES / "scan" / "clean_code.py"),
            "--repo",
            str(ROOT / "dino" / "common"),
        ]
    )
    assert code == 0
    return json.loads(out)


def test_parse_destination_schemes() -> None:
    assert parse_destination("./out").scheme == "file"
    assert parse_destination("s3://bucket/team/proofs").netloc == "bucket"
    assert parse_destination("https://dash.example/api/proofs").scheme == "https"
    try:
        parse_destination("ftp://nope")
        assert False
    except ValueError:
        pass


def test_export_local_dir() -> None:
    outdir = WORK / "local_src"
    dest = WORK / "local_dest"
    if dest.exists():
        import shutil

        shutil.rmtree(dest)
    proof = _seal_proof(outdir)
    report = export_proof_dir(outdir, str(dest))
    assert report["ok"] is True
    assert report["scheme"] == "file"
    target = Path(report["destination"])
    assert (target / "proof.json").is_file()
    assert (target / "export.json").is_file()
    assert (target / "capsule" / "capsule.json").is_file()
    env = json.loads((target / "export.json").read_text(encoding="utf-8"))
    assert env["schema"] == "dino.proof.export.v1"
    assert env["proof_hash"] == proof["proof_hash"]
    assert (dest / "proof_index.json").is_file()


def test_export_via_proof_run_flag() -> None:
    outdir = WORK / "run_flag_src"
    dest = WORK / "run_flag_dest"
    code, out, _ = run(
        [
            "proof",
            "run",
            "--output-dir",
            str(outdir),
            "--command",
            "echo",
            "flag_export",
            "--scan",
            str(FIXTURES / "scan" / "clean_code.py"),
            "--export",
            str(dest),
        ]
    )
    assert code == 0
    payload = json.loads(out)
    assert payload["export"]["ok"] is True
    assert Path(payload["export"]["destination"]).is_dir()


def test_export_http_post() -> None:
    received: dict = {}

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:  # noqa: N802
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length)
            received["body"] = json.loads(body.decode("utf-8"))
            received["hash"] = self.headers.get("X-Dino-Proof-Hash")
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"accepted":true}')

        def log_message(self, *_args) -> None:
            return

    server = HTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        outdir = WORK / "http_src"
        _seal_proof(outdir)
        report = export_proof_dir(outdir, f"http://127.0.0.1:{port}/api/proofs")
        assert report["ok"] is True
        assert received["body"]["schema"] == "dino.proof.export.v1"
        assert received["hash"] == received["body"]["proof_hash"]
        assert "proof" in received["body"]
        assert "capsule/capsule.json" in received["body"]["artifacts"]
        assert "index_entry" in received["body"]
    finally:
        server.shutdown()


def test_proof_export_subcommand() -> None:
    outdir = WORK / "sub_src"
    dest = WORK / "sub_dest"
    _seal_proof(outdir)
    code, out, _ = run(
        ["proof", "export", "--proof-dir", str(outdir), "--to", str(dest)]
    )
    assert code == 0
    report = json.loads(out)
    assert report["ok"] is True
    assert (dest / "proof_index.json").is_file()
