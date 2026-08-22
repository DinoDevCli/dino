from __future__ import annotations

import sys

from dino.common.domain_self_test import run_self_test
from dino.cli import main

_DOMAIN = "map"

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "--self-test":
        raise SystemExit(run_self_test(_DOMAIN))
    raise SystemExit(main(['map', *sys.argv[1:]]))
