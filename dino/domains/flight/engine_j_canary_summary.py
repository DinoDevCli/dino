from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CanaryRecord:
    path: Path
    timestamp: str
    strict_mode: bool
    run_count: int
    flakiness_score: float
    payload_equal_first_second: bool
    hash_equal_first_second: bool
    runtime_delta_ratio_first_second: float
    mismatch_indices_vs_first: list[int]
    snapshots: list[dict[str, Any]]


def _load_record(path: Path) -> CanaryRecord:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return CanaryRecord(
        path=path,
        timestamp=str(raw.get("timestamp", "")),
        strict_mode=bool(raw.get("strict_mode", False)),
        run_count=int(raw.get("run_count", 0)),
        flakiness_score=float(raw.get("flakiness_score", 0.0)),
        payload_equal_first_second=bool(raw.get("payload_equal_first_second", False)),
        hash_equal_first_second=bool(raw.get("hash_equal_first_second", False)),
        runtime_delta_ratio_first_second=float(raw.get("runtime_delta_ratio_first_second", 0.0)),
        mismatch_indices_vs_first=list(raw.get("mismatch_indices_vs_first", [])),
        snapshots=list(raw.get("snapshots", [])),
    )


def _payload_map(snapshot: dict[str, Any]) -> dict[str, str]:
    payload = snapshot.get("payload", [])
    mapped: dict[str, str] = {}
    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, list) and len(item) == 2:
                mapped[str(item[0])] = str(item[1])
    return mapped


def _stable_tail_length(scores: list[float], threshold: float = 1.0) -> int:
    count = 0
    for score in reversed(scores):
        if score >= threshold:
            count += 1
        else:
            break
    return count


def build_summary(records: list[CanaryRecord]) -> dict[str, Any]:
    if not records:
        return {"error": "No canary records found."}

    by_time = sorted(records, key=lambda r: (r.timestamp, r.path.name))
    scores = [r.flakiness_score for r in by_time]
    avg_score = sum(scores) / len(scores)

    worst = min(by_time, key=lambda r: r.flakiness_score)
    best = max(by_time, key=lambda r: r.flakiness_score)

    runtime_drifts = [r.runtime_delta_ratio_first_second for r in by_time]

    unstable_fields: Counter[str] = Counter()
    hash_change_count = 0
    for rec in by_time:
        snaps = rec.snapshots
        if len(snaps) < 2:
            continue
        base_payload = _payload_map(snaps[0])
        for snap in snaps[1:]:
            if snap.get("deterministic_hash") != snaps[0].get("deterministic_hash"):
                hash_change_count += 1
            current_payload = _payload_map(snap)
            keys = set(base_payload) | set(current_payload)
            for key in keys:
                if base_payload.get(key) != current_payload.get(key):
                    unstable_fields[key] += 1

    trend = []
    for rec in by_time:
        trend.append(
            {
                "timestamp": rec.timestamp,
                "file": rec.path.name,
                "flakiness_score": rec.flakiness_score,
                "run_count": rec.run_count,
                "runtime_delta_ratio_first_second": rec.runtime_delta_ratio_first_second,
                "strict_mode": rec.strict_mode,
            }
        )

    return {
        "records": len(by_time),
        "avg_flakiness_score": round(avg_score, 6),
        "best_flakiness_score": best.flakiness_score,
        "best_record": best.path.name,
        "worst_flakiness_score": worst.flakiness_score,
        "worst_record": worst.path.name,
        "stable_since_runs": _stable_tail_length(scores, threshold=1.0),
        "runtime_delta_ratio_min": min(runtime_drifts),
        "runtime_delta_ratio_max": max(runtime_drifts),
        "hash_change_events": hash_change_count,
        "most_unstable_payload_fields": dict(unstable_fields.most_common(10)),
        "trend": trend,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize Engine J canary artifacts.")
    parser.add_argument(
        "--artifacts-dir",
        default="artifacts/engine_j_canary",
        help="Directory containing engine_j_canary_*.json files.",
    )
    parser.add_argument(
        "--output",
        default="artifacts/engine_j_canary/summary.json",
        help="Where to write the summary JSON report.",
    )
    args = parser.parse_args()

    artifacts_dir = Path(args.artifacts_dir)
    files = sorted(artifacts_dir.glob("engine_j_canary_*.json"))
    records = [_load_record(path) for path in files]
    summary = build_summary(records)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
