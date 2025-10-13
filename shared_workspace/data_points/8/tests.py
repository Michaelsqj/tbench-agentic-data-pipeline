import os
import subprocess
from pathlib import Path

SCRIPT = Path("infrastructure/setup_rootless_docker.sh")


def _write_stub(path: Path, body: str):
    path.write_text(body)
    path.chmod(0o755)


def _make_rootless_stubs(tmp_path: Path):
    stubs = tmp_path / "stubs_rootless"
    stubs.mkdir()
    log = tmp_path / "rootless_log.txt"
    _write_stub(stubs / "dockerd-rootless-setuptool.sh", f"#!/bin/bash
echo rootless setup >> {log}
exit 0
")
    _write_stub(stubs / "systemctl", "#!/bin/bash
if [ "$1" = '--user' ]; then exit 0; fi
exit 1
")
    _write_stub(stubs / "docker", f"#!/bin/bash
if [ "$1" = '--version' ]; then echo 'Docker version'; exit 0; fi
echo docker "$@" >> {log}
exit 0
")
    return stubs


def _make_group_stubs(tmp_path: Path):
    stubs = tmp_path / "stubs_group"
    stubs.mkdir()
    log = tmp_path / "group_log.txt"
    _write_stub(stubs / "systemctl", "#!/bin/bash
exit 1
")
    _write_stub(stubs / "dockerd-rootless-setuptool.sh", "#!/bin/bash
exit 1
")
    _write_stub(stubs / "docker", "#!/bin/bash
if [ "$1" = '--version' ]; then echo 'Docker version'; exit 0; fi
exit 0
")
    _write_stub(stubs / "getent", "#!/bin/bash
exit 2
")
    _write_stub(stubs / "groupadd", f"#!/bin/bash
echo groupadd '$@' >> {log}
exit 0
")
    _write_stub(stubs / "gpasswd", f"#!/bin/bash
echo gpasswd '$@' >> {log}
exit 0
")
    _write_stub(stubs / "id", "#!/bin/bash
if [ "$1" = '-nG' ]; then echo 'users'; exit 0; fi
/bin/id '$@'
")
    return stubs, log


def test_script_exists():
    assert SCRIPT.exists(), "infrastructure/setup_rootless_docker.sh is missing"
    assert SCRIPT.stat().st_mode & 0o111, "Script must be executable"


def test_rootless_setup_documented(tmp_path):
    stubs = _make_rootless_stubs(tmp_path)
    env = os.environ.copy()
    env['PATH'] = f"{stubs}:{env['PATH']}"
    env['HOME'] = str(tmp_path / 'home_rootless')
    (tmp_path / 'home_rootless').mkdir(exist_ok=True)

    result = subprocess.run([
        "bash",
        str(SCRIPT)
    ], capture_output=True, text=True, env=env)
    assert result.returncode == 0, result.stderr or result.stdout

    readiness = Path("docs/rootless_docker_readiness.md")
    assert readiness.exists(), "Readiness document missing"
    content = readiness.read_text()
    assert "rootless" in content.lower()
    assert "DOCKER_HOST" in content
    assert (Path(env['HOME']) / '.config/docker-rootless').exists(), "Rootless directory should be created"


def test_group_fallback_documented(tmp_path):
    stubs, log = _make_group_stubs(tmp_path)
    env = os.environ.copy()
    env['PATH'] = f"{stubs}:{env['PATH']}"
    env['HOME'] = str(tmp_path / 'home_group')
    (tmp_path / 'home_group').mkdir(exist_ok=True)

    result = subprocess.run([
        "bash",
        str(SCRIPT),
        "--user",
        "otherdev"
    ], capture_output=True, text=True, env=env)
    assert result.returncode == 0, result.stderr or result.stdout

    readiness = Path("docs/rootless_docker_readiness.md")
    assert readiness.exists(), "Readiness document missing"
    content = readiness.read_text()
    assert "otherdev" in content
    assert "docker group" in content.lower()
    assert log.exists(), "group operations were not logged"


def test_dry_run_records_without_changes(tmp_path):
    stubs, log = _make_group_stubs(tmp_path)
    env = os.environ.copy()
    env['PATH'] = f"{stubs}:{env['PATH']}"
    env['HOME'] = str(tmp_path / 'home_dry')
    (tmp_path / 'home_dry').mkdir(exist_ok=True)

    result = subprocess.run([
        "bash",
        str(SCRIPT),
        "--dry-run"
    ], capture_output=True, text=True, env=env)
    assert result.returncode == 0, result.stderr or result.stdout
    readiness = Path("docs/rootless_docker_readiness.md")
    assert readiness.exists()
    assert "dry-run" in (result.stdout + result.stderr).lower()
