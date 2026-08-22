"""Persistent archive store for findings and outcome events."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def utc_now() -> str:
    from dino.common.determinism import stable_clock

    return stable_clock()


@dataclass
class ArchiveStore:
    root: Path

    def __post_init__(self) -> None:
        self.root = Path(self.root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.findings_path = self.root / "findings.json"
        self.queue_path = self.root / "submission_queue.json"
        self.events_path = self.root / "events.jsonl"

    def _load_findings(self) -> dict[str, dict[str, Any]]:
        if not self.findings_path.is_file():
            return {}
        try:
            data = json.loads(self.findings_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
        items = data.get("findings") if isinstance(data, dict) else data
        if not isinstance(items, dict):
            return {}
        return {str(k): v for k, v in items.items() if isinstance(v, dict)}

    def save_findings(self, findings: dict[str, dict[str, Any]]) -> None:
        payload = {"version": "1.0", "updated_at": utc_now(), "findings": findings}
        self.findings_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def upsert_finding(self, finding: dict[str, Any]) -> dict[str, Any]:
        findings = self._load_findings()
        fid = str(finding["finding_id"])
        existing = findings.get(fid)
        if existing:
            merged = dict(existing)
            for key in ("runs", "mutations_tried"):
                old = list(merged.get(key) or [])
                new = list(finding.get(key) or [])
                merged[key] = list(dict.fromkeys(old + new))
            for key, value in finding.items():
                if key not in ("runs", "mutations_tried") and value not in (None, "", []):
                    if key == "status" and merged.get("submission", {}).get("h1_report_id"):
                        if value == "candidate":
                            continue
                    merged[key] = value
            merged["updated_at"] = utc_now()
            findings[fid] = merged
        else:
            record = dict(finding)
            record.setdefault("created_at", utc_now())
            record["updated_at"] = utc_now()
            findings[fid] = record
        self.save_findings(findings)
        return findings[fid]

    def get_finding(self, finding_id: str) -> dict[str, Any] | None:
        return self._load_findings().get(finding_id)

    def all_findings(self) -> list[dict[str, Any]]:
        return list(self._load_findings().values())

    def findings_by_program(self, program: str) -> list[dict[str, Any]]:
        return [f for f in self.all_findings() if str(f.get("program", "")) == program]

    def findings_by_status(self, status: str) -> list[dict[str, Any]]:
        return [f for f in self.all_findings() if str(f.get("status", "")) == status]

    def update_finding(self, finding_id: str, patch: dict[str, Any]) -> dict[str, Any] | None:
        findings = self._load_findings()
        if finding_id not in findings:
            return None
        merged = dict(findings[finding_id])
        merged.update(patch)
        merged["updated_at"] = utc_now()
        findings[finding_id] = merged
        self.save_findings(findings)
        return merged

    def append_event(self, event: dict[str, Any]) -> None:
        record = dict(event)
        record.setdefault("ts", utc_now())
        with self.events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, separators=(",", ":")) + "\n")

    def load_queue(self) -> list[dict[str, Any]]:
        if not self.queue_path.is_file():
            return []
        try:
            data = json.loads(self.queue_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        return list(data.get("items") or [])

    def save_queue(self, items: list[dict[str, Any]]) -> None:
        payload = {"version": "1.0", "updated_at": utc_now(), "items": items}
        self.queue_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
