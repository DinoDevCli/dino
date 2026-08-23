"""Pack gating for the live dino CLI."""

from __future__ import annotations

from dino.license import DEFAULT_LICENSE, activate_pack, get_active_packs, is_domain_active, save_license
from dino.packs import PACKS, resolve_pack_name
from tests.dino.conftest import run


def test_pack_catalog():
    assert set(PACKS) == {"free", "proof"}
    assert PACKS["free"]["domains"] == ["scan"]
    assert set(PACKS["proof"]["domains"]) == {"capsule", "map", "bundle", "flight", "verify", "proof"}
    assert resolve_pack_name("pro") == "proof"
    assert resolve_pack_name("research") == "free"


def test_free_default_locks_proof(tmp_path, monkeypatch):
    lic_dir = tmp_path / ".dino"
    lic_dir.mkdir(exist_ok=True)
    monkeypatch.setattr("dino.license.LICENSE_DIR", lic_dir)
    monkeypatch.setattr("dino.license.LICENSE_PATH", lic_dir / "license.json")
    save_license(dict(DEFAULT_LICENSE))
    assert "free" in get_active_packs()
    assert is_domain_active("scan")
    assert not is_domain_active("capsule")
    assert not is_domain_active("verify")


def test_proof_unlocks_flagship(tmp_path, monkeypatch):
    lic_dir = tmp_path / ".dino"
    lic_dir.mkdir(exist_ok=True)
    monkeypatch.setattr("dino.license.LICENSE_DIR", lic_dir)
    monkeypatch.setattr("dino.license.LICENSE_PATH", lic_dir / "license.json")
    monkeypatch.setenv("DINO_OFFLINE_LICENSE_KEYS", "test-proof-key")
    save_license(dict(DEFAULT_LICENSE))
    activate_pack("proof", key="test-proof-key")
    for d in ("capsule", "map", "bundle", "flight", "verify", "proof"):
        assert is_domain_active(d)
    assert is_domain_active("scan")  # free always on


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
    assert is_domain_active("capsule")


def test_cli_packs_and_lock(tmp_path, monkeypatch):
    lic_dir = tmp_path / ".dino"
    lic_dir.mkdir(exist_ok=True)
    monkeypatch.setattr("dino.license.LICENSE_DIR", lic_dir)
    monkeypatch.setattr("dino.license.LICENSE_PATH", lic_dir / "license.json")
    save_license(dict(DEFAULT_LICENSE))

    code, out, _ = run(["packs"], json_mode=False)
    assert code == 0
    assert "proof" in out
    assert "scan" in out

    code, out, _ = run(["capsule", "doctor", "--output-dir", str(tmp_path / "c")], json_mode=True)
    assert code == 2
    assert "locked" in out.lower() or "pack_locked" in out.lower()
