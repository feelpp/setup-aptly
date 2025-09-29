# setup-aptly

Reusable GitHub Action that installs [aptly](https://www.aptly.info/) and optionally publishes Debian/Ubuntu packages to the Feel++ APT repository (or any aptly-backed mirror).

## Usage

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
        uses: feelpp/setup-aptly@main
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

See [`action.yml`](./action.yml) for the full list of inputs and outputs.
