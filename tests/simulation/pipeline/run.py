#!/usr/bin/env python3
"""Realistic multi-step fraud scoring pipeline for Dino production simulation.

Steps: extract → transform → model → report
Deterministic given seed/rows. Optional --fail / --hang for error-case tests.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from extract import generate_csv  # noqa: E402
from model import predict, train  # noqa: E402
from report import build_report, write_report  # noqa: E402
from transform import load_rows, transform, write_features  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dino simulation fraud pipeline")
    parser.add_argument("--workdir", type=Path, default=ROOT / "_work")
    parser.add_argument("--rows", type=int, default=500)
    parser.add_argument("--seed", default="dino-sim")
    parser.add_argument("--fail", action="store_true", help="Raise after extract")
    parser.add_argument("--hang", type=float, default=0.0, help="Sleep seconds before exit")
    parser.add_argument("--no-artifacts", action="store_true", help="Skip writing report")
    args = parser.parse_args(argv)

    work = args.workdir.resolve()
    work.mkdir(parents=True, exist_ok=True)
    raw = work / "raw.csv"
    feats = work / "features.csv"
    report_path = work / "report.json"

    print(f"[extract] rows={args.rows} seed={args.seed}", flush=True)
    generate_csv(raw, rows=args.rows, seed=args.seed)

    if args.fail:
        raise RuntimeError("simulated pipeline failure after extract")

    print("[transform] building features", flush=True)
    rows = load_rows(raw)
    features = transform(rows)
    write_features(features, feats)

    print("[model] training logistic regression", flush=True)
    model = train(features)
    scores = predict(model, features)

    if args.hang > 0:
        print(f"[hang] sleeping {args.hang}s", flush=True)
        time.sleep(args.hang)

    if args.no_artifacts:
        print("[report] skipped (--no-artifacts)", flush=True)
        return 0

    print("[report] writing report.json", flush=True)
    report = build_report(model=model, scores=scores, features=features)
    write_report(report, report_path)
    print(
        f"[done] accuracy={report['accuracy']} mean_score={report['score_mean']}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
