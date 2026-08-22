"""Demo hotpath module for import-fanout checks."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    print("hotpath ok", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
