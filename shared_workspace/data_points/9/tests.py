import os
from pathlib import Path
import subprocess

SCRIPT = Path("runtime/upgrade_node.sh")


def _write_stub(path: Path, body: str):
    path.write_text(body)
    path.chmod(0o755)


def _setup_node_stubs(tmp_path: Path, active_version: str = "v18.17.1"):
    stubs = tmp_path / "node_stubs"
    stubs.mkdir()
    log = tmp_path / "node_stub.log"

    _write_stub(stubs / "npm", f"#!/bin/bash
if [ "$1" = '--version' ]; then echo '9.0.0'; exit 0; fi
if [ "$1" = 'list' ]; then exit 1; fi
if [ "$1" = 'install' ]; then echo npm install '$@' >> {log}; exit 0; fi
echo npm '$@' >> {log}
exit 0
")
    _write_stub(stubs / "n", f"#!/bin/bash
echo n '$@' >> {log}
if [ "$1" = 'which' ]; then echo '/usr/local/bin/node'; exit 0; fi
exit 0
")
    _write_stub(stubs / "node", f"#!/bin/bash
if [ "$1" = '--version' ]; then echo '{active_version}'; exit 0; fi
exit 0
")
    return stubs, log


def test_script_exists():
    assert SCRIPT.exists(), "runtime/upgrade_node.sh is missing"
    assert SCRIPT.stat().st_mode & 0o111, "Script must be executable"


def test_upgrade_writes_log(tmp_path):
    stubs, log = _setup_node_stubs(tmp_path)
    env = os.environ.copy()
    env['PATH'] = f"{stubs}:{env['PATH']}"

    config_path = Path("config/node_version.txt")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text("18.17.1
")

    result = subprocess.run([
        "bash",
        str(SCRIPT)
    ], capture_output=True, text=True, env=env)
    assert result.returncode == 0, result.stderr or result.stdout

    log_path = Path("reports/node_upgrade.log")
    assert log_path.exists(), "node_upgrade.log not created"
    contents = log_path.read_text()
    assert "18.17.1" in contents
    assert "npm version" in contents.lower() or "npm --version" in contents

    assert log.exists(), "stub log missing"
    stub_lines = log.read_text()
    assert "npm install -g n" in stub_lines or "npm install" in stub_lines
    assert "n 18.17.1" in stub_lines

    # Test rollback path with cached version missing
    result2 = subprocess.run([
        "bash",
        str(SCRIPT),
        "--rollback",
        "16.20.0"
    ], capture_output=True, text=True, env=env)
    assert result2.returncode != 0, "Rollback with missing cache should fail"
    assert "16.20.0" in (result2.stderr or result2.stdout)


def test_missing_version_file_fails(tmp_path):
    if Path("config/node_version.txt").exists():
        Path("config/node_version.txt").unlink()

    stubs, log = _setup_node_stubs(tmp_path)
    env = os.environ.copy()
    env['PATH'] = f"{stubs}:{env['PATH']}"

    result = subprocess.run([
        "bash",
        str(SCRIPT)
    ], capture_output=True, text=True, env=env)
    assert result.returncode != 0, "Script should fail without version file"
    message = (result.stderr or result.stdout).lower()
    assert "config/node_version.txt" in message
