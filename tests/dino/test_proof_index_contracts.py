"""Proof index compare / metrics / layout contracts."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from dino.domains.proof.export import IndexMeta, export_proof_dir
from dino.domains.proof.index import (
    compare_entries,
    load_index,
    metrics_summary,
    refresh_layout,
)
from tests.dino.conftest import FIXTURES, ROOT, run

WORK = Path(__file__).resolve().parent / "_export_work"
WORK.mkdir(parents=True, exist_ok=True)


def _seal(outdir: Path, label: str) -> dict:
    code, out, _ = run(
        [
            "proof",
            "run",
            "--output-dir",
            str(outdir),
            "--command",
            "echo",
            label,
            "--scan",
            str(FIXTURES / "scan" / "clean_code.py"),
            "--repo",
            str(ROOT / "dino" / "common"),
        ]
    )
    assert code == 0
    return json.loads(out)


def test_compare_and_metrics_and_layout() -> None:
    archive = WORK / "cml_archive"
    if archive.exists():
        shutil.rmtree(archive)

    a_src = WORK / "cml_a"
    b_src = WORK / "cml_b"
    pa = _seal(a_src, "cmp_a")
    pb = _seal(b_src, "cmp_b")
    export_proof_dir(
        a_src,
        str(archive),
        meta=IndexMeta(pipeline="fraud_score_v4", group="risk", tags=("prod",)),
    )
    export_proof_dir(
        b_src,
        str(archive),
        meta=IndexMeta(pipeline="fraud_score_v5", group="risk", tags=("prod", "canary")),
    )

    # Layout
    assert (archive / "pipelines" / "fraud_score_v4").is_dir()
    assert (archive / "groups" / "risk").is_dir()
    assert (archive / "tags" / "prod").is_dir()

    ha = pa["proof_hash"]
    hb = pb["proof_hash"]
    code, out, _ = run(["proof", "index", "compare", str(archive), ha[:12], hb[:12]])
    # changed → exit 1
    assert code == 1
    cmp = json.loads(out)
    assert cmp["schema"] == "dino.proof.index.compare.v1"
    assert cmp["changed"] is True
    assert cmp["pipeline_version_diff"]["from"] == "fraud_score_v4"
    assert cmp["pipeline_version_diff"]["to"] == "fraud_score_v5"
    assert "canary" in cmp["tags_diff"]["only_b"]

    code, out, _ = run(["proof", "index", "metrics", str(archive)])
    assert code == 0
    metrics = json.loads(out)
    assert metrics["schema"] == "dino.proof.index.metrics.v1"
    assert metrics["total"] == 2
    assert metrics["passed"] == 2
    assert "fraud_score_v4" in metrics["pipelines"]
    assert metrics["leakage_detected"] == 0

    code, out, _ = run(["proof", "index", "layout", str(archive)], json_mode=False)
    assert code == 0
    assert "Layout refreshed" in out

    # Unit: identical entries → unchanged
    index = load_index(archive / "proof_index.json")
    e0 = index["proofs"][0]
    same = compare_entries(e0, e0)
    assert same["changed"] is False
    m = metrics_summary(index)
    assert m["total"] == 2
    layout = refresh_layout(archive, index)
    assert layout["linked"] >= 1
