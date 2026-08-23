"""Tiny deterministic logistic regression (no sklearn)."""

from __future__ import annotations

import math
from typing import Any


FEATURE_KEYS = ("amount_norm", "age_norm", "country_norm", "prior_norm", "risk_proxy")


def _sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def train(features: list[dict[str, float]], *, epochs: int = 40, lr: float = 0.5) -> dict[str, Any]:
    weights = [0.0] * len(FEATURE_KEYS)
    bias = 0.0
    n = max(len(features), 1)
    for _ in range(epochs):
        grad_w = [0.0] * len(FEATURE_KEYS)
        grad_b = 0.0
        for row in features:
            x = [row[k] for k in FEATURE_KEYS]
            z = bias + sum(w * xi for w, xi in zip(weights, x))
            pred = _sigmoid(z)
            err = pred - row["label"]
            for i, xi in enumerate(x):
                grad_w[i] += err * xi
            grad_b += err
        for i in range(len(weights)):
            weights[i] -= lr * (grad_w[i] / n)
        bias -= lr * (grad_b / n)
    return {
        "weights": [round(w, 8) for w in weights],
        "bias": round(bias, 8),
        "feature_keys": list(FEATURE_KEYS),
        "epochs": epochs,
        "n_samples": len(features),
    }


def predict(model: dict[str, Any], features: list[dict[str, float]]) -> list[float]:
    weights = model["weights"]
    bias = float(model["bias"])
    keys = model["feature_keys"]
    scores: list[float] = []
    for row in features:
        x = [row[k] for k in keys]
        z = bias + sum(w * xi for w, xi in zip(weights, x))
        scores.append(round(_sigmoid(z), 8))
    return scores
