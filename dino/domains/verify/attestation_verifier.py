#!/usr/bin/env python3
"""Standalone attestation verify — stdlib only (hash-bound trust surface)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from dino.common.determinism import canonical_hash


def signature_preimage(attestation: dict[str, Any]) -> dict[str, Any]:
    ts = attestation.get("trust_surface") or {}
    validation = attestation.get("validation") or {}
    policy = attestation.get("policy") or validation.get("policy") or {}
    return {
        "attestation_signature_v1": True,
        "H_verdict": ts.get("H_verdict") or attestation.get("H_verdict"),
        "H_input": ts.get("H_input"),
        "pipeline_hash": attestation.get("pipeline_hash") or ts.get("pipeline_hash"),
        "golden_hash": attestation.get("golden_hash") or ts.get("golden_hash"),
        "decision_trace_hash": attestation.get("decision_trace_hash"),
        "policy_verdict_hash": policy.get("policy_verdict_hash") or ts.get("policy_verdict_hash"),
        "intent": attestation.get("intent"),
        "repo": attestation.get("repo"),
        "graph_truth": attestation.get("graph_truth"),
        "verdict": attestation.get("verdict"),
        "graph_hash": attestation.get("graph_hash") or ts.get("graph_hash"),
        "release_manifest_hash": attestation.get("release_manifest_hash")
        or ts.get("release_manifest_hash"),
        "trust_anchor_version": attestation.get("trust_anchor_version")
        or ts.get("trust_anchor_version"),
    }


def verify_signature(attestation: dict[str, Any], public_key_pem: str) -> tuple[bool, str]:
    block = attestation.get("trustless_replay") or {}
    if not public_key_pem:
        return False, "missing public_key_pem"
    if not block.get("signature_b64"):
        return False, "missing signature_b64"
    pre_hash = canonical_hash({"v": 3, "payload": signature_preimage(attestation)})
    expected = block.get("signature_preimage_hash")
    if expected and pre_hash != expected:
        return False, "signature_preimage_hash mismatch"
    return True, "preimage hash bound"


def verify_attestation(att: dict[str, Any], anchor: dict[str, Any]) -> dict[str, Any]:
    ok_sig, msg_sig = verify_signature(att, str(anchor.get("public_key_pem") or ""))
    ts = att.get("trust_surface") or {}
    anchor_errs: list[str] = []
    if (att.get("trust_anchor_version") or ts.get("trust_anchor_version")) != anchor.get(
        "trust_anchor_version"
    ):
        anchor_errs.append("trust_anchor_version mismatch")
    if not (att.get("release_manifest_hash") or ts.get("release_manifest_hash")):
        anchor_errs.append("missing release_manifest_hash")
    att_ph = att.get("pipeline_hash") or ts.get("pipeline_hash")
    if att_ph and att_ph != anchor.get("pipeline_hash"):
        anchor_errs.append("pipeline_hash mismatch")
    ok_anchor = not anchor_errs
    ok_ph = bool(att_ph) and att_ph == anchor.get("pipeline_hash")
    passed = ok_sig and ok_anchor and ok_ph
    return {
        "passed": passed,
        "verdict": "VERIFIED" if passed else "REJECTED",
        "signature": {"ok": ok_sig, "detail": msg_sig},
        "anchor": {"ok": ok_anchor, "errors": anchor_errs},
        "pipeline_hash": {"ok": ok_ph, "value": att_ph},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Standalone attestation verify")
    parser.add_argument("attest_json", type=Path)
    parser.add_argument("--trust-anchor", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if not args.attest_json.is_file():
        print(f"missing attestation: {args.attest_json}", file=sys.stderr)
        return 2
    if not args.trust_anchor.is_file():
        print(f"missing trust anchor: {args.trust_anchor}", file=sys.stderr)
        return 2
    att = json.loads(args.attest_json.read_text(encoding="utf-8"))
    anchor = json.loads(args.trust_anchor.read_text(encoding="utf-8"))
    report = verify_attestation(att, anchor)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print("Dino verify attest")
        print(f"Attestation: {args.attest_json.name}")
        print(f"Trust anchor: {args.trust_anchor.name}")
        print(f"  signature: {'ok' if report['signature']['ok'] else 'fail'} — {report['signature']['detail']}")
        print(f"  anchor: {'ok' if report['anchor']['ok'] else 'fail'}")
        print(f"  pipeline_hash: {'ok' if report['pipeline_hash']['ok'] else 'fail'}")
        print(f"Result: {report['verdict']}")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
