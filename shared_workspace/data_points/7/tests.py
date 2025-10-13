import csv
import os
from pathlib import Path
import subprocess

SCRIPT = Path("reports/summarize_storage.sh")


def _make_dir_with_size(path: Path, size_kb: int):
    path.mkdir(parents=True, exist_ok=True)
    file_path = path / "blob.bin"
    with file_path.open("wb") as fh:
        fh.write(b"0" * size_kb * 1024)


def _write_config(rows):
    config_path = Path("config/storage_targets.csv")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with config_path.open("w") as fh:
        fh.write("path,quota_gb
")
        for path, quota in rows:
            fh.write(f"{path},{quota}
")


def test_script_exists():
    assert SCRIPT.exists(), "reports/summarize_storage.sh is missing"
    assert SCRIPT.stat().st_mode & 0o111, "Script must be executable"


def test_summary_and_alerts_created(tmp_path):
    data_root = Path("workspace_data")
    _make_dir_with_size(data_root / "team_a", 512)
    _make_dir_with_size(data_root / "team_b", 128)
    _make_dir_with_size(data_root / "team_a" / "sub1", 256)
    _make_dir_with_size(data_root / "team_a" / "sub2", 128)
    _make_dir_with_size(data_root / "team_a" / "sub3", 32)

    _write_config([
        (str(data_root / "team_a"), 0.4),
        (str(data_root / "team_b"), 0.5)
    ])

    env = os.environ.copy()
    env["MAX_DEPTH"] = "2"

    result = subprocess.run([
        "bash",
        str(SCRIPT)
    ], capture_output=True, text=True, env=env)
    assert result.returncode == 0, result.stderr or result.stdout

    summary_path = Path("reports/storage_summary.tsv")
    assert summary_path.exists(), "Summary TSV missing"
    with summary_path.open() as fh:
        reader = list(csv.DictReader(fh, delimiter='	'))
    assert reader[0]['path'].endswith('team_a')
    assert float(reader[0]['quota_gb']) == 0.4

    alerts_path = Path("reports/storage_alerts.md")
    assert alerts_path.exists(), "Alerts markdown missing"
    alerts = alerts_path.read_text()
    assert "team_a" in alerts and "over by" in alerts
    assert "sub1" in alerts


def test_missing_path_triggers_error():
    _write_config([
        ("does/not/exist", 0.1)
    ])

    result = subprocess.run([
        "bash",
        str(SCRIPT)
    ], capture_output=True, text=True)
    assert result.returncode != 0, "Script should fail when a path is missing"
    message = (result.stderr or result.stdout).lower()
    assert "does/not/exist" in message
