"""Full E2E: proof run → export → index → metrics → compare → layout → rebuild."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from dino.license import DEFAULT_LICENSE, activate_pack, save_license
from dino.packs import PACKS
from tests.dino.conftest import run

E2E = Path(__file__).resolve().parent
PIPE = E2E / "pipe.py"
PROOF_OUT = E2E / "proof_out"
ARCHIVE = E2E / "archive"


@pytest.fixture(autouse=True)
def _unlock_and_clean(tmp_path, monkeypatch):
    lic_dir = tmp_path / ".dino"
    lic_dir.mkdir(exist_ok=True)
    monkeypatch.setattr("dino.license.LICENSE_DIR", lic_dir)
    monkeypatch.setattr("dino.license.LICENSE_PATH", lic_dir / "license.json")
    monkeypatch.setenv("DINO_OFFLINE_LICENSE_KEYS", "e2e-key")
    save_license(dict(DEFAULT_LICENSE))
    for pack in PACKS:
        activate_pack(pack, key="e2e-key")
    for path in (PROOF_OUT, ARCHIVE):
        if path.exists():
            shutil.rmtree(path)
    yield


def _extract_hash(payload: dict) -> str:
    h = payload.get("proof_hash") or (payload.get("export") or {}).get("proof_hash")
    assert h and isinstance(h, str) and len(h) >= 16
    return h


def _layout_target(archive: Path, kind: str, name: str, hash16: str) -> Path:
    return archive / kind / name / hash16


def test_full_e2e_proof_export_index() -> None:
    assert PIPE.is_file()

    code, out, err = run(
        [
            "proof",
            "run",
            "--command",
            "echo ok",
            "--scan",
            str(PIPE),
            "--output-dir",
            str(PROOF_OUT),
            "--pipeline",
            "fraud_score_v4",
            "--group",
            "risk-team",
            "--tag",
            "prod",
            "--tag",
            "v4",
            "--export",
            str(ARCHIVE),
        ]
    )
    assert code == 0, f"proof run failed: {err}\n{out}"
    payload = json.loads(out)
    assert payload.get("ok") is True
    proof_hash = _extract_hash(payload)
    hash16 = proof_hash[:16]

    # Local seal artifacts
    assert (PROOF_OUT / "proof.json").is_file()
    assert (PROOF_OUT / "scan.json").is_file()

    # Exported bundle
    bundle = ARCHIVE / hash16
    assert (bundle / "proof.json").is_file()
    assert (bundle / "scan.json").is_file()
    assert (bundle / "export.json").is_file()
    assert (ARCHIVE / "proof_index.json").is_file()

    export_body = json.loads((bundle / "export.json").read_text(encoding="utf-8"))
    assert export_body["schema"] == "dino.proof.export.v1"
    assert export_body["proof_hash"] == proof_hash
    assert "index_entry" in export_body
    assert export_body["index_entry"]["pipeline"] == "fraud_score_v4"

    # Browse layout (symlink or .dino_layout_ref)
    for kind, name in (
        ("pipelines", "fraud_score_v4"),
        ("groups", "risk-team"),
        ("tags", "prod"),
        ("tags", "v4"),
    ):
        target = _layout_target(ARCHIVE, kind, name, hash16)
        assert target.exists() or target.is_symlink(), f"missing layout: {target}"
        if target.is_dir() and not target.is_symlink():
            assert (target / ".dino_layout_ref").is_file() or (target / "proof.json").is_file()

    # index show
    code, out, _ = run(["proof", "index", "show", str(ARCHIVE)])
    assert code == 0
    index = json.loads(out)
    assert index["schema"] == "dino.proof.index.v1"
    assert len(index["proofs"]) == 1
    assert index["proofs"][0]["hash"] == proof_hash

    # metrics
    code, out, _ = run(["proof", "index", "metrics", str(ARCHIVE)])
    assert code == 0
    metrics = json.loads(out)
    assert metrics["schema"] == "dino.proof.index.metrics.v1"
    for key in (
        "total",
        "passed",
        "failed",
        "drift_none",
        "drift_minor",
        "drift_severe",
        "leakage_detected",
        "pipelines",
    ):
        assert key in metrics
    assert metrics["total"] == 1
    assert metrics["passed"] == 1
    assert metrics["failed"] == 0
    assert "fraud_score_v4" in metrics["pipelines"]

    # compare identical → exit 0
    code, out, _ = run(
        ["proof", "index", "compare", str(ARCHIVE), proof_hash, hash16]
    )
    assert code == 0, out
    cmp = json.loads(out)
    assert cmp["schema"] == "dino.proof.index.compare.v1"
    assert cmp["changed"] is False

    # layout refresh
    code, out, _ = run(["proof", "index", "layout", str(ARCHIVE)])
    assert code == 0
    layout = json.loads(out)
    assert layout.get("ok") is True
    assert layout.get("linked", 0) >= 1

    # rebuild
    code, out, _ = run(["proof", "index", "rebuild", str(ARCHIVE)])
    assert code == 0
    rebuilt = json.loads(out)
    assert rebuilt.get("ok") is True
    assert rebuilt.get("proof_count") == 1
    assert (ARCHIVE / "proof_index.json").is_file()
