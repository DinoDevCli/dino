from pathlib import Path
import json, hashlib
from typing import Any, Dict, List

def _sha256(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()

def build_run_payload_v1_1(
    *,
    core_version: str,
    execution_graph: List[str],
    signals: Dict[str, Any],
    decision: str,
    explainability: Dict[str, Any],
    evidence: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "schema_version": "1.1.0",
        "core_version": core_version,
        "execution_graph": execution_graph,
        "signals": signals,
        "decision": decision,
        "explainability": explainability,
        "evidence": evidence,
    }

def write_run_artifact_v1_1(out_path: str | Path, payload: Dict[str, Any]) -> Path:
    hash_hex = _sha256(payload)
    envelope = {
        "envelope_version": "1.1.0",
        "artifact_type": "run_artifact",
        "artifact_version": "1.1.0",
        "hash_sha256": hash_hex,
        "payload": payload,
    }
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(envelope, indent=2), encoding="utf-8")
    return out_path


if __name__ == "__main__":
    # CLI: write a demo artifact under ./artifacts/ (cwd-relative) for tests / local runs.
    demo = build_run_payload_v1_1(
        core_version="0.1.0",
        execution_graph=["brain", "vault", "kernel", "governance"],
        signals={"risk_score": 1},
        decision="pass",
        explainability={"reason": "demo roundtrip"},
        evidence={"files_checked": 1},
    )
    write_run_artifact_v1_1(Path.cwd() / "artifacts" / "run_artifact_v1_1.json", demo)
