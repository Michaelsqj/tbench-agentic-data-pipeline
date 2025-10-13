import os
import shutil
import subprocess
from pathlib import Path


SCRIPT = Path("maintenance/remove_vendor_ppa.sh")


def _make_stub_commands(target_dir: Path, log_file: Path):
    target_dir.mkdir(parents=True, exist_ok=True)
    for name in ["add-apt-repository", "ppa-purge", "apt-get", "apt-cache"]:
        script_path = target_dir / name
        script_path.write_text(f"#!/bin/bash
echo {name} "$@" >> {log_file}
exit 0
")
        script_path.chmod(0o755)


def _prepare_root(tmp_path: Path):
    root = tmp_path / "root"
    (root / "etc/apt/sources.list.d").mkdir(parents=True)
    shutil.copy(
        Path("files/etc/apt/sources.list.d/vendor-team-ubuntu-ppa-jammy.list"),
        root / "etc/apt/sources.list.d/vendor-team-ubuntu-ppa-jammy.list"
    )
    (root / "config").mkdir(parents=True)
    shutil.copy(Path("files/config/vendor_ppa.txt"), root / "config/vendor_ppa.txt")
    return root


def test_script_exists():
    assert SCRIPT.exists(), "maintenance/remove_vendor_ppa.sh is missing"
    assert SCRIPT.stat().st_mode & 0o111, "Script must be executable"


def test_run_generates_report_and_removes_list(tmp_path, monkeypatch):
    assert SCRIPT.exists(), "Script missing"

    root = _prepare_root(tmp_path)
    stubs_dir = tmp_path / "stubs"
    log_file = tmp_path / "stub.log"
    _make_stub_commands(stubs_dir, log_file)

    env = os.environ.copy()
    env["PPA_ROOT"] = str(root)
    env["PATH"] = f"{stubs_dir}:{env['PATH']}"

    result = subprocess.run([
        "bash",
        str(SCRIPT)
    ], capture_output=True, text=True, env=env)
    assert result.returncode == 0, result.stderr or result.stdout

    report_path = Path("reports/ppa_retirement_report.md")
    assert report_path.exists(), "Report not created"
    report_text = report_path.read_text()
    assert "ppa:vendor/team" in report_text
    assert "add-apt-repository --remove" in report_text
    assert "ppa-purge" in report_text

    list_path = root / "etc/apt/sources.list.d/vendor-team-ubuntu-ppa-jammy.list"
    assert not list_path.exists(), "PPA list file should be removed"

    assert log_file.exists(), "Stub commands were not invoked"
    stub_lines = log_file.read_text().strip().splitlines()
    assert any("add-apt-repository" in line for line in stub_lines)
    assert any("ppa-purge" in line for line in stub_lines)

    # Rerun should be idempotent and mention no-op
    result2 = subprocess.run([
        "bash",
        str(SCRIPT)
    ], capture_output=True, text=True, env=env)
    assert result2.returncode == 0
    report_again = report_path.read_text()
    assert "No changes necessary" in report_again


def test_missing_identifier_fails(tmp_path):
    root = tmp_path / "root"
    (root / "config").mkdir(parents=True)
    (root / "etc/apt/sources.list.d").mkdir(parents=True)

    env = os.environ.copy()
    env["PPA_ROOT"] = str(root)

    result = subprocess.run([
        "bash",
        str(SCRIPT)
    ], capture_output=True, text=True, env=env)
    assert result.returncode != 0, "Script should fail without PPA identifier"
    message = (result.stderr or result.stdout).lower()
    assert "config/vendor_ppa.txt" in message
