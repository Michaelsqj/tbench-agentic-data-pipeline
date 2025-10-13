import shutil
import subprocess
from pathlib import Path
import sys


def _run_cli(*args):
    return subprocess.run([
        sys.executable,
        "tools/kept_back_report.py",
        *args
    ], capture_output=True, text=True)


def test_cli_exists():
    assert Path("tools/kept_back_report.py").exists(), "tools/kept_back_report.py is missing"


def test_report_lists_kept_back_packages(tmp_path):
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    shutil.copy(Path("files/logs/apt_upgrade_with_kept_back.log"), logs_dir / "apt-upgrade.log")

    result = _run_cli()
    assert result.returncode == 0, result.stderr or result.stdout

    report_path = Path("reports/kept_back_plan.md")
    assert report_path.exists(), "Report file was not created"
    report_text = report_path.read_text()

    for pkg in ["gimp", "gimp-data", "libgegl-0.0-0", "libgimp2.0"]:
        assert pkg in report_text, f"Expected {pkg} to appear in the report"
    assert "sudo apt-get --with-new-pkgs upgrade gimp gimp-data libgegl-0.0-0 libgimp2.0" in report_text
    assert "dist-upgrade" in report_text.lower(), "Report should explain when to use dist-upgrade"

    # Use override flag with clean log to ensure success path
    clean_log = tmp_path / "no_kept_back.log"
    shutil.copy(Path("files/logs/apt_upgrade_clean.log"), clean_log)
    result = _run_cli("--log-path", str(clean_log))
    assert result.returncode == 0, result.stderr or result.stdout
    clean_text = Path("reports/kept_back_plan.md").read_text()
    assert "No packages are currently held back" in clean_text


def test_missing_log_fails():
    log_path = Path("logs/apt-upgrade.log")
    if log_path.exists():
        log_path.unlink()

    result = _run_cli()
    assert result.returncode != 0, "CLI should fail when log file is absent"
    assert "apt-upgrade.log" in (result.stderr or result.stdout), "Error message should mention missing log"
