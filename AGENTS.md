# AGENTS.md - Development and Release Process

This document provides guidelines for AI agents and developers working on the setup-aptly action.

## Project Overview

**setup-aptly** is a GitHub Action that installs aptly package manager and publishes Debian packages to the Feel++ APT repository using `feelpp-aptly-publisher`.

### Key Components

1. **action.yml** - GitHub Action definition
2. **pyproject.toml** - Python project configuration and dependencies
3. **scripts/aptly_publish.py** - Legacy publish script (deprecated, kept for backward compatibility)
4. **tests/** - Test suite
5. **README.md** - User documentation

## Development Process

### 1. Environment Setup

Always use uv for dependency management:

```bash
# Create virtual environment
uv venv

# Activate it
source .venv/bin/activate

# Install dependencies (including test dependencies)
uv pip install -e ".[test]"
```

### 2. Making Changes

When modifying the action:

1. **Update action.yml** - Main action logic
2. **Update pyproject.toml** - If dependencies change
3. **Update README.md** - If usage changes
4. **Update tests/** - Add/modify tests for new functionality
5. **Update CHANGELOG.md** - Document changes (if exists)

### 3. Testing

Always test before committing:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_action.py

# Run with verbose output
pytest -v

# Run and show print statements
pytest -s
```

### 4. Pre-commit Checklist

Before committing changes:

- [ ] All tests pass: `pytest`
- [ ] Code is formatted: `ruff format .` (if using ruff)
- [ ] No lint errors: `ruff check .` (if using ruff)
- [ ] Dependencies are updated in pyproject.toml
- [ ] README.md reflects any usage changes
- [ ] AGENTS.md is updated if process changes

### 5. Commit and Push

```bash
# Check what's changed
git status
git diff

# Add changes
git add action.yml pyproject.toml README.md tests/ AGENTS.md

# Commit with descriptive message
git commit -m "feat: update to use feelpp-aptly-publisher v1.2.0"

# Push to origin
git push origin main
```

### 6. Release Process

After changes are tested and pushed:

1. **Tag the release:**
   ```bash
   git tag -a v1.1.0 -m "Release v1.1.0: Updated to use feelpp-aptly-publisher"
   git push origin v1.1.0
   ```

2. **Update major version tag** (optional, for convenience):
   ```bash
   git tag -fa v1 -m "Update v1 to v1.1.0"
   git push origin v1 --force
   ```

3. **Create GitHub release:**
   - Go to https://github.com/feelpp/setup-aptly/releases/new
   - Select the tag (v1.1.0)
   - Title: "v1.1.0 - Feature description"
   - Description: List changes, breaking changes, and migration notes

## Key Dependencies

### Runtime Dependencies

- **pyyaml** - YAML parsing for action configuration
- **requests** - HTTP requests for downloading aptly
- **feelpp-aptly-publisher** - Core publishing tool (v1.2.0+)

### Test Dependencies

- **pytest** - Test framework
- **pytest-mock** - Mocking support

## Action Inputs

The action accepts these inputs (see action.yml for full details):

- `version` - Aptly version to install (default: 1.6.2)
- `architecture` - System architecture (default: amd64)
- `cache` - Enable caching (default: true)
- `publish` - Whether to publish packages (default: false)
- `component` - APT component (base/feelpp/applications/ktirio)
- `distribution` - Debian distribution (default: noble)
- `channel` - Publication channel (stable/testing/pr)
- `debs-path` - Path to .deb files
- `apt-repo-path` - Path to feelpp/apt checkout

## Testing Guidelines

### Unit Tests

Located in `tests/test_*.py`:

- **test_action.py** - Action input validation
- **test_mock_publish.py** - Publishing logic
- **test_utils.py** - Utility functions

### Integration Tests

Mark with `@pytest.mark.integration`:

```python
@pytest.mark.integration
def test_full_publish_workflow():
    # Test complete publishing workflow
    pass
```

Run only unit tests:
```bash
pytest -m "not integration"
```

### Mock Strategy

- Mock external calls (aptly commands, git operations)
- Use `pytest-mock` fixtures
- Don't make actual network requests in tests
- Create temporary directories for file operations

## Common Tasks

### Update feelpp-aptly-publisher Version

1. Update pyproject.toml:
   ```toml
   dependencies = [
       "feelpp-aptly-publisher>=1.3.0",
   ]
   ```

2. Update README.md with new features

3. Test with new version:
   ```bash
   uv pip install -e ".[test]"
   pytest
   ```

4. Commit and release

### Add New Input Parameter

1. Update action.yml:
   ```yaml
   inputs:
     new-param:
       description: 'Description of new parameter'
       required: false
       default: 'default-value'
   ```

2. Update action logic to use the parameter

3. Update README.md with new usage example

4. Add tests for new parameter

### Fix a Bug

1. Write a failing test that reproduces the bug
2. Fix the bug
3. Verify test now passes
4. Add regression test to prevent future breakage
5. Commit with "fix:" prefix

## Troubleshooting

### Tests Fail Due to Missing Dependencies

```bash
# Reinstall dependencies
uv pip install -e ".[test]"
```

### aptly Not Found in Tests

The test suite mocks aptly calls, so actual aptly installation is not required for unit tests. Integration tests may require aptly.

### Import Errors

Ensure virtual environment is activated:
```bash
source .venv/bin/activate
```

## Version Strategy

We use semantic versioning (SemVer):

- **MAJOR** (v2.0.0) - Breaking changes to action inputs/outputs
- **MINOR** (v1.1.0) - New features, backward compatible
- **PATCH** (v1.0.1) - Bug fixes, backward compatible

### Version Tags

- `v1.0.0` - Specific version
- `v1` - Rolling tag pointing to latest v1.x.x
- `main` - Development branch

Users can reference:
- `uses: feelpp/setup-aptly@v1` - Automatic updates within v1
- `uses: feelpp/setup-aptly@v1.0.0` - Pin to specific version
- `uses: feelpp/setup-aptly@main` - Latest development (not recommended)

## CI/CD Integration

The action is used in workflows like this:

```yaml
jobs:
  publish:
    runs-on: ubuntu-24.04
    steps:
    - name: Checkout APT repo
      uses: actions/checkout@v4
      with:
        repository: feelpp/apt
        path: apt-repo
    
    - name: Setup aptly and publish
      uses: feelpp/setup-aptly@v1
      with:
        publish: true
        component: base
        channel: testing
        distribution: noble
        debs-path: .
        apt-repo-path: apt-repo
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│ GitHub Action (action.yml)                              │
│                                                          │
│ 1. Install aptly from GitHub releases                   │
│ 2. Cache installation                                   │
│ 3. If publish=true:                                     │
│    ├─ Install feelpp-aptly-publisher (via uv)          │
│    ├─ Run feelpp-apt-publish command                   │
│    └─ Publish to feelpp/apt gh-pages                   │
└─────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│ feelpp-aptly-publisher (Python package)                 │
│                                                          │
│ - Multi-component repository management                 │
│ - Preserves existing components                         │
│ - Handles empty component bootstrapping                 │
│ - Automatic git operations                              │
└─────────────────────────────────────────────────────────┘
```

## Links

- **Main Repo**: https://github.com/feelpp/setup-aptly
- **APT Repo**: https://github.com/feelpp/apt
- **Publisher**: https://github.com/feelpp/apt (Python package)
- **Documentation**: https://github.com/feelpp/apt/blob/main/CI_CD_GUIDE.md

## Migration Notes

### From Old Python Script to feelpp-aptly-publisher

**Old way** (deprecated):
- Used `scripts/aptly_publish.py` directly
- Required `pages-repo` and `pages-branch` inputs
- Manual git operations

**New way** (current):
- Uses `feelpp-aptly-publisher` package
- Automatic GitHub Pages handling
- Simplified inputs (no pages-repo needed)
- Better component preservation
- Empty component support

**Action Changes**:
- Removed: `pages-repo`, `pages-branch`, `gpg-key-id`, `gpg-passphrase` inputs
- Added: Automatic `feelpp-aptly-publisher` installation
- Updated: Publishing logic to use `feelpp-apt-publish` command

## Maintenance Schedule

- **Monthly**: Check for aptly updates
- **Quarterly**: Update dependencies in pyproject.toml
- **Annually**: Review and update documentation
- **As needed**: Bug fixes, feature requests

## Contact

For questions or issues:
- Open an issue: https://github.com/feelpp/setup-aptly/issues
- Feel++ discussions: https://github.com/feelpp/feelpp/discussions
