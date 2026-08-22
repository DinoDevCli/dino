from __future__ import annotations

import json
from pathlib import Path
from typing import Dict


class DedupStore:
    """Persist processed keys (sha256:pipeline) to skip duplicate work."""

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._data: Dict[str, Dict[str, str]] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            self._data = json.loads(self.path.read_text(encoding="utf-8") or "{}")
        except Exception:
            self._data = {}

    def _save(self) -> None:
        self.path.write_text(json.dumps(self._data, ensure_ascii=False, indent=2), encoding="utf-8")

    def contains(self, key: str) -> bool:
        return key in self._data

    def add(self, key: str, meta: Dict[str, str]) -> None:
        from dino.common.determinism import stable_clock

        record = dict(meta)
        clock = stable_clock()
        if clock:
            record["at"] = clock
        self._data[key] = record
        self._save()

    def prune_missing_files(self, repo_root: Path) -> int:
        """Entfernt Dedup-Einträge, deren Quelldatei nicht mehr existiert (z. B. nach Rotation)."""
        removed = 0
        root = repo_root.resolve()
        for key in list(self._data.keys()):
            meta = self._data[key]
            rel = (meta.get("path") or "").strip()
            if not rel:
                continue
            p = (root / rel).resolve()
            try:
                p.relative_to(root)
            except ValueError:
                continue
            if not p.is_file():
                del self._data[key]
                removed += 1
        if removed:
            self._save()
        return removed
