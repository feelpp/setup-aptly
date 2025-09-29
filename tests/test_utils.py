"""
Test utilities for setup-aptly action testing.
"""

import os
import tempfile
import subprocess
from pathlib import Path

def create_mock_deb_package(output_dir: Path, package_name: str = "test-package", version: str = "1.0.0") -> Path:
    """Create a mock .deb package for testing."""
    
    # Create package structure
    pkg_dir = output_dir / f"{package_name}-{version}"
    debian_dir = pkg_dir / "DEBIAN" 
    debian_dir.mkdir(parents=True, exist_ok=True)
    
    # Create control file
    control_content = f"""Package: {package_name}
Version: {version}
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Test <test@example.com>
Description: Mock package for testing setup-aptly action
"""
    
    control_file = debian_dir / "control"
    control_file.write_text(control_content)
    
    # Create some dummy files
    usr_bin = pkg_dir / "usr" / "bin"
    usr_bin.mkdir(parents=True, exist_ok=True)
    (usr_bin / package_name).write_text("#!/bin/bash\necho 'Mock executable'\n")
    
    # Build the .deb package
    deb_file = output_dir / f"{package_name}_{version}_amd64.deb"
    result = subprocess.run([
        "dpkg-deb", "--build", str(pkg_dir), str(deb_file)
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"Failed to create .deb package: {result.stderr}")
    
    return deb_file

def run_action_locally(inputs: dict) -> subprocess.CompletedProcess:
    """Run the setup-aptly action locally for testing."""
    
    # This would typically invoke the action using act or similar
    # For now, we simulate action execution
    
    action_yml = Path(__file__).parent.parent / "action.yml"
    
    # Create a minimal test that validates action.yml structure
    result = subprocess.run([
        "python3", "-c", 
        "import yaml; yaml.safe_load(open(r'{}'))".format(action_yml)
    ], capture_output=True, text=True)
    
    return result

def validate_action_outputs(outputs: dict) -> bool:
    """Validate that action outputs conform to expected schema."""
    
    required_outputs = ["aptly-version", "aptly-path"]
    optional_outputs = ["published", "publication-url"]
    
    for output in required_outputs:
        if output not in outputs:
            return False
    
    return True