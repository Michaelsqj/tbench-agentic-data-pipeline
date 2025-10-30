import os
import subprocess

def test_data_archive_extracted_to_directory():
    """Test that data_archive.zip was extracted to /root/extracted/ directory."""
    # Check that the extracted directory exists
    assert os.path.exists('/root/extracted'), \
        "Target directory /root/extracted/ was not created"

    # Check that the file was extracted
    assert os.path.exists('/root/extracted/project_data.txt'), \
        "File project_data.txt not found in /root/extracted/"

    # Verify file content
    with open('/root/extracted/project_data.txt', 'r') as f:
        content = f.read()
        assert 'Project configuration data' in content, \
            "Extracted file content is incorrect"

def test_backup_extracted_to_current_directory():
    """Test that backup.zip was extracted to current directory."""
    # The file should be in /root/ (working directory)
    assert os.path.exists('/root/config.txt'), \
        "File config.txt not found in /root/ directory"

    # Verify file content
    with open('/root/config.txt', 'r') as f:
        content = f.read()
        assert 'database_host' in content, \
            "Extracted file content is incorrect"

def test_unzip_utility_installed():
    """Test that unzip utility is installed and functional."""
    result = subprocess.run(['which', 'unzip'], capture_output=True, text=True)
    assert result.returncode == 0, \
        "unzip utility is not installed or not in PATH"
