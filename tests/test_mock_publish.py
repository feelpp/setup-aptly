import pytest
import subprocess
import os
import tempfile
from pathlib import Path

def test_mock_aptly_publish_script():
    """Test that the mock aptly_publish.py script works correctly."""
    script_path = Path(__file__).parent.parent / "scripts" / "aptly_publish.py"
    
    # Create a temporary directory with mock .deb files
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        # Create a mock .deb file
        mock_deb = tmpdir_path / "test-package_1.0.0_amd64.deb"
        mock_deb.write_text("mock deb content")
        
        # Test the script with minimal args
        result = subprocess.run([
            "python3", str(script_path),
            "--component", "test-component",
            "--debs", str(tmpdir_path),
            "--pages-repo", "https://example.com/repo.git",
            "--verbose"
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert "Mock aptly_publish.py started" in result.stderr
        assert "Found 1 .deb files" in result.stderr
        assert "Mock publish completed" in result.stdout

def test_mock_aptly_publish_with_signing():
    """Test the mock script with GPG signing enabled."""
    script_path = Path(__file__).parent.parent / "scripts" / "aptly_publish.py"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        mock_deb = tmpdir_path / "test-package_1.0.0_amd64.deb"
        mock_deb.write_text("mock deb content")
        
        # Test with signing
        result = subprocess.run([
            "python3", str(script_path),
            "--component", "test-component",
            "--debs", str(tmpdir_path),
            "--pages-repo", "https://example.com/repo.git",
            "--sign",
            "--keyid", "ABCD1234",
            "--verbose"
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert "Mock: Signing repository with key ABCD1234" in result.stderr

def test_mock_aptly_publish_missing_debs():
    """Test script behavior when no .deb files are found."""
    script_path = Path(__file__).parent.parent / "scripts" / "aptly_publish.py"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Empty directory with no .deb files
        result = subprocess.run([
            "python3", str(script_path),
            "--component", "test-component", 
            "--debs", str(tmpdir),
            "--pages-repo", "https://example.com/repo.git"
        ], capture_output=True, text=True)
        
        assert result.returncode == 1
        assert "No .deb files found" in result.stderr

def test_mock_aptly_publish_missing_keyid():
    """Test script behavior when signing is enabled but no key ID provided."""
    script_path = Path(__file__).parent.parent / "scripts" / "aptly_publish.py"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        mock_deb = tmpdir_path / "test-package_1.0.0_amd64.deb"
        mock_deb.write_text("mock deb content")
        
        result = subprocess.run([
            "python3", str(script_path),
            "--component", "test-component",
            "--debs", str(tmpdir_path),
            "--pages-repo", "https://example.com/repo.git",
            "--sign"  # Missing --keyid
        ], capture_output=True, text=True)
        
        assert result.returncode == 1
        assert "GPG key ID required for signing" in result.stderr