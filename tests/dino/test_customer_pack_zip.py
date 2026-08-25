"""Customer-pack.v1 ZIP: required files, schemas, placeholders filled."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "issue-early-access.sh"
PACK_SRC = ROOT / "docs" / "internal" / "customer_pack"

REQUIRED = (
    "KEY.txt",
    "QUICKSTART.md",
    "EMAIL.txt",
    "LICENSE",
    "VERSION",
    "examples/proof_index.json",
    "examples/compare.json",
)


def test_example_hashes_are_documented() -> None:
    v1 = hashlib.sha256(b"dino-example-fraud_score_v1").hexdigest()
    v2 = hashlib.sha256(b"dino-example-fraud_score_v2").hexdigest()
    index = json.loads((PACK_SRC / "examples" / "proof_index.json").read_text(encoding="utf-8"))
    hashes = {row["hash"] for row in index["proofs"]}
    assert hashes == {v1, v2}
    compare = json.loads((PACK_SRC / "examples" / "compare.json").read_text(encoding="utf-8"))
    assert compare["changed"] is True
    assert compare["pipeline_version_diff"] == {
        "from": "fraud_score_v1",
        "to": "fraud_score_v2",
    }
    assert compare["schema"] == "dino.proof.index.compare.v1"
    assert index["schema"] == "dino.proof.index.v1"


def test_issue_script_writes_customer_pack_zip(tmp_path: Path) -> None:
    env = os.environ.copy()
    env.pop("DINO_EA_SIGNING_SECRET", None)
    proc = subprocess.run(
        [str(SCRIPT), "ACME Risk", "60", "--allow-sim", "--out", str(tmp_path), "--name", "Alex"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    zips = list(tmp_path.glob("dino-ea-acme-risk-v*.zip"))
    assert len(zips) == 1
    zip_path = zips[0]
    assert "acme-risk" in zip_path.name

    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
        for rel in REQUIRED:
            assert f"acme-risk/{rel}" in names, rel
        key = zf.read("acme-risk/KEY.txt").decode("utf-8").strip()
        email = zf.read("acme-risk/EMAIL.txt").decode("utf-8")
        quick = zf.read("acme-risk/QUICKSTART.md").decode("utf-8")
        version = zf.read("acme-risk/VERSION").decode("utf-8").strip()
        license_text = zf.read("acme-risk/LICENSE").decode("utf-8")
        index = json.loads(zf.read("acme-risk/examples/proof_index.json"))
        compare = json.loads(zf.read("acme-risk/examples/compare.json"))

    assert key.startswith("dinoea.v1.")
    assert "{" not in email
    assert "{" not in quick
    assert "Alex" in email
    assert key in email
    assert key in quick
    assert "acme-risk" in email
    assert version == "1.0.0"
    assert "MIT License" in license_text
    assert index["schema"] == "dino.proof.index.v1"
    assert compare["changed"] is True
    assert "Attach:" in proc.stdout
    assert str(zip_path) in proc.stdout


def test_issue_script_refuses_sim_secret_by_default(tmp_path: Path) -> None:
    env = os.environ.copy()
    env.pop("DINO_EA_SIGNING_SECRET", None)
    proc = subprocess.run(
        [str(SCRIPT), "acme-risk", "60", "--out", str(tmp_path)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    assert "DINO_EA_SIGNING_SECRET" in proc.stderr
    assert list(tmp_path.glob("*.zip")) == []
