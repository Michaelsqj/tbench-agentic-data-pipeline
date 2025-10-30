import os
import subprocess

def test_package_list_file_created():
    """Test that the package list file was created at the correct location."""
    assert os.path.exists('/root/installed_packages.txt'), \
        "Package list file not found at /root/installed_packages.txt"

    # Check that file is not empty
    with open('/root/installed_packages.txt', 'r') as f:
        content = f.read().strip()
        assert len(content) > 0, "Package list file is empty"

    # Check that it contains multiple lines (multiple packages)
    lines = content.split('\n')
    assert len(lines) >= 10, f"Expected at least 10 packages, found {len(lines)}"

def test_package_list_excludes_deinstall():
    """Test that the package list excludes deinstalled packages."""
    with open('/root/installed_packages.txt', 'r') as f:
        content = f.read()

    # Should not contain deinstall status
    assert 'deinstall' not in content.lower(), \
        "Package list contains deinstalled packages"

    # Should contain expected system packages
    expected_packages = ['bash', 'coreutils']
    for pkg in expected_packages:
        assert pkg in content.lower(), \
            f"Expected system package '{pkg}' not found in package list"
