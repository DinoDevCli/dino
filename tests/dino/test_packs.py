"""Pack gating for the live dino CLI — Free Snapshot vs Proof Pack System Mode."""

from __future__ import annotations

from dino.license import (
    DEFAULT_LICENSE,
    activate_pack,
    get_active_packs,
    has_proof_pack,
    is_domain_active,
    save_license,
)
from dino.packs import PACKS, resolve_pack_name
from tests.dino.conftest import run


def test_pack_catalog():
    assert set(PACKS) == {"free", "proof"}
    assert set(PACKS["free"]["domains"]) == {"scan", "proof", "capsule"}
    assert set(PACKS["proof"]["domains"]) == {"capsule", "map", "bundle", "flight", "verify", "proof"}
    assert resolve_pack_name("pro") == "proof"
    assert resolve_pack_name("research") == "free"


def test_free_snapshot_domains(tmp_path, monkeypatch):
    lic_dir = tmp_path / ".dino"
    lic_dir.mkdir(exist_ok=True)
    monkeypatch.setattr("dino.license.LICENSE_DIR", lic_dir)
    monkeypatch.setattr("dino.license.LICENSE_PATH", lic_dir / "license.json")
    save_license(dict(DEFAULT_LICENSE))
    assert "free" in get_active_packs()
    assert not has_proof_pack()
    assert is_domain_active("scan")
    assert is_domain_active("proof")
    assert is_domain_active("capsule")
    assert not is_domain_active("map")
    assert not is_domain_active("verify")
    assert not is_domain_active("bundle")


def test_proof_unlocks_system_domains(tmp_path, monkeypatch):
    lic_dir = tmp_path / ".dino"
    lic_dir.mkdir(exist_ok=True)
    monkeypatch.setattr("dino.license.LICENSE_DIR", lic_dir)
    monkeypatch.setattr("dino.license.LICENSE_PATH", lic_dir / "license.json")
    monkeypatch.setenv("DINO_OFFLINE_LICENSE_KEYS", "test-proof-key")
    save_license(dict(DEFAULT_LICENSE))
    activate_pack("proof", key="test-proof-key")
    assert has_proof_pack()
    for d in ("capsule", "map", "bundle", "flight", "verify", "proof"):
        assert is_domain_active(d)
    assert is_domain_active("scan")


def test_proof_requires_key(tmp_path, monkeypatch):
    lic_dir = tmp_path / ".dino"
    lic_dir.mkdir(exist_ok=True)
    monkeypatch.setattr("dino.license.LICENSE_DIR", lic_dir)
    monkeypatch.setattr("dino.license.LICENSE_PATH", lic_dir / "license.json")
    monkeypatch.delenv("DINO_OFFLINE_LICENSE_KEYS", raising=False)
    monkeypatch.delenv("DINO_LICENSE_SKIP_REMOTE", raising=False)
    save_license(dict(DEFAULT_LICENSE))
    try:
        activate_pack("proof")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "team key" in str(exc).lower() or "license key" in str(exc).lower()


def test_cli_upgrade_requires_key(tmp_path, monkeypatch):
    lic_dir = tmp_path / ".dino"
    lic_dir.mkdir(exist_ok=True)
    monkeypatch.setattr("dino.license.LICENSE_DIR", lic_dir)
    monkeypatch.setattr("dino.license.LICENSE_PATH", lic_dir / "license.json")
    monkeypatch.delenv("DINO_OFFLINE_LICENSE_KEYS", raising=False)
    monkeypatch.delenv("DINO_LICENSE_SKIP_REMOTE", raising=False)
    save_license(dict(DEFAULT_LICENSE))
    code, out, err = run(["upgrade", "--pack", "proof"], json_mode=False)
    assert code == 2
    assert "team key" in (out + err).lower() or "license key" in (out + err).lower()


def test_cli_upgrade_with_offline_key(tmp_path, monkeypatch):
    lic_dir = tmp_path / ".dino"
    lic_dir.mkdir(exist_ok=True)
    monkeypatch.setattr("dino.license.LICENSE_DIR", lic_dir)
    monkeypatch.setattr("dino.license.LICENSE_PATH", lic_dir / "license.json")
    monkeypatch.setenv("DINO_OFFLINE_LICENSE_KEYS", "offline-ok")
    save_license(dict(DEFAULT_LICENSE))
    code, out, _ = run(
        ["upgrade", "--pack", "proof", "--key", "offline-ok"], json_mode=False
    )
    assert code == 0
    assert "proof" in out.lower()
    assert is_domain_active("map")


def test_free_snapshot_commands_work(tmp_path, monkeypatch):
    lic_dir = tmp_path / ".dino"
    lic_dir.mkdir(exist_ok=True)
    monkeypatch.setattr("dino.license.LICENSE_DIR", lic_dir)
    monkeypatch.setattr("dino.license.LICENSE_PATH", lic_dir / "license.json")
    save_license(dict(DEFAULT_LICENSE))

    code, out, err = run(["scan", "grammar"], json_mode=True)
    assert code == 0, err

    outdir = tmp_path / "proof_free"
    code, out, err = run(
        ["run", "--command", "echo", "free-ok", "--output-dir", str(outdir)],
        json_mode=True,
    )
    assert code == 0, f"{err}\n{out}"


def test_system_mode_gate_friendly_exit_zero(tmp_path, monkeypatch):
    lic_dir = tmp_path / ".dino"
    lic_dir.mkdir(exist_ok=True)
    monkeypatch.setattr("dino.license.LICENSE_DIR", lic_dir)
    monkeypatch.setattr("dino.license.LICENSE_PATH", lic_dir / "license.json")
    save_license(dict(DEFAULT_LICENSE))

    code, out, err = run(
        ["capsule", "doctor", "--output-dir", str(tmp_path / "c")],
        json_mode=False,
    )
    assert code == 0
    text = out + err
    assert "Proof Pack" in text
    assert "https://dino.dev/upgrade" in text
    assert "local snapshots" in text.lower()

    code, out, err = run(
        ["proof", "index", "metrics", str(tmp_path / "missing-archive")],
        json_mode=False,
    )
    assert code == 0
    assert "https://dino.dev/upgrade" in (out + err)

    code, out, err = run(
        [
            "run",
            "--export",
            str(tmp_path / "archive"),
            "--command",
            "echo",
            "gated",
            "--output-dir",
            str(tmp_path / "p"),
        ],
        json_mode=False,
    )
    assert code == 0
    assert "https://dino.dev/upgrade" in (out + err)
    assert not (tmp_path / "archive").exists()


def test_help_unchanged_visibility(tmp_path, monkeypatch):
    """Help must still list System Mode commands (no hiding)."""
    lic_dir = tmp_path / ".dino"
    lic_dir.mkdir(exist_ok=True)
    monkeypatch.setattr("dino.license.LICENSE_DIR", lic_dir)
    monkeypatch.setattr("dino.license.LICENSE_PATH", lic_dir / "license.json")
    save_license(dict(DEFAULT_LICENSE))

    code, out, err = run(["--help"], json_mode=False)
    assert code == 0
    text = out + err
    assert "Core Workflow:" in text
    assert "map" in text
    assert "bundle" in text
    assert "verify" in text
    assert "dino.dev/upgrade" not in text  # runtime gate only, not help
