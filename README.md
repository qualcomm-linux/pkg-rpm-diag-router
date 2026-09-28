# Diag-router RPM Packing

RPM packaging for Qualcomm's diagnostic router daemon on CentOS 10 Stream.
The `diag-router` daemon routes Qualcomm diagnostic messages between the host
and modem.

This repository follows the Fedora/CentOS dist-git model: documentation and
workflow entry points live on `main`, while the package definition lives on the
`c10s` branch.

## Package

The current package is `diag-router` 1.0.3:

| Property | Value |
|---|---|
| Target stream | CentOS 10 Stream (`c10s`) |
| Architecture | `aarch64` only |
| Package type | Prebuilt binary RPM; no local compilation |
| Runtime dependency | `libdiag` |
| Service integration | `diag-router.service` and `diag-router.conf` |
| License | Qualcomm.nologin.binaries.license|

The upstream archive is already arranged as an RPM payload. The package
installs the daemon, its systemd service and sysusers configuration,
documentation, and license. The archive also contains prebuilt debug/build-id
files; these are intentionally discarded because this package does not
regenerate or publish debuginfo.

## Repository layout

| Path | Purpose |
|---|---|
| [`c10s/diag-router.spec`](https://github.com/qualcomm-linux/pkg-rpm-diag-router/blob/c10s/diag-router.spec) | RPM metadata, source URL, install rules, and file list |
| [`c10s/sources`](https://github.com/qualcomm-linux/pkg-rpm-diag-router/blob/c10s/sources) | SHA512 checksum and filename for the source archive |
| [`build-on-pr.yml`](.github/workflows/build-on-pr.yml) | Pull-request build validation |
| [`pkg-release.yml`](.github/workflows/pkg-release.yml) | Manual RPM release workflow |
| [`docs/workflows.md`](docs/workflows.md) | Detailed reusable-workflow and lookaside-cache documentation |

### Branches

- **`main`** — project documentation, workflow callers, and community files.
- **`c10s`** — the CentOS 10 Stream package branch. Package changes should be
  made here; it contains `diag-router.spec` and `sources` at the branch root.

## Source archive

The package consumes the prebuilt archive published in Qualcomm Artifactory:

```text
https://qartifactory-edge.qualcomm.com/artifactory/qsc_releases/software/chip/component/core-technologies.qclinux.0.0/260925.1/prebuilt_rpm/diag-router/diag-router-1.0.3_1.el10.aarch64.tar.gz
```

The tarball is not committed to Git. Its filename and SHA512 digest are tracked
in [`c10s/sources`](https://github.com/qualcomm-linux/pkg-rpm-diag-router/blob/c10s/sources).
The PR and release workflows resolve the archive from the lookaside cache when
available; on a cache miss they fetch the URL from `Source0` in the spec and
verify it against `sources`. Release builds can cache a verified upstream
archive for subsequent builds.

## Build and release

### Pull-request build

Open a pull request against `c10s` for package changes. The
[`Build on PR`](.github/workflows/build-on-pr.yml) workflow:

1. resolves the archive from the lookaside cache or `Source0`;
2. verifies its SHA512 checksum;
3. builds the RPM with the shared `qcom-rpm-utils` workflow; and
4. uploads the resulting RPM as a workflow artifact.

The workflow is read-only with respect to publishing. It requires the
`SRC_TARBALL_CACHE_BASE_URL` Actions variable and access to the shared ARM64
runner/build infrastructure.

### Release

After the `c10s` change is merged, run
[`Release`](.github/workflows/pkg-release.yml) manually from the Actions tab.
The release workflow builds the package, caches a verified source archive on a
cache miss, and publishes the RPM to the configured Artifactory repository
after the `pkg-release-approval` environment gate is approved.

See [`docs/workflows.md`](docs/workflows.md) for the full cache layout,
required GitHub configuration, credentials, and troubleshooting guidance.

## Updating the package

Make package updates on `c10s`:

1. Update `Version:` and, when necessary, the `Source0` URL in
   [`diag-router.spec`](https://github.com/qualcomm-linux/pkg-rpm-diag-router/blob/c10s/diag-router.spec).
2. Fetch the matching upstream archive, for example
   `diag-router-<version>_1.el10.aarch64.tar.gz`.
3. Regenerate the checksum pointer:
   ```bash
   sha512sum --tag diag-router-<version>_1.el10.aarch64.tar.gz > sources
   ```
4. Commit the spec and `sources`, then open a pull request against `c10s`.
5. After the PR build passes and the change is merged, run the manual Release
   workflow.

Keep the filename in `sources` identical to the filename resolved from the
spec's `Source0`. Do not commit source archives to the repository.
