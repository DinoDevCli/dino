from __future__ import annotations

from pathlib import Path


def cwd_root() -> Path:
    return Path.cwd().resolve()


def resolve_path(raw: str | Path, *, base: Path | None = None) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = (base or cwd_root()) / path
    return path.resolve()
