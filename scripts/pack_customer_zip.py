#!/usr/bin/env python3
"""Assemble a customer-pack.v1 folder + ZIP (no key issuance)."""

from __future__ import annotations

import argparse
import re
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path


PLACEHOLDERS = ("TEAM", "DAYS", "NAME", "KEY", "VERSION")


def dino_version(root: Path) -> str:
    text = (root / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'(?m)^version\s*=\s*"([^"]+)"', text)
    if match:
        return match.group(1)
    fallback = (root / "docs/internal/customer_pack/VERSION").read_text(encoding="utf-8").strip()
    if fallback:
        return fallback.splitlines()[0].strip()
    raise SystemExit("could not read Dino version from pyproject.toml")


def render(text: str, values: dict[str, str]) -> str:
    out = text
    for key in PLACEHOLDERS:
        out = out.replace("{" + key + "}", values[key])
    return out


def pack(
    *,
    root: Path,
    team: str,
    days: str,
    name: str,
    key: str,
    out_dir: Path,
    stamp: str | None = None,
) -> dict[str, Path]:
    version = dino_version(root)
    stamp = stamp or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    src = root / "docs/internal/customer_pack"
    values = {
        "TEAM": team,
        "DAYS": days,
        "NAME": name,
        "KEY": key,
        "VERSION": version,
    }

    zip_stem = f"dino-ea-{team}-v{version}-{stamp}"
    bundle = out_dir / zip_stem
    inner = bundle / team
    examples = inner / "examples"
    if bundle.exists():
        shutil.rmtree(bundle)
    examples.mkdir(parents=True)

    (inner / "KEY.txt").write_text(key.strip() + "\n", encoding="utf-8")
    (inner / "VERSION").write_text(version + "\n", encoding="utf-8")
    shutil.copy2(root / "LICENSE", inner / "LICENSE")
    (inner / "QUICKSTART.md").write_text(
        render((src / "QUICKSTART.md").read_text(encoding="utf-8"), values),
        encoding="utf-8",
    )
    (inner / "EMAIL.txt").write_text(
        render((src / "EMAIL.txt").read_text(encoding="utf-8"), values),
        encoding="utf-8",
    )
    shutil.copy2(src / "examples" / "proof_index.json", examples / "proof_index.json")
    shutil.copy2(src / "examples" / "compare.json", examples / "compare.json")

    zip_path = out_dir / f"{zip_stem}.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(inner.rglob("*")):
            if path.is_file():
                zf.write(path, arcname=str(path.relative_to(bundle)))

    return {"bundle": bundle, "zip": zip_path, "inner": inner}


def main() -> int:
    p = argparse.ArgumentParser(description="Write customer-pack.v1 ZIP")
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--team", required=True)
    p.add_argument("--days", required=True)
    p.add_argument("--name", default="there")
    p.add_argument("--key", required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--stamp", default="")
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    result = pack(
        root=args.root.resolve(),
        team=args.team,
        days=str(args.days),
        name=args.name,
        key=args.key,
        out_dir=args.out.resolve(),
        stamp=args.stamp or None,
    )
    print(result["zip"])
    print(result["inner"] / "EMAIL.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
