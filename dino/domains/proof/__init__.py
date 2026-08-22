"""Proof domain — unique market surface: sealed run + integrity + structure."""

from .chain import (
    SCHEMA,
    SCHEMAS,
    build_proof,
    format_audit_banner,
    run_proof_doctor,
    verify_proof,
)

__all__ = [
    "SCHEMA",
    "SCHEMAS",
    "build_proof",
    "format_audit_banner",
    "run_proof_doctor",
    "verify_proof",
]
