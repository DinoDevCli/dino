"""Transform raw CSV rows into feature vectors (stdlib only)."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


def load_rows(csv_path: Path) -> list[dict[str, Any]]:
    with csv_path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def transform(rows: list[dict[str, Any]]) -> list[dict[str, float]]:
    out: list[dict[str, float]] = []
    for row in rows:
        amount = float(row["amount"])
        age = float(row["age_days"])
        country = float(row["country_code"])
        prior = float(row["prior_flags"])
        label = float(row["label"])
        out.append(
            {
                "amount_norm": amount / 1000.0,
                "age_norm": age / 3650.0,
                "country_norm": country / 20.0,
                "prior_norm": prior / 5.0,
                "risk_proxy": (amount / 1000.0) * 0.4 + (prior / 5.0) * 0.6,
                "label": label,
            }
        )
    return out


def write_features(features: list[dict[str, float]], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not features:
        path.write_text("", encoding="utf-8")
        return path
    fields = list(features[0].keys())
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in features:
            writer.writerow({k: f"{v:.8f}" for k, v in row.items()})
    return path
