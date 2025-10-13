import json
import os
import tarfile
from pathlib import Path
import subprocess

SCRIPT = Path("scripts/extract_dataset.sh")


def _create_archive(source_dir: Path, target_path: Path):
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(target_path, "w:gz") as tf:
        tf.add(source_dir, arcname="")


def test_script_exists():
    assert SCRIPT.exists(), "scripts/extract_dataset.sh is missing"
    assert SCRIPT.stat().st_mode & 0o111, "Script must be executable"


def test_successful_extraction_produces_artifacts(tmp_path):
    archive_path = Path("artifacts/media_bundle.tar.gz")
    _create_archive(Path("files/sample_dataset"), archive_path)

    if Path("staging").exists():
        for child in Path("staging").iterdir():
            if child.is_dir():
                import shutil
                shutil.rmtree(child)
            else:
                child.unlink()

    result = subprocess.run([
        "bash",
        str(SCRIPT)
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr or result.stdout

    dest = Path("staging/media")
    assert dest.exists(), "Destination directory missing"
    checksum_file = Path("staging/media_checksums.txt")
    assert checksum_file.exists(), "Checksum file missing"
    checksums = checksum_file.read_text().strip().splitlines()
    assert any("images/a.txt" in line for line in checksums)

    summary_path = Path("logs/extraction_summary.json")
    assert summary_path.exists(), "Summary JSON missing"
    summary = json.loads(summary_path.read_text())
    assert summary["archive"].endswith("media_bundle.tar.gz")
    assert summary["destination"].endswith("staging/media")
    assert summary["file_count"] >= 3
    assert summary["total_bytes"] >= sum((dest / p).stat().st_size for p in [Path("images/a.txt"), Path("images/b.txt"), Path("README.md")])

    # Ensure overriding destination works
    alternate_archive = tmp_path / "custom.tar.gz"
    _create_archive(Path("files/sample_dataset"), alternate_archive)
    result2 = subprocess.run([
        "bash",
        str(SCRIPT),
        "--archive",
        str(alternate_archive),
        "--dest",
        "staging/custom/"
    ], capture_output=True, text=True)
    assert result2.returncode == 0
    assert Path("staging/custom").exists()


def test_corrupt_archive_fails_cleanly(tmp_path):
    archive_path = Path("artifacts/media_bundle.tar.gz")
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    archive_path.write_bytes(b"not a real tarball")

    result = subprocess.run([
        "bash",
        str(SCRIPT)
    ], capture_output=True, text=True)
    assert result.returncode != 0, "Script should fail on corrupt archive"
    dest = Path("staging/media")
    assert not dest.exists() or not any(dest.iterdir()), "Destination should remain empty after failure"
