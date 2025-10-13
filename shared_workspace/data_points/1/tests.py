import os
import shutil
import subprocess
import zipfile
from pathlib import Path


def _write_zip(source_dir: Path, target_zip: Path):
    with zipfile.ZipFile(target_zip, "w") as zf:
        for path in source_dir.rglob("*"):
            arcname = path.relative_to(source_dir)
            if path.is_dir():
                continue
            zf.write(path, arcname)


def _prepare_release_payload(tmp_path, include_manifest=True):
    payload_dir = tmp_path / "payload"
    shutil.copytree(Path("files/release_payload"), payload_dir)
    if not include_manifest:
        (payload_dir / "manifest.json").unlink()
    target_zip = Path("artifacts/current_release.zip")
    target_zip.parent.mkdir(parents=True, exist_ok=True)
    _write_zip(payload_dir, target_zip)
    return target_zip


def test_extract_script_exists():
    script_path = Path("scripts/extract_release.sh")
    assert script_path.exists(), "Expected scripts/extract_release.sh to exist"
    assert script_path.stat().st_mode & 0o111, "Script must be executable"


def test_successful_extraction_creates_report(tmp_path):
    script_path = Path("scripts/extract_release.sh")
    assert script_path.exists(), "Script missing"

    _prepare_release_payload(tmp_path, include_manifest=True)

    result = subprocess.run([
        "bash",
        str(script_path)
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr or result.stdout

    dest_dir = Path("releases/current")
    manifest_path = dest_dir / "manifest.json"
    assert dest_dir.exists(), "Destination directory was not created"
    assert manifest_path.exists(), "Manifest was not extracted"

    report_path = Path("logs/extraction_report.txt")
    assert report_path.exists(), "logs/extraction_report.txt was not created"
    report = report_path.read_text().strip().splitlines()
    assert len(report) == 3, "Report must contain three lines"
    assert report[0].startswith("sha256:"), "SHA256 line missing"
    assert report[1].startswith("files:"), "File count line missing"
    assert report[2].startswith("destination:"), "Destination line missing"


def test_missing_manifest_causes_failure(tmp_path):
    script_path = Path("scripts/extract_release.sh")
    assert script_path.exists(), "Script missing"

    _prepare_release_payload(tmp_path, include_manifest=False)

    result = subprocess.run([
        "bash",
        str(script_path)
    ], capture_output=True, text=True)
    assert result.returncode != 0, "Script should fail when manifest.json is absent"
    assert "manifest" in (result.stderr or result.stdout).lower(), "Error should mention missing manifest"
