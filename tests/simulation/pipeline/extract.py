"""Generate a deterministic synthetic CSV for the risk scoring pipeline."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


def generate_csv(path: Path, *, rows: int = 500, seed: str = "dino-sim") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["txn_id", "amount", "age_days", "country_code", "prior_flags", "label"]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for i in range(rows):
            digest = hashlib.sha256(f"{seed}:{i}".encode()).hexdigest()
            amount = (int(digest[0:8], 16) % 100000) / 100.0
            age_days = int(digest[8:12], 16) % 3650
            country = int(digest[12:14], 16) % 20
            prior = int(digest[14:16], 16) % 5
            label = 1 if (amount > 700 and prior >= 2) or (age_days < 30 and prior >= 3) else 0
            writer.writerow(
                {
                    "txn_id": f"T{i:06d}",
                    "amount": f"{amount:.2f}",
                    "age_days": str(age_days),
                    "country_code": str(country),
                    "prior_flags": str(prior),
                    "label": str(label),
                }
            )
    return path
