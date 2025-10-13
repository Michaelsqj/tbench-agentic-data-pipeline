import json
import shutil
from pathlib import Path
import subprocess

SCRIPT = Path("admin/apply_user_state.sh")


def _reset_mock_root(tmp_path: Path):
    source = Path("files/mock_root")
    target = Path("mock_root")
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)
    return target


def _write_config(text: str):
    config_path = Path("config/user_operations.yaml")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(text)


def _load_passwd(root: Path):
    passwd = {}
    for line in (root / "etc/passwd").read_text().strip().splitlines():
        parts = line.split(":")
        passwd[parts[0]] = parts
    return passwd


def test_script_exists():
    assert SCRIPT.exists(), "admin/apply_user_state.sh is missing"
    assert SCRIPT.stat().st_mode & 0o111, "Script must be executable"


def test_apply_user_state_modifies_chroot(tmp_path):
    root = _reset_mock_root(tmp_path)
    _write_config(
        "users:
"
        "  - name: analytics
"
        "    state: present
"
        "    uid: 1200
"
        "    gid: 1200
"
        "    shell: /bin/bash
"
        "    full_name: Analytics Bot
"
        "    groups: [ops]
"
        "    create_home: true
"
        "  - name: legacy
"
        "    state: absent
"
        "    remove_home: true
"
        "  - name: ops
"
        "    state: present
"
        "    shell: /bin/zsh
"
        "    full_name: Site Reliability
"
    )

    result = subprocess.run([
        "bash",
        str(SCRIPT)
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr or result.stdout

    passwd = _load_passwd(root)
    assert "analytics" in passwd
    assert passwd["analytics"][5] == "/home/analytics"
    assert Path("mock_root/home/analytics").exists()
    assert "legacy" not in passwd
    assert not Path("mock_root/home/legacy").exists()
    assert passwd["ops"][6] == "/bin/zsh"

    report = json.loads(Path("reports/user_audit.json").read_text())
    assert any(action["user"] == "analytics" for action in report["actions"])
    assert any(user["username"] == "ops" for user in report["users"])

    result2 = subprocess.run([
        "bash",
        str(SCRIPT)
    ], capture_output=True, text=True)
    assert result2.returncode == 0, result2.stderr or result2.stdout
    assert "no changes" in (result2.stdout + result2.stderr).lower()


def test_plan_only_does_not_modify(tmp_path):
    root = _reset_mock_root(tmp_path)
    original_passwd = (root / "etc/passwd").read_text()
    _write_config(
        "users:
"
        "  - name: temp
"
        "    state: present
"
        "    shell: /bin/bash
"
        "    full_name: Temp User
"
        "    create_home: true
"
    )

    result = subprocess.run([
        "bash",
        str(SCRIPT),
        "--plan-only"
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr or result.stdout
    assert (root / "etc/passwd").read_text() == original_passwd, "Plan-only should not modify passwd"

    report = json.loads(Path("reports/user_audit.json").read_text())
    assert report.get("actions"), "Report should include planned actions"
    assert all(not action.get("applied", True) for action in report["actions"])
