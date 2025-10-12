# setup-aptly

Reusable GitHub Action that installs [aptly](https://www.aptly.info/) and optionally publishes Debian/Ubuntu packages to the Feel++ APT repository using the modern `feelpp-aptly-publisher` tool.

[![CI](https://github.com/feelpp/setup-aptly/workflows/CI/badge.svg)](https://github.com/feelpp/setup-aptly/actions)

## Features

- ✅ Installs aptly from official GitHub releases
- ✅ Supports Linux, macOS, and Windows runners
- ✅ Configurable version and architecture  
- ✅ Built-in caching for faster subsequent runs
- ✅ Automatic PATH configuration
- ✅ Optional APT repository publishing with **feelpp-aptly-publisher**
- ✅ Multi-component architecture support (base, feelpp, applications, ktirio)
- ✅ Automatic component preservation during updates
- ✅ Testing and validation

## What's New in v2

- 🔄 **Migrated to feelpp-aptly-publisher**: Modern Python package replacing legacy scripts
- 🎯 **Simplified inputs**: No longer need `pages-repo`, `pages-branch`, or GPG parameters
- 🏗️ **Component architecture**: Supports base/feelpp/applications/ktirio structure
- ⚡ **Faster setup**: Uses uv for dependency management
- 🔒 **Built-in recovery**: Automatically recovers aptly database from published repositories

## Usage

### Basic Installation

```yaml
- name: Setup aptly
  uses: feelpp/setup-aptly@v1
  with:
    version: '1.6.2'
```

### With Publishing (Updated for v2)

```yaml
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Checkout feelpp/apt repository
        uses: actions/checkout@v4
        with:
          repository: feelpp/apt
          ref: main
          path: apt-repo

      - name: Build packages
        run: |
          dpkg-buildpackage -us -uc -b

      - name: Publish to APT repository
        uses: feelpp/setup-aptly@v2
        with:
          publish: true
          component: base  # or feelpp, applications, ktirio
          distribution: noble
          channel: testing  # or stable, pr
          debs-path: ..
          apt-repo-path: apt-repo
```

### Component Architecture

The action supports the Feel++ 4-layer component structure:

```yaml
# External dependencies → base component
- uses: feelpp/setup-aptly@v2
  with:
    component: base
    # For: mmg, parmmg, napp, etc.

# Feel++ core → feelpp component  
- uses: feelpp/setup-aptly@v2
  with:
    component: feelpp
    # For: libfeelpp, feelpp-tools, etc.

# General applications → applications component
- uses: feelpp/setup-aptly@v2
  with:
    component: applications
    # For: feelpp-project, organ-on-chip, sepsis

# KTIRIO stack → ktirio component
- uses: feelpp/setup-aptly@v2
  with:
    component: ktirio
    # For: ktirio-urban-building, ktirio-geom, ktirio-data
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `version` | Aptly version to install | No | `1.6.2` |
| `architecture` | Target architecture | No | `amd64` |
| `cache` | Enable installation caching | No | `true` |
| `publish` | Enable APT publishing | No | `false` |
| `component` | APT component (base, feelpp, applications, ktirio) | No | `''` |
| `distribution` | Ubuntu/Debian distribution | No | `noble` |
| `channel` | Publication channel (stable, testing, pr) | No | `stable` |
| `debs-path` | Path to .deb files | No | `''` |
| `sign` | Sign the publication with GPG | No | `false` |
| `gpg-key-id` | GPG key ID for signing (required if sign=true) | No | `''` |
| `gpg-passphrase` | GPG passphrase (optional, can use GPG agent) | No | `''` |
| `apt-repo-path` | Path to feelpp/apt checkout | No | `.` |

### Removed Inputs (v2)

The following inputs are no longer needed:
- ~~`pages-repo`~~ - Automatically uses feelpp/apt via feelpp-aptly-publisher
- ~~`pages-branch`~~ - Always uses gh-pages

### GPG Signing

To sign packages with GPG:

```yaml
- name: Import GPG key
  run: |
    echo "${{ secrets.GPG_PRIVATE_KEY }}" | gpg --import
    
- name: Publish with signing
  uses: feelpp/setup-aptly@v2
  with:
    publish: true
    component: base
    sign: true
    gpg-key-id: ${{ secrets.GPG_KEY_ID }}
    gpg-passphrase: ${{ secrets.GPG_PASSPHRASE }}  # Optional if using gpg-agent
    debs-path: ..
    apt-repo-path: apt-repo
```

**Security Notes:**
- Store GPG keys and passphrases as GitHub secrets
- Consider using GPG agent instead of passphrase
- Unsigned repositories work but show warnings to users
- Signing is recommended for production (stable) channel

## Outputs

| Output | Description |
|--------|-------------|
| `aptly-version` | Installed aptly version |
| `aptly-path` | Path to aptly executable |
| `published` | Whether packages were published |
| `publication-url` | URL of published APT repository |

## Supported Platforms

- Ubuntu 24.04 (amd64, arm64)
- Ubuntu 22.04 (amd64)
- Linux runners in general
- macOS (experimental)
- Windows (experimental)

## Publishing Workflow

When `publish: true` is set, the action:

1. Validates required inputs (component, debs-path, apt-repo-path)
2. Installs `feelpp-aptly-publisher` from the apt-repo checkout
3. Uses `uv` for fast Python dependency management
4. Converts relative paths to absolute paths
5. Configures git for GitHub Actions
6. Executes `feelpp-apt-publish` with appropriate parameters
7. Automatically preserves existing components in the repository
8. Pushes changes to the gh-pages branch
9. Returns publication URL and status

### Under the Hood

The action now uses `feelpp-aptly-publisher`, which provides:
- **Database recovery**: Reconstructs aptly database from published metadata
- **Component preservation**: Maintains all existing components when adding/updating
- **Atomic operations**: All-or-nothing publishing
- **Error handling**: Clear error messages and validation

## Migration from v1 to v2

If you're using v1, update your workflows:

```diff
- uses: feelpp/setup-aptly@v1
  with:
    publish: true
    component: my-package
-   pages-repo: https://github.com/feelpp/apt.git
-   pages-branch: gh-pages
-   gpg-key-id: ${{ secrets.GPG_KEY }}
-   gpg-passphrase: ${{ secrets.GPG_PASS }}
    apt-repo-path: apt-repo

+ uses: feelpp/setup-aptly@v2
+   with:
+     publish: true
+     component: base  # Use proper component name
+     apt-repo-path: apt-repo
```

## Development

### Running Tests Locally

```bash
# Make test script executable
chmod +x test.py

# Run basic functionality tests
python3 test.py

# Or run with verbose output
python3 test.py --verbose
```

### CI Testing

The repository includes CI testing:

- ✅ Aptly installation across versions
- ✅ Caching behavior validation  
- ✅ Cross-platform compatibility
- ✅ Input validation and error handling
- ✅ Mock publishing workflow
- ✅ Integration testing
- ✅ YAML linting

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure CI passes
5. Submit a pull request

See [`action.yml`](./action.yml) for the full list of inputs and outputs.
