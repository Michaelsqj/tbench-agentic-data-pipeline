import json
import os
from pathlib import Path
import subprocess

SCRIPT = Path("deploy/install_internal_tool.sh")


def _write_stub(name: str, target_dir: Path, lines: str):
    path = target_dir / name
    path.write_text(lines)
    path.chmod(0o755)


def _setup_stubs(tmp_path: Path):
    stubs = tmp_path / "stubs"
    stubs.mkdir()
    log = tmp_path / "stub.log"
    state = tmp_path / "state"
    state.mkdir()

    _write_stub("dpkg", stubs, f"#!/bin/bash
set -e
LOG={log}
STATE={state}
CMD="$@"
echo dpkg $CMD >> $LOG
if [ "$1" = '-i' ]; then
  if [ ! -f {state/'attempted'} ]; then
    touch {state/'attempted'}
    exit 1
  fi
fi
exit 0
")

    _write_stub("apt-get", stubs, f"#!/bin/bash
echo apt-get "$@" >> {log}
exit 0
")

    _write_stub("dpkg-query", stubs, f"#!/bin/bash
echo 'internal-tool	1.4.2'
exit 0
")

    return stubs, log, state


def test_script_exists():
    assert SCRIPT.exists(), "deploy/install_internal_tool.sh is missing"
    assert SCRIPT.stat().st_mode & 0o111, "Script must be executable"


def test_install_flow_with_retry(tmp_path):
    stubs, log, state = _setup_stubs(tmp_path)
    env = os.environ.copy()
    env['PATH'] = f"{stubs}:{env['PATH']}"

    artifact = Path("artifacts/internal-tool_1.4.2.deb")
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(b"placeholder")

    reports_dir = Path("reports")
    if reports_dir.exists():
        for child in reports_dir.iterdir():
            child.unlink()
    else:
        reports_dir.mkdir()

    result = subprocess.run([
        "bash",
        str(SCRIPT)
    ], capture_output=True, text=True, env=env)
    assert result.returncode == 0, result.stderr or result.stdout

    log_lines = log.read_text().strip().splitlines()
    assert log_lines.count("dpkg -i artifacts/internal-tool_1.4.2.deb") >= 2, "dpkg -i should be attempted twice"
    assert any("apt-get install -f" in line for line in log_lines), "apt-get --fix broken should be invoked"

    status_path = Path("reports/internal_tool_status.json")
    assert status_path.exists(), "Status JSON not created"
    status = json.loads(status_path.read_text())
    assert status == {"package": "internal-tool", "version": "1.4.2", "source": "local-artifact"}

    # Second run should detect already installed
    result2 = subprocess.run([
        "bash",
        str(SCRIPT)
    ], capture_output=True, text=True, env=env)
    assert result2.returncode == 0, result2.stderr or result2.stdout


def test_missing_artifact_fails(tmp_path):
    stubs, log, state = _setup_stubs(tmp_path)
    env = os.environ.copy()
    env['PATH'] = f"{stubs}:{env['PATH']}"
    if Path("artifacts/internal-tool_1.4.2.deb").exists():
        Path("artifacts/internal-tool_1.4.2.deb").unlink()

    result = subprocess.run([
        "bash",
        str(SCRIPT)
    ], capture_output=True, text=True, env=env)
    assert result.returncode != 0, "Script should fail if artifact missing"
    message = (result.stderr or result.stdout).lower()
    assert "internal-tool_1.4.2.deb" in message
