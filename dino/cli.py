"""Dino CLI — Deterministic Proof for Python Decision Pipelines."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from dino import __version__
from dino.common.output import Output


def _pop_json_flag(argv: list[str]) -> tuple[list[str], bool]:
    json_mode = "--json" in argv
    return [a for a in argv if a != "--json"], json_mode


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="dino",
        description="Deterministic Proof for Python Decision Pipelines",
        epilog=(
            "Meta: dino version | packs | status | upgrade --pack proof --key KEY | "
            "init-license. Global: --json for machine-readable envelopes."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--version", action="version", version=f"dino {__version__}")
    p.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON envelopes (also accepted before the domain)",
    )
    sub = p.add_subparsers(dest="domain", required=True)

    # Kept product surface only (see packs.py / README)
    _scan(sub)
    _bundle(sub)
    _flight(sub)
    _verify_domain(sub)
    _map(sub)
    _capsule(sub)
    _proof(sub)
    return p


def _group(sub: argparse._SubParsersAction, name: str, help_text: str) -> argparse.ArgumentParser:
    g = sub.add_parser(name, help=help_text)
    g.set_defaults(domain=name)
    return g


def _bundle(sub: argparse._SubParsersAction) -> None:
    g = _group(sub, "bundle", "Run bundles and local stores")
    s = g.add_subparsers(dest="cmd", required=True)
    b = s.add_parser("create", help="Build complete run bundle")
    b.add_argument("--rundata", required=True)
    b.add_argument("--output", required=True)
    b.add_argument("--repo-root", default="")
    rp = s.add_parser("replay", help="Compare current dump against replay baseline")
    rp.add_argument("--baseline", required=True, help="Baseline JSON path")
    rp.add_argument("--current", required=True, help="Current dump or baseline-shaped JSON")
    rp.add_argument("--target-id", default="default")
    bv = s.add_parser("verify", help="Alias of replay — official regression gate (exit 1 on fail)")
    bv.add_argument("--baseline", required=True)
    bv.add_argument("--current", required=True)
    bv.add_argument("--target-id", default="default")
    bd = s.add_parser("diff", help="Same comparison as verify, always exit 0 (review)")
    bd.add_argument("--baseline", required=True)
    bd.add_argument("--current", required=True)
    bd.add_argument("--target-id", default="default")
    a = s.add_parser("archive", help="Initialize archive store")
    a.add_argument("--path", default="./.dino-archive")
    d = s.add_parser("dedup", help="Initialize dedup store")
    d.add_argument("--path", default="./.dino-dedup.json")


def _flight(sub: argparse._SubParsersAction) -> None:
    g = _group(sub, "flight", "Canary flight summary")
    s = g.add_subparsers(dest="cmd", required=True)
    sm = s.add_parser("summary", help="Summarize canary artifacts")
    sm.add_argument("--artifacts-dir", required=True)
    sm.add_argument("--output", required=True)


def _verify_domain(sub: argparse._SubParsersAction) -> None:
    g = _group(sub, "verify", "Attestation verification")
    s = g.add_subparsers(dest="cmd", required=True)
    v = s.add_parser("attest", help="Verify attestation document")
    v.add_argument("attest_json")
    v.add_argument("--trust-anchor", required=True)
    bv = s.add_parser("binary", help="Binary attestation verify")
    bv.add_argument("attestation")
    bv.add_argument("--repo", default=".")
    dc = s.add_parser("drift", help="Classify attestation drift")
    dc.add_argument("--distance", type=int, required=True)
    dc.add_argument("--tau", type=int, default=5)
    dc.add_argument("--graph-truth", default="")
    su = s.add_parser("supersede", help="Runtime supersession check")
    su.add_argument("--runtime-verdict", required=True)
    su.add_argument("--release-verdict", default="APPROVED")
    su.add_argument("--contract", default="", help="Contract JSON (optional; demo if omitted)")
    su.add_argument("--previous", default="", help="Previous contract JSON")


def _map(sub: argparse._SubParsersAction) -> None:
    g = _group(sub, "map", "Import graph mapping and planning")
    s = g.add_subparsers(dest="cmd", required=True)
    a = s.add_parser("analyze", help="Analyze import graph")
    a.add_argument("path")
    v = s.add_parser("verify", help="Structural quality verify")
    v.add_argument("--repo", required=True)
    v.add_argument("--baseline", default="")
    pl = s.add_parser("plan", help="Topological execution plan")
    pl.add_argument("path")
    dr = s.add_parser("drift", help="Graph drift vs baseline")
    dr.add_argument("path")
    dr.add_argument("--baseline", required=True)
    dr.add_argument("--tau", type=int, default=5)


def _capsule(sub: argparse._SubParsersAction) -> None:
    g = _group(sub, "capsule", "Sealed execution capsules")
    s = g.add_subparsers(dest="cmd", required=True)
    run = s.add_parser("run", help="Execute command into capsule")
    run.add_argument("--output-dir", default="./capsule_output/run")
    run.add_argument(
        "--command",
        nargs="+",
        default=["echo", "ok"],
        help='Argv to seal, e.g. echo ok (or one string: "echo ok")',
    )
    rep = s.add_parser("replay", help="Replay capsule")
    rep.add_argument("--capsule", required=True)
    rep.add_argument("--output-dir", default="./capsule_output/replay")
    doc = s.add_parser("doctor", help="Capsule environment doctor")
    doc.add_argument("--output-dir", default="./capsule_output/doctor")


def _proof(sub: argparse._SubParsersAction) -> None:
    g = _group(sub, "proof", "Unique proof chain: capsule + scan + map")
    s = g.add_subparsers(dest="cmd", required=True)
    run = s.add_parser("run", help="Seal command + optional scan/map into proof.json")
    run.add_argument("--output-dir", default="./proof_output")
    run.add_argument(
        "--command",
        nargs="+",
        default=["echo", "ok"],
        help='Argv to seal, e.g. echo ok (or one string: "echo ok")',
    )
    run.add_argument("--repo", default="", help="Optional repo for map verify")
    run.add_argument("--scan", nargs="*", default=[], help="Optional paths for leakage scan")
    run.add_argument("--stdin", default="")
    run.add_argument(
        "--export",
        default="",
        help="Upload sealed proof: path | http(s)://… | s3://bucket/prefix",
    )
    run.add_argument("--pipeline", default="", help="Pipeline label for proof_index.json")
    run.add_argument("--group", default="", help="Group label for proof_index.json")
    run.add_argument("--tag", action="append", default=[], help="Tag for proof_index.json (repeatable)")
    ver = s.add_parser("verify", help="Re-verify a proof.json bundle")
    ver.add_argument("--proof", required=True)
    exp = s.add_parser("export", help="Upload an existing proof directory")
    exp.add_argument(
        "--proof-dir",
        default="",
        help="Directory containing proof.json (default: parent of --proof)",
    )
    exp.add_argument("--proof", default="", help="Path to proof.json (alternative to --proof-dir)")
    exp.add_argument(
        "--to",
        required=True,
        help="Destination: path | http(s)://… | s3://bucket/prefix",
    )
    exp.add_argument("--pipeline", default="", help="Pipeline label for proof_index.json")
    exp.add_argument("--group", default="", help="Group label for proof_index.json")
    exp.add_argument("--tag", action="append", default=[], help="Tag for proof_index.json (repeatable)")
    idx = s.add_parser("index", help="Proof index manifest (proof_index.json)")
    idx_sub = idx.add_subparsers(dest="index_cmd", required=True)
    idx_show = idx_sub.add_parser("show", help="Print proof_index.json")
    idx_show.add_argument("archive", help="Archive directory containing proof_index.json")
    idx_rebuild = idx_sub.add_parser("rebuild", help="Rebuild index from archive subfolders")
    idx_rebuild.add_argument("archive", help="Archive root to scan")
    idx_cmp = idx_sub.add_parser("compare", help="Compare two proofs by hash/prefix")
    idx_cmp.add_argument("archive", help="Archive directory")
    idx_cmp.add_argument("hash_a", help="First proof hash (or prefix / path)")
    idx_cmp.add_argument("hash_b", help="Second proof hash (or prefix / path)")
    idx_metrics = idx_sub.add_parser("metrics", help="Aggregate health summary JSON")
    idx_metrics.add_argument("archive", help="Archive directory")
    idx_layout = idx_sub.add_parser("layout", help="Refresh pipelines/groups/tags browse links")
    idx_layout.add_argument("archive", help="Archive directory")
    doc = s.add_parser("doctor", help="Proof-stack health checks")
    doc.add_argument("--output-dir", default="")


def _scan(sub: argparse._SubParsersAction) -> None:
    g = _group(sub, "scan", "Grammar and leakage scanning")
    s = g.add_subparsers(dest="cmd", required=True)
    s.add_parser("grammar", help="Expression grammar smoke test")
    ls = s.add_parser("leakage", help="Static leakage scan")
    ls.add_argument("paths", nargs="+")


def _out(domain: str, command: str, json_mode: bool) -> Output:
    return Output(domain=domain, command=command, json_mode=json_mode)


def _fail(out: Output, error_type: str, detail: str, code: int = 1) -> int:
    out.emit_error(error_type, detail)
    return code


def dispatch(args: argparse.Namespace, json_mode: bool) -> int:
    domain, cmd = args.domain, args.cmd
    from dino.license import is_domain_active, required_packs_for_domain

    if not is_domain_active(domain):
        need = required_packs_for_domain(domain)
        hint = need[0] if need else "proof"
        out = _out(domain, cmd or "unknown", json_mode)
        return _fail(
            out,
            "pack_locked",
            f"Domain '{domain}' is locked. Unlock with: dino upgrade --pack {hint}  (see: dino packs)",
            2,
        )
    handlers = {
        "bundle": _run_bundle,
        "flight": _run_flight,
        "verify": _run_verify,
        "map": _run_map,
        "capsule": _run_capsule,
        "scan": _run_scan,
        "proof": _run_proof,
    }
    fn = handlers.get(domain)
    if fn is None:
        out = _out(domain, cmd or "unknown", json_mode)
        return _fail(out, "unknown_domain", f"unknown domain: {domain}", 2)
    return fn(args, cmd, json_mode)





def _bundle_compare(args: argparse.Namespace) -> tuple[int, dict[str, Any] | None, str | None]:
    """Shared baseline compare. Returns (load_error_code_or_0, result, error_detail)."""
    from dino.domains.bundle.replay_baseline import (
        ReplayBaseline,
        build_baseline_from_dump,
        compare_regression,
        load_baseline,
    )

    baseline_path = Path(args.baseline)
    current_path = Path(args.current)
    if not baseline_path.is_file():
        return 2, None, f"missing baseline: {baseline_path}"
    if not current_path.is_file():
        return 2, None, f"missing current: {current_path}"
    baseline = load_baseline(baseline_path)
    if baseline is None:
        return 2, None, f"could not load baseline: {baseline_path}"
    current_raw = json.loads(current_path.read_text(encoding="utf-8"))
    if "true_count" in current_raw and "verified_hotspots" not in current_raw:
        if "endpoint_count" not in current_raw and "endpoints" in current_raw:
            current_raw = {
                **current_raw,
                "endpoint_count": len(current_raw.get("endpoints") or []),
            }
        current = ReplayBaseline.from_dict(current_raw)
    else:
        current = build_baseline_from_dump(args.target_id, current_raw)
    raw_b = json.loads(baseline_path.read_text(encoding="utf-8"))
    if baseline.endpoint_count == 0 and isinstance(raw_b.get("endpoints"), list):
        baseline = ReplayBaseline.from_dict(
            {**raw_b, "endpoint_count": len(raw_b.get("endpoints") or [])}
        )
    result = compare_regression(current, baseline)
    result["schema"] = "dino.bundle.regression.v1"
    result["audit"] = {
        "verdict": "BUNDLE_REGRESSION_PASSED" if result.get("passed") else "BUNDLE_REGRESSION_FAILED",
        "summary": (
            "Baseline met (true_count and endpoint coverage)."
            if result.get("passed")
            else "Regression: true_count or endpoint coverage below baseline."
        ),
        "reasons": [
            f"true_delta={result.get('true_delta')}",
            f"endpoint_ratio={result.get('endpoint_ratio')}",
        ],
    }
    return 0, result, None


def _run_bundle(args: argparse.Namespace, cmd: str, json_mode: bool) -> int:
    out = _out("bundle", cmd, json_mode)
    if cmd == "create":
        from dino.domains.bundle.complete_run_bundle import build_complete_run_bundle_dict
        from dino.common.utils import write_json

        bundle = build_complete_run_bundle_dict(
            rundata_path=Path(args.rundata),
            repo_root=Path(args.repo_root) if args.repo_root else None,
        )
        target = write_json(Path(args.output), bundle)
        out.emit_success({"bytes": target.stat().st_size, "output": str(target), "status": "ok"})
        return 0
    if cmd in {"replay", "verify", "diff"}:
        code, result, detail = _bundle_compare(args)
        if result is None:
            return _fail(out, "missing_file" if code == 2 else "invalid_baseline", detail or "compare failed", code)
        out.emit_success(result)
        if cmd == "diff":
            return 0
        return 0 if result.get("passed") else 1
    if cmd == "archive":
        from dino.domains.bundle.archive_store import ArchiveStore

        ArchiveStore(Path(args.path))
        out.emit_success({"path": args.path, "status": "initialized", "store": "archive"})
        return 0
    if cmd == "dedup":
        from dino.domains.bundle.dedup_store import DedupStore

        DedupStore(Path(args.path))
        out.emit_success({"path": args.path, "status": "initialized", "store": "dedup"})
        return 0
    return _fail(out, "unknown_command", f"unknown bundle command: {cmd}", 2)






def _run_flight(args: argparse.Namespace, cmd: str, json_mode: bool) -> int:
    out = _out("flight", cmd, json_mode)
    if cmd == "summary":
        from dino.domains.flight.engine_j_canary_summary import _load_record, build_summary
        from dino.common.utils import write_json

        artifacts = Path(args.artifacts_dir)
        files = sorted(artifacts.glob("engine_j_canary_*.json"))
        records = [_load_record(path) for path in files]
        summary = build_summary(records)
        write_json(Path(args.output), summary)
        out.emit_success(summary)
        return 0 if "error" not in summary else 1
    return _fail(out, "unknown_command", f"unknown flight command: {cmd}", 2)


def _run_verify(args: argparse.Namespace, cmd: str, json_mode: bool) -> int:
    out = _out("verify", cmd, json_mode)
    if cmd == "attest":
        from dino.domains.verify.attestation_verifier import verify_attestation

        att_path = Path(args.attest_json)
        anchor_path = Path(args.trust_anchor)
        if not att_path.is_file():
            return _fail(out, "missing_file", f"missing attestation: {att_path}", 2)
        if not anchor_path.is_file():
            return _fail(out, "missing_file", f"missing trust anchor: {anchor_path}", 2)
        report = verify_attestation(
            json.loads(att_path.read_text(encoding="utf-8")),
            json.loads(anchor_path.read_text(encoding="utf-8")),
        )
        out.emit_success(report)
        return 0 if report.get("passed") else 1
    if cmd == "binary":
        from dino.domains.verify.attestation_binary_verify import verify_attestation_binary

        att_path = Path(args.attestation)
        if not att_path.is_file():
            return _fail(out, "missing_file", f"missing attestation: {att_path}", 2)
        att = json.loads(att_path.read_text(encoding="utf-8"))
        report = verify_attestation_binary(att, repo_path=Path(args.repo))
        out.emit_success(report)
        return 0 if report.get("passed") else 1
    if cmd == "drift":
        from dino.domains.verify.drift_classifier import classify_drift

        label = classify_drift(distance=args.distance, tau=args.tau, graph_truth=args.graph_truth)
        out.emit_success({"bucket": label, "distance": args.distance, "tau": args.tau})
        return 0
    if cmd == "supersede":
        from dino.domains.verify.supersession_checker import (
            apply_runtime_supersession,
            verify_supersession_chain,
        )

        if args.contract:
            cpath = Path(args.contract)
            if not cpath.is_file():
                return _fail(out, "missing_file", f"missing contract: {cpath}", 2)
            doc = json.loads(cpath.read_text(encoding="utf-8"))
        else:
            doc = {"decision": {"decision_id": "demo-1", "revision": 0, "verdict": args.release_verdict}}
        prev = None
        if args.previous:
            ppath = Path(args.previous)
            if not ppath.is_file():
                return _fail(out, "missing_file", f"missing previous: {ppath}", 2)
            prev = json.loads(ppath.read_text(encoding="utf-8"))
        elif not args.contract:
            prev = {"decision": {"decision_id": "demo-0", "revision": 0}}
        result = apply_runtime_supersession(
            doc,
            previous_doc=prev,
            runtime_verdict=args.runtime_verdict,
            release_verdict=args.release_verdict,
        )
        chain_ok, chain_detail = verify_supersession_chain(result, previous_doc=prev)
        result["chain_ok"] = chain_ok
        result["chain_detail"] = chain_detail
        out.emit_success(result)
        return 0 if chain_ok else 1
    return _fail(out, "unknown_command", f"unknown verify command: {cmd}", 2)


def _run_map(args: argparse.Namespace, cmd: str, json_mode: bool) -> int:
    out = _out("map", cmd, json_mode)
    if cmd == "analyze":
        from dino.domains.map.graph import build_graph
        from dino.domains.map.planner import plan

        graph = build_graph(Path(args.path))
        planned = plan(graph)
        out.emit_success({"graph": graph, "plan": planned})
        return 0
    if cmd == "verify":
        from dino.domains.map.verify import verify_repo

        baseline = None
        if args.baseline:
            baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
        report = verify_repo(args.repo, baseline=baseline)
        out.emit_success(report)
        return 0
    if cmd == "plan":
        from dino.domains.map.graph import build_graph
        from dino.domains.map.planner import plan

        planned = plan(build_graph(Path(args.path)))
        out.emit_success(planned)
        return 0
    if cmd == "drift":
        from dino.domains.map.drift import compare
        from dino.domains.map.graph import build_graph

        current = build_graph(Path(args.path))
        baseline = build_graph(Path(args.baseline))
        out.emit_success(compare(current, baseline, tau=args.tau))
        return 0
    return _fail(out, "unknown_command", f"unknown map command: {cmd}", 2)


def _run_capsule(args: argparse.Namespace, cmd: str, json_mode: bool) -> int:
    out = _out("capsule", cmd, json_mode)
    from dino.common.utils import read_json

    outdir = Path(args.output_dir)
    if cmd == "doctor":
        from dino.domains.capsule.doctor import run_doctor

        report = run_doctor(output_dir=outdir)
        out.emit_success(report)
        return 0 if report.get("ok") else 1
    if cmd == "run":
        from dino.domains.capsule.execute import execute

        try:
            result = execute(list(args.command), output_dir=outdir)
        except ValueError as exc:
            return _fail(out, "invalid_args", str(exc), 2)
        out.emit_success(result)
        return 0 if result.get("replay_ok") else 1
    if cmd == "replay":
        from dino.domains.capsule.replay import replay

        cap = Path(args.capsule)
        if not cap.is_file():
            return _fail(out, "missing_file", f"capsule missing: {cap}", 1)
        try:
            report = replay(read_json(cap))
        except ValueError as exc:
            return _fail(out, "invalid_args", str(exc), 2)
        out.emit_success(report)
        return 0 if report.get("replay_ok") else 1
    return _fail(out, "unknown_command", f"unknown capsule command: {cmd}", 2)



def _run_scan(args: argparse.Namespace, cmd: str, json_mode: bool) -> int:
    out = _out("scan", cmd, json_mode)
    if cmd == "grammar":
        from dino.domains.scan.grammar import smoke

        out.emit_success(smoke())
        return 0
    if cmd == "leakage":
        from dino.domains.scan.leakage import scan_paths

        report = scan_paths([Path(p) for p in args.paths])
        out.emit_success(report.to_dict())
        return 0 if report.ok else 1
    return _fail(out, "unknown_command", f"unknown scan command: {cmd}", 2)


def _emit_proof_result(out: Output, result: dict, *, json_mode: bool) -> None:
    from dino.domains.proof.chain import format_audit_banner

    if json_mode:
        out.emit_success(result)
        return
    # Audit-event style text (not a generic Done-only banner).
    import sys

    banner = format_audit_banner(result)
    sys.stdout.write(f"🔍 proof {out.command}\n")
    sys.stdout.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    sys.stdout.write(banner + "\n")
    sys.stdout.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    sys.stdout.write(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def _run_proof(args: argparse.Namespace, cmd: str, json_mode: bool) -> int:
    out = _out("proof", cmd, json_mode)
    if cmd == "run":
        from dino.domains.proof.chain import build_proof

        if not args.command:
            return _fail(out, "invalid_args", "proof run requires --command", 2)
        repo = Path(args.repo) if args.repo else None
        scan_roots = [Path(p) for p in (args.scan or [])] or None
        try:
            proof = build_proof(
                output_dir=Path(args.output_dir),
                command=list(args.command),
                repo=repo,
                scan_roots=scan_roots,
                stdin=args.stdin,
            )
        except ValueError as exc:
            return _fail(out, "invalid_args", str(exc), 2)

        export_dest = getattr(args, "export", "") or ""
        if export_dest.strip():
            from dino.domains.proof.export import IndexMeta, export_proof_dir

            try:
                export_report = export_proof_dir(
                    Path(args.output_dir),
                    export_dest.strip(),
                    meta=IndexMeta.from_namespace(args),
                )
            except ValueError as exc:
                return _fail(out, "export_failed", str(exc), 1)
            proof = dict(proof)
            proof["export"] = export_report

        _emit_proof_result(out, proof, json_mode=json_mode)
        return 0 if proof.get("ok") else 1
    if cmd == "export":
        from dino.domains.proof.export import IndexMeta, export_proof_dir

        proof_dir = getattr(args, "proof_dir", "") or ""
        proof_path = getattr(args, "proof", "") or ""
        if proof_dir:
            base = Path(proof_dir)
        elif proof_path:
            base = Path(proof_path).resolve().parent
        else:
            return _fail(out, "invalid_args", "proof export requires --proof-dir or --proof", 2)
        try:
            report = export_proof_dir(base, args.to, meta=IndexMeta.from_namespace(args))
        except ValueError as exc:
            return _fail(out, "export_failed", str(exc), 1)
        out.emit_success(report)
        return 0 if report.get("ok") else 1
    if cmd == "index":
        from dino.domains.proof.index import (
            compare_refs,
            index_file_path,
            load_index,
            metrics_summary,
            rebuild_index_from_archive,
            refresh_layout,
            save_index,
        )

        archive = Path(args.archive)
        if args.index_cmd == "show":
            index = load_index(index_file_path(archive))
            if json_mode:
                out.emit_success(index)
            else:
                import sys

                sys.stdout.write(json.dumps(index, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
            return 0
        if args.index_cmd == "rebuild":
            index = rebuild_index_from_archive(archive)
            path = save_index(index_file_path(archive), index)
            layout = refresh_layout(archive, index)
            payload = {
                "ok": True,
                "index_path": str(path),
                "proof_count": len(index.get("proofs") or []),
                "layout": {"linked": layout.get("linked")},
            }
            if json_mode:
                out.emit_success(payload)
            else:
                import sys

                sys.stdout.write(
                    f"Rebuilt {path} ({payload['proof_count']} proofs, "
                    f"{layout.get('linked')} layout links)\n"
                )
            return 0
        if args.index_cmd == "compare":
            index = load_index(index_file_path(archive))
            try:
                report = compare_refs(index, args.hash_a, args.hash_b)
            except ValueError as exc:
                return _fail(out, "not_found", str(exc), 2)
            if json_mode:
                out.emit_success(report)
            else:
                import sys

                sys.stdout.write(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
            return 0 if not report.get("changed") else 1
        if args.index_cmd == "metrics":
            index = load_index(index_file_path(archive))
            report = metrics_summary(index)
            if json_mode:
                out.emit_success(report)
            else:
                import sys

                sys.stdout.write(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
            return 0
        if args.index_cmd == "layout":
            index = load_index(index_file_path(archive))
            report = refresh_layout(archive, index)
            if json_mode:
                out.emit_success(report)
            else:
                import sys

                sys.stdout.write(
                    f"Layout refreshed: {report.get('linked')} linked under {archive}\n"
                )
            return 0 if report.get("ok") else 1
        return _fail(out, "unknown_command", f"unknown proof index command: {args.index_cmd}", 2)
    if cmd == "verify":
        from dino.domains.proof.chain import verify_proof

        path = Path(args.proof)
        if not path.is_file():
            return _fail(out, "missing_file", f"Proof failed because proof file is missing: {path}", 2)
        report = verify_proof(path)
        _emit_proof_result(out, report, json_mode=json_mode)
        return 0 if report.get("ok") else 1
    if cmd == "doctor":
        from dino.domains.proof.chain import run_proof_doctor

        outdir = Path(args.output_dir) if args.output_dir else None
        report = run_proof_doctor(output_dir=outdir)
        _emit_proof_result(out, report, json_mode=json_mode)
        return 0 if report.get("ok") else 1
    return _fail(out, "unknown_command", f"unknown proof command: {cmd}", 2)


def _run_meta(argv: list[str], json_mode: bool) -> int:
    """Handle packs / upgrade / status / init-license outside domain parser."""
    from dino.license import (
        activate_pack,
        get_active_packs,
        is_domain_active,
        load_license,
        save_license,
    )
    from dino.packs import ALL_DOMAINS, PACKS, resolve_pack_name

    cmd = argv[0]
    if cmd == "packs":
        active = set(get_active_packs())
        rows = []
        for name, meta in PACKS.items():
            rows.append(
                {
                    "pack": name,
                    "tier": meta.get("tier"),
                    "price_hint": meta.get("price_hint"),
                    "active": name in active,
                    "domains": meta.get("domains", []),
                    "description": meta.get("description", ""),
                }
            )
        if json_mode:
            sys.stdout.write(json.dumps({"active_packs": sorted(active), "packs": rows}, indent=2) + "\n")
            return 0
        sys.stdout.write("Dino packs (free + proof)\n\n")
        for row in rows:
            mark = "*" if row["active"] else " "
            sys.stdout.write(f"[{mark}] {row['pack']:10} {row['tier']:5}  {row['price_hint']}\n")
            sys.stdout.write(f"    {row['description']}\n")
            sys.stdout.write(f"    domains: {', '.join(row['domains'])}\n\n")
        sys.stdout.write("Unlock:  dino upgrade --pack proof --key YOUR_LICENSE_KEY\n")
        return 0

    if cmd == "status":
        active = get_active_packs()
        payload = {
            "version": __version__,
            "license_path": str(Path.home() / ".dino" / "license.json"),
            "active_packs": active,
            "domains": {d: is_domain_active(d) for d in ALL_DOMAINS},
        }
        if json_mode:
            sys.stdout.write(json.dumps(payload, indent=2) + "\n")
            return 0
        sys.stdout.write(f"dino {__version__}\n")
        sys.stdout.write(f"Active packs: {', '.join(active)}\n")
        for d, ok in payload["domains"].items():
            sys.stdout.write(f"  [{'ON ' if ok else 'OFF'}] {d}\n")
        return 0

    if cmd == "init-license":
        path = save_license(load_license())
        sys.stdout.write(f"Wrote {path} (default pack: free)\n")
        return 0

    if cmd == "upgrade":
        pack = None
        key = ""
        args = argv[1:]
        i = 0
        while i < len(args):
            if args[i] == "--pack" and i + 1 < len(args):
                pack = args[i + 1]
                i += 2
                continue
            if args[i].startswith("--pack="):
                pack = args[i].split("=", 1)[1]
                i += 1
                continue
            if args[i] == "--key" and i + 1 < len(args):
                key = args[i + 1]
                i += 2
                continue
            if args[i].startswith("--key="):
                key = args[i].split("=", 1)[1]
                i += 1
                continue
            i += 1
        if not pack:
            sys.stderr.write("Usage: dino upgrade --pack proof|free --key KEY\n")
            return 2
        try:
            lic = activate_pack(pack, key=key)
        except ValueError as exc:
            sys.stderr.write(f"{exc}\n")
            return 2
        name = resolve_pack_name(pack)
        meta = PACKS[name]
        sys.stdout.write(f"Activated pack: {name} ({meta.get('price_hint', '')})\n")
        sys.stdout.write(f"Active packs: {', '.join(lic['active_packs'])}\n")
        return 0

    sys.stderr.write(f"Unknown meta command: {cmd}\n")
    return 2


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv == ["version"] or (len(argv) == 1 and argv[0] == "version"):
        sys.stdout.write(f"{__version__}\n")
        return 0
    argv, json_mode = _pop_json_flag(argv)
    if argv and argv[0] in {"packs", "upgrade", "status", "init-license"}:
        return _run_meta(argv, json_mode)
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code
        return 0 if code is None else int(code) if isinstance(code, int) else 1
    return dispatch(args, json_mode)


if __name__ == "__main__":
    raise SystemExit(main())
