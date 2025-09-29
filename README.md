# setup-aptly

Reusable GitHub Action that installs [aptly](https://www.aptly.info/) and optionally publishes Debian/Ubuntu packages to the Feel++ APT repository (or any aptly-backed mirror).

[![CI](https://github.com/feelpp/setup-aptly/workflows/CI/badge.svg)](https://github.com/feelpp/setup-aptly/actions)

## Features

- ✅ Installs aptly from official GitHub releases
- ✅ Supports Linux, macOS, and Windows runners
- ✅ Configurable version and architecture  
- ✅ Built-in caching for faster subsequent runs
- ✅ Automatic PATH configuration
- ✅ Optional APT repository publishing
- ✅ GPG signing support
- ✅ Testing and validation

## Usage

### Basic Installation

```yaml
- name: Setup aptly
  uses: feelpp/setup-aptly@v1
  with:
    version: '1.6.2'
```

### With Publishing

```yaml
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Checkout feelpp/apt scripts
        uses: actions/checkout@v4
        with:
          repository: feelpp/apt
          ref: main
          path: apt-scripts

      - name: Build packages
        run: |
          cmake --build build --target package

      - name: Publish to APT
        uses: feelpp/setup-aptly@v1
        with:
          publish: true
          component: organ-on-chip
          distribution: noble
          channel: testing
          debs-path: build/default/assets
          pages-repo: https://github.com/feelpp/apt.git
          apt-repo-path: apt-scripts
          gpg-key-id: ${{ secrets.APT_GPG_KEY_ID }}
          gpg-passphrase: ${{ secrets.APT_GPG_PASSPHRASE }}
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `version` | Aptly version to install | No | `1.6.2` |
| `architecture` | Target architecture | No | `amd64` |
| `cache` | Enable installation caching | No | `true` |
| `publish` | Enable APT publishing | No | `false` |
| `component` | APT component name | No | `''` |
| `distribution` | Ubuntu/Debian distribution | No | `noble` |
| `channel` | Publication channel | No | `stable` |
| `debs-path` | Path to .deb files | No | `''` |
| `pages-repo` | GitHub Pages repository URL | No | `''` |
| `pages-branch` | GitHub Pages branch | No | `gh-pages` |
| `gpg-key-id` | GPG key ID for signing | No | `''` |
| `gpg-passphrase` | GPG passphrase | No | `''` |
| `apt-repo-path` | Path to APT scripts directory | No | `.` |

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

1. Validates required inputs (component, debs-path, pages-repo)
2. Locates the aptly_publish.py script from the apt-repo-path
3. Converts relative paths to absolute paths
4. Configures git for GitHub Actions
5. Executes the publishing script with appropriate parameters
6. Handles GPG signing if credentials are provided
7. Returns publication URL and status

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
