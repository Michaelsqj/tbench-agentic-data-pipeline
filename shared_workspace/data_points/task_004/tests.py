import subprocess

def test_hello_package_installed():
    """Test that the hello package was successfully installed."""
    # Check if hello package is installed
    result = subprocess.run(
        ['dpkg', '-l', 'hello'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, "hello package not found in dpkg"
    assert 'hello' in result.stdout, "hello package not properly installed"

    # Check that package is in 'ii' state (installed and configured)
    lines = result.stdout.strip().split('\n')
    for line in lines:
        if line.startswith('ii') and 'hello' in line:
            break
    else:
        assert False, "hello package not in installed state"

def test_hello_command_works():
    """Test that the hello command from the package works."""
    # Try to run the hello command
    result = subprocess.run(
        ['hello', '--version'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, "hello command failed to execute"
    assert 'hello' in result.stdout.lower() or 'Hello' in result.stdout, \
        "hello command output unexpected"
