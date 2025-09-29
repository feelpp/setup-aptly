import pytest
import yaml
from pathlib import Path
from tests.test_utils import run_action_locally, validate_action_outputs

def test_action_yml_structure():
    """Test that action.yml has the correct structure."""
    action_yml = Path(__file__).parent.parent / "action.yml"
    
    with open(action_yml) as f:
        action = yaml.safe_load(f)
    
    # Test required fields
    assert "name" in action
    assert "description" in action
    assert "runs" in action
    assert "inputs" in action
    assert "outputs" in action
    
    # Test runs section
    runs = action["runs"]
    assert runs["using"] == "composite"
    assert "steps" in runs
    assert len(runs["steps"]) > 0
    
    # Test that all steps have required fields
    for step in runs["steps"]:
        assert "name" in step
        # Only shell steps need shell and run fields
        if "uses" not in step:  # This is a shell step
            assert "shell" in step
            assert "run" in step

def test_action_inputs():
    """Test that action inputs are properly defined."""
    action_yml = Path(__file__).parent.parent / "action.yml"
    
    with open(action_yml) as f:
        action = yaml.safe_load(f)
    
    inputs = action["inputs"]
    
    # Test required inputs exist
    required_inputs = ["version", "architecture", "cache"]
    for inp in required_inputs:
        assert inp in inputs
        assert "description" in inputs[inp]
    
    # Test publishing inputs exist when needed
    publishing_inputs = ["publish", "component", "debs-path", "pages-repo"]
    for inp in publishing_inputs:
        assert inp in inputs

def test_action_outputs():
    """Test that action outputs are properly defined."""
    action_yml = Path(__file__).parent.parent / "action.yml"
    
    with open(action_yml) as f:
        action = yaml.safe_load(f)
    
    outputs = action["outputs"]
    
    # Test required outputs exist
    required_outputs = ["aptly-version", "aptly-path", "published", "publication-url"]
    for output in required_outputs:
        assert output in outputs
        assert "description" in outputs[output]
        assert "value" in outputs[output]

def test_action_yaml_syntax():
    """Test that action.yml is valid YAML."""
    action_yml = Path(__file__).parent.parent / "action.yml"
    
    # This should not raise an exception
    with open(action_yml) as f:
        yaml.safe_load(f)

def test_readme_structure():
    """Test that README.md has expected sections."""
    readme_path = Path(__file__).parent.parent / "README.md"
    
    with open(readme_path) as f:
        content = f.read()
    
    # Test for expected sections
    expected_sections = [
        "# setup-aptly",
        "## Features", 
        "## Usage",
        "## Inputs",
        "## Outputs",
        "## Development"
    ]
    
    for section in expected_sections:
        assert section in content, f"Missing section: {section}"