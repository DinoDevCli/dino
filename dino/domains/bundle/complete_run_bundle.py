#!/usr/bin/env python3
"""
Merge all artifacts from a Brain repo-runner style analysis into one JSON file.

Typical inputs:
  --rundata   Path to full_dump.json (metadata, ir, engines, …)
  --repo-root Repo used for the run (reads .brain/incremental.json when present)

Output: one JSON with schema brain-complete-run-v1.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_extra_json_args(raw: list[str] | None) -> dict[str, Path]:
    out: dict[str, Path] = {}
    if not raw:
        return out
    for item in raw:
        if "=" not in item:
            raise SystemExit(f"--extra-json requires ROLE=PATH, got: {item!r}")
        role, path = item.split("=", 1)
        role = role.strip()
        if not role:
            raise SystemExit(f"Invalid --extra-json (empty role): {item!r}")
        out[role] = Path(path).expanduser().resolve()
    return out


def build_complete_run_bundle_dict(
    *,
    rundata_path: Path,
    repo_root: Path | None,
    extra_json: dict[str, Path] | None = None,
) -> dict[str, Any]:
    sources: list[dict[str, Any]] = []
    brain_run = _load_json(rundata_path)
    sources.append(
        {
            "role": "brain_run",
            "path": str(rundata_path.resolve()),
            "bytes": rundata_path.stat().st_size,
        }
    )

    incremental: dict[str, Any] | None = None
    inc_path: Path | None = None
    if repo_root is not None:
        candidate = (repo_root / ".brain" / "incremental.json").resolve()
        if candidate.is_file():
            incremental = _load_json(candidate)
            inc_path = candidate
            sources.append(
                {
                    "role": "incremental_disk_state",
                    "path": str(candidate),
                    "bytes": candidate.stat().st_size,
                }
            )

    extras: dict[str, Any] = {}
    extras_manifest: list[dict[str, Any]] = []
    if extra_json:
        for role, pth in sorted(extra_json.items()):
            if not pth.is_file():
                raise FileNotFoundError(f"--extra-json file missing: {role}={pth}")
            extras[role] = _load_json(pth)
            extras_manifest.append({"role": role, "path": str(pth), "bytes": pth.stat().st_size})
            sources.append({"role": f"extra:{role}", "path": str(pth), "bytes": pth.stat().st_size})

    result: dict[str, Any] = {
        "bundle_schema": "complete-run-v1",
        "manifest": {
            "description": "Archiv: brain_run (RunData), optional incremental_disk_state, optional extra_json Artefakte.",
            "sources": sources,
            "extras": extras_manifest or None,
        },
        "brain_run": brain_run,
        "incremental_disk_state": incremental,
        "incremental_path": str(inc_path) if inc_path else None,
    }
    if extras:
        result["extras"] = extras
    return result


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Pack Brain rundata + incremental.json into one JSON file.")
    p.add_argument(
        "--rundata",
        type=Path,
        required=True,
        help="Pfad zu full_dump.json oder anderer Brain-Rundaten-JSON.",
    )
    p.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repo-Wurzel (optional): laedt .brain/incremental.json wenn vorhanden.",
    )
    p.add_argument(
        "--output",
        "-o",
        type=Path,
        required=True,
        help="Zieldatei fuer das kombinierte Bundle.",
    )
    p.add_argument(
        "--extra-json",
        action="append",
        default=None,
        metavar="ROLE=PATH",
        help="Weitere JSON-Ausgaben einbetten (ROLE=PATH, z.B. extras=/tmp/report.json). Wiederholbar.",
    )
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    extras = _parse_extra_json_args(args.extra_json)
    bundle = build_complete_run_bundle_dict(
        rundata_path=args.rundata.resolve(),
        repo_root=args.repo_root.resolve() if args.repo_root else None,
        extra_json=extras if extras else None,
    )
    out = args.output.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": "ok", "output": str(out), "bytes": out.stat().st_size}, indent=2))


if __name__ == "__main__":
    main()
