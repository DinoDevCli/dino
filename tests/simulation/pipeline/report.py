"""Write a deterministic JSON report artifact."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_report(
    *,
    model: dict[str, Any],
    scores: list[float],
    features: list[dict[str, float]],
) -> dict[str, Any]:
    threshold = 0.5
    predicted = [1 if s >= threshold else 0 for s in scores]
    labels = [int(row["label"]) for row in features]
    tp = sum(1 for p, y in zip(predicted, labels) if p == 1 and y == 1)
    tn = sum(1 for p, y in zip(predicted, labels) if p == 0 and y == 0)
    fp = sum(1 for p, y in zip(predicted, labels) if p == 1 and y == 0)
    fn = sum(1 for p, y in zip(predicted, labels) if p == 0 and y == 1)
    total = max(len(labels), 1)
    return {
        "schema": "dino.sim.fraud_report.v1",
        "pipeline": "fraud_score_sim",
        "n_rows": len(features),
        "threshold": threshold,
        "accuracy": round((tp + tn) / total, 6),
        "confusion": {"tp": tp, "tn": tn, "fp": fp, "fn": fn},
        "model": model,
        "score_mean": round(sum(scores) / max(len(scores), 1), 8),
        "score_max": round(max(scores) if scores else 0.0, 8),
    }


def write_report(report: dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
