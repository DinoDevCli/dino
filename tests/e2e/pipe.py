"""Minimal clean pipeline for E2E leakage scan (no findings)."""


def score(features: list[float]) -> float:
    return sum(features) / max(len(features), 1)
