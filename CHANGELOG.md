# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
