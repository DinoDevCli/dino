"""Install/health checks. Fixed output path, no timestamps, no incrementing IDs."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from dino.common.determinism import canonical_hash
from dino.common.utils import write_json

from .capsule import SCHEMA, make_capsule
from .execute import execute, run_command
from .replay import replay


def run_doctor(*, output_dir: Path | None = None) -> dict[str, Any]:
    checks: list[dict[str, Any]] = [
        {
            "check": "python_major_minor",
            "passed": True,
            "detail": f"{sys.version_info.major}.{sys.version_info.minor}",
        },
        {"check": "capsule_schema", "passed": True, "detail": SCHEMA},
    ]

    live = run_command(["echo", "ok"])
    sample = make_capsule(
        command=["echo", "ok"],
        output=live["stdout"],
        stderr=live["stderr"],
        exit_code=live["exit_code"],
    )
    replayed = replay(sample, reexec=True)
    checks.append(
        {
            "check": "replay_symmetry",
            "passed": bool(replayed["replay_ok"]),
            "detail": replayed["recomputed_hash"][:16],
        }
    )
    checks.append(
        {
            "check": "exec_capture",
            "passed": live["stdout"] in ("ok\n", "ok") or live["stdout"].strip() == "ok",
            "detail": repr(live["stdout"][:32]),
        }
    )

    out_dir = (output_dir or Path.cwd() / "capsule_output" / "doctor").resolve()
    writable = True
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        probe = out_dir / ".write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except OSError as exc:
        writable = False
        checks.append({"check": "output_writable", "passed": False, "detail": str(exc)})
    else:
        checks.append({"check": "output_writable", "passed": True, "detail": str(out_dir)})

    # End-to-end seal into doctor dir (overwrites fixed paths).
    if writable:
        sealed = execute(["echo", "doctor"], output_dir=out_dir, reexec_on_seal=True)
        checks.append(
            {
                "check": "seal_roundtrip",
                "passed": bool(sealed.get("replay_ok")),
                "detail": str(sealed.get("capsule_hash", ""))[:16],
            }
        )

    passed = all(c["passed"] for c in checks)
    report: dict[str, Any] = {
        "schema": "dino.capsule.doctor.v1",
        "ok": passed,
        "checks": checks,
        "report_hash": "",
    }
    report["report_hash"] = canonical_hash({k: v for k, v in report.items() if k != "report_hash"})
    if writable:
        write_json(out_dir / "result.json", report)
        (out_dir / "capsule_sample.json").write_text(
            json.dumps(sample, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    report["output_dir"] = str(out_dir)
    return report
