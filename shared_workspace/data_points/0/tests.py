import csv
import os
import subprocess
from datetime import datetime
from pathlib import Path


def test_inventory_script_exists():
    script_path = Path("tools/generate_package_inventory.sh")
    assert script_path.exists(), "Expected tools/generate_package_inventory.sh to exist"
    assert script_path.stat().st_mode & 0o111, "Script must be executable"


def test_inventory_generation(tmp_path):
    script_path = Path("tools/generate_package_inventory.sh")
    assert script_path.exists(), "Script is missing"

    result = subprocess.run([
        "bash",
        str(script_path)
    ], capture_output=True, text=True)

    assert result.returncode == 0, result.stderr or result.stdout

    inventory_path = Path("artifacts/package_inventory.csv")
    assert inventory_path.exists(), "artifacts/package_inventory.csv was not created"

    with inventory_path.open() as fh:
        reader = csv.reader(fh)
        rows = list(reader)

    assert rows, "CSV should not be empty"
    header = rows[0]
    assert header == ["package", "version", "installation_state", "recorded_at"], "Unexpected CSV header"

    data_rows = rows[1:]
    assert data_rows, "CSV must contain package rows"

    recorded_times = {row[3] for row in data_rows}
    assert len(recorded_times) == 1, "All rows must share the same recorded_at timestamp"

    timestamp = recorded_times.pop()
    try:
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise AssertionError("recorded_at must be ISO-8601 UTC") from exc

    package_names = [row[0] for row in data_rows]
    assert package_names == sorted(package_names), "Packages must be sorted alphabetically"
    assert "bash" in package_names, "Expected core package 'bash' to be listed"

    bash_rows = [row for row in data_rows if row[0] == "bash"]
    assert bash_rows, "Missing metadata for bash"
    assert bash_rows[0][2] in {"manual", "auto"}, "installation_state must be manual or auto"
