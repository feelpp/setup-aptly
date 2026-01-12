# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.5] - 2026-01-12

### Fixed
- Use full path to feelpp-apt-publish command: `.venv-publish/bin/feelpp-apt-publish`
- Reverted incorrect venv activation change from 2.2.4
- Ensures command works correctly in composite action context on self-hosted runners

## [2.2.4] - 2026-01-12

### Fixed
- Virtual environment activation: moved venv activation after all pip install operations
- Ensures feelpp-apt-publish command is available in PATH when called

## [2.2.3] - 2026-01-12

### Fixed
- Command argument order: `publish` subcommand now comes before arguments, not after
- Fixes "error: the following arguments are required: --component" when using subcommands

## [2.2.2] - 2026-01-12

### Fixed
- Publishing command now correctly passes `publish` subcommand to `feelpp-apt-publish` CLI
- Fixes "error: --keyid is required when --sign is used" when using signing parameters

## [2.2.1] - 2026-01-12

### Fixed
- CI workflow: Added aptly installation step before publishing test to fix missing aptly command error

## [2.2.0] - 2026-01-12

### Added
- Integrated `setup-uv` action for faster and more reliable Python environment setup
- Improved publishing workflow with `uv` package manager

### Changed
- Updated action to use `astral-sh/setup-uv@v6` for Python dependency installation
- Simplified Python environment setup in publishing step

## [2.1.0] - 2026-01-11

### Added
- New `auto-bump` input parameter for automatically incrementing Debian revision when package version already exists in repository
- Default behavior is `false` to maintain backward compatibility and use force-overwrite instead

### Notes
- This provides an alternative to force-overwrite for handling duplicate package versions
- Useful for development workflows where you want automatic version incrementing

## [2.0.0] - 2025-10-12

### Added
- Modern Python project structure with `pyproject.toml`
- `AGENTS.md` for development workflow documentation
- GPG signing support with `sign`, `gpg-key-id`, and `gpg-passphrase` inputs
- Automatic repository detection from `github.repository` context
- Integration with `feelpp-aptly-publisher` package
- Fast dependency management using `uv`
- Comprehensive security notes for GPG signing
- Example workflow with signing configuration

### Changed
- **BREAKING**: Removed `pages-repo` input (auto-determined from github context)
- **BREAKING**: Removed `pages-branch` input (always uses `gh-pages`)
- Migrated from legacy `scripts/aptly_publish.py` to `feelpp-aptly-publisher` package
- Updated installation process to use `uv` for Python dependencies
- Improved error handling with conditional signing validation
- Enhanced documentation with security best practices

### Fixed
- GPG signing now properly supported (was incorrectly marked as deprecated)
- Publishing step uses array arguments for proper parameter handling
- All tests updated to reflect actual inputs (not removed ones)

### Migration Guide

#### From v1 to v2

**Before (v1):**
```yaml
- uses: feelpp/setup-aptly@v1
  with:
    publish: true
    component: base
    pages-repo: https://github.com/feelpp/apt.git
    pages-branch: gh-pages
    debs-path: ..
```

**After (v2):**
```yaml
- uses: feelpp/setup-aptly@v2
  with:
    publish: true
    component: base
    # pages-repo removed (auto-detected)
    # pages-branch removed (always gh-pages)
    debs-path: ..
    apt-repo-path: apt-repo  # Path to local checkout
```

**With Signing (v2):**
```yaml
- uses: feelpp/setup-aptly@v2
  with:
    publish: true
    component: base
    sign: true  # NEW: Enable signing
    gpg-key-id: ${{ secrets.GPG_KEY_ID }}  # RESTORED
    gpg-passphrase: ${{ secrets.GPG_PASSPHRASE }}  # RESTORED (optional)
    debs-path: ..
    apt-repo-path: apt-repo
```

### Technical Details

- Minimum Python: 3.8+
- Uses `uv` for fast virtual environment and package management
- Installs `feelpp-aptly-publisher` from local checkout or PyPI
- Supports conditional signing with proper error validation
- All 9 pytest tests passing
- All 6 standalone tests passing

## [1.0.0] - 2024-xx-xx

### Added
- Initial release with aptly installation
- Basic publishing support via Python script
- Caching support
- Multi-platform support (Linux, macOS, Windows)

[2.0.0]: https://github.com/feelpp/setup-aptly/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/feelpp/setup-aptly/releases/tag/v1.0.0
