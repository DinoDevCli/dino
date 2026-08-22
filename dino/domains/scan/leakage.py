"""Leakage scan for research / feature-pipeline integrity (Python AST + patterns)."""

from __future__ import annotations

import ast
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class ScanFinding:
    path: str
    rule: str
    detail: str
    severity: str = "FAIL"
    line: int | None = None


@dataclass
class ScanReport:
    ok: bool
    findings: list[ScanFinding]
    files_scanned: int = 0
    rules: list[str] | None = None

    def to_dict(self) -> dict:
        return {
            "schema": "dino.scan.leakage.v1",
            "ok": self.ok,
            "files_scanned": self.files_scanned,
            "rules": self.rules or RULE_IDS,
            "findings": [asdict(f) for f in self.findings],
        }


RULE_IDS = [
    "SYNTAX",
    "LEAKY_IMPORT",
    "FUTURE_INDEX",
    "SHIFT_NEGATIVE",
    "CONVOLVE_MODE_SAME_AST",
    "SEEDLESS_SPLIT",
    "TARGET_IN_FEATURES",
]

FUTURE_INDEX = re.compile(r"(close|closes|label|y_true|target|y)\s*\[\s*i\s*\+\s*1\s*\]")
FORBIDDEN_IMPORT = re.compile(
    r"^\s*(from\s+\S*economics\s+import|import\s+\S*economics)\b",
    re.MULTILINE,
)
SHIFT_NEGATIVE = re.compile(r"\.shift\s*\(\s*-\s*\d+")
TARGET_NAME = re.compile(r"\b(label|y_true|target|close|closes)\b")


def _iter_py(roots: Iterable[Path]) -> list[Path]:
    out: list[Path] = []
    for root in roots:
        if root.is_file() and root.suffix == ".py":
            out.append(root)
            continue
        if not root.exists():
            continue
        for p in sorted(root.rglob("*.py")):
            if "__pycache__" in p.parts:
                continue
            out.append(p)
    return out


def _lineno(node: ast.AST) -> int | None:
    return getattr(node, "lineno", None)


def _call_name(node: ast.Call) -> str:
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    if isinstance(node.func, ast.Name):
        return node.func.id
    return ""


def _has_kw(node: ast.Call, name: str) -> bool:
    return any(kw.arg == name for kw in node.keywords)


def _scan_tree(path: str, tree: ast.AST, text: str, findings: list[ScanFinding]) -> None:
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = _call_name(node)
            if name == "convolve":
                for kw in node.keywords:
                    if (
                        kw.arg == "mode"
                        and isinstance(kw.value, ast.Constant)
                        and kw.value.value == "same"
                    ):
                        findings.append(
                            ScanFinding(
                                path,
                                "CONVOLVE_MODE_SAME_AST",
                                "convolve mode same (causal risk)",
                                line=_lineno(node),
                            )
                        )
            if name == "train_test_split" and not _has_kw(node, "random_state"):
                findings.append(
                    ScanFinding(
                        path,
                        "SEEDLESS_SPLIT",
                        "train_test_split without random_state",
                        line=_lineno(node),
                    )
                )
            # drop(columns=[...]) / feature matrix including label-ish names
            if name in {"drop", "DataFrame"}:
                pass

        if isinstance(node, ast.Assign):
            # X = df[["a", "label"]] style target-in-features
            if isinstance(node.value, ast.Subscript):
                targets = [t for t in node.targets if isinstance(t, ast.Name)]
                if targets and targets[0].id.lower() in {"x", "features", "x_train", "x_test"}:
                    snippet = ast.dump(node.value.slice) if hasattr(node.value, "slice") else ""
                    if TARGET_NAME.search(snippet) or TARGET_NAME.search(ast.dump(node.value)):
                        findings.append(
                            ScanFinding(
                                path,
                                "TARGET_IN_FEATURES",
                                "feature matrix appears to include label/target columns",
                                line=_lineno(node),
                            )
                        )

    if FUTURE_INDEX.search(text):
        findings.append(ScanFinding(path, "FUTURE_INDEX", "lookahead index i+1"))
    if FORBIDDEN_IMPORT.search(text):
        findings.append(ScanFinding(path, "LEAKY_IMPORT", "forbidden economics import"))
    if SHIFT_NEGATIVE.search(text):
        findings.append(ScanFinding(path, "SHIFT_NEGATIVE", "negative shift (future peek)"))


def scan_paths(roots: list[Path]) -> ScanReport:
    findings: list[ScanFinding] = []
    files = _iter_py(roots)
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        display = str(path)
        try:
            tree = ast.parse(text)
        except SyntaxError as exc:
            findings.append(ScanFinding(display, "SYNTAX", str(exc), line=exc.lineno))
            continue
        _scan_tree(display, tree, text, findings)
    fails = [f for f in findings if f.severity == "FAIL"]
    return ScanReport(
        ok=len(fails) == 0,
        findings=findings,
        files_scanned=len(files),
        rules=list(RULE_IDS),
    )


def main(argv: list[str] | None = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Leakage scan")
    p.add_argument("paths", nargs="+", type=Path)
    args = p.parse_args(argv)
    report = scan_paths(list(args.paths))
    print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
