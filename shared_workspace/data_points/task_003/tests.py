import os
import subprocess

def test_ppa_files_removed():
    """Test that the PPA list files have been removed from sources.list.d."""
    # Check that graphics-drivers PPA file is removed
    assert not os.path.exists('/etc/apt/sources.list.d/graphics-drivers-ppa.list'), \
        "graphics-drivers-ppa.list file still exists"

    # Check that libreoffice PPA file is removed
    assert not os.path.exists('/etc/apt/sources.list.d/libreoffice-ppa.list'), \
        "libreoffice-ppa.list file still exists"

def test_apt_update_succeeds():
    """Test that apt-get update runs successfully after PPA removal."""
    # This should succeed without errors after PPAs are removed
    result = subprocess.run(
        ['apt-get', 'update'],
        capture_output=True,
        text=True,
        timeout=60
    )

    # apt-get update should complete successfully
    assert result.returncode == 0, \
        f"apt-get update failed after PPA removal: {result.stderr}"

    # Check that removed PPAs don't appear in error messages
    assert 'graphics-drivers' not in result.stderr.lower(), \
        "graphics-drivers PPA still referenced in apt output"
    assert 'libreoffice' not in result.stderr.lower(), \
        "libreoffice PPA still referenced in apt output"
