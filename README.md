<!--
Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
SPDX-License-Identifier: BSD-3-Clause
-->
# Diag-router RPM Packing

**This is the branch for CentOS 10 Stream (`c10s`)** It holds the `diag-router` RPM's spec
file and `sources` pointer, plus the CI workflows that build and publish them.

Following the Fedora/CentOS **dist-git** convention, each distro stream gets its
own branch, and the packaging files live at the branch root:

| Branch | Stream | Contents |
|---|---|---|
| `main` | — | Project README, workflow documentation, and community files. Nothing is built here. |
| **`c10s`** | CentOS 10 Stream | **This branch.** `diag-router.spec` + `sources` + workflows. |

Full workflow configuration, source-cache reference, and troubleshooting live on
[`main`](../../tree/main) — see its `README.md` and `docs/workflows.md`.

---

## Layout

```
diag-router.spec          # RPM spec for the Qualcomm diag router daemon
sources                   # dist-git checksum pointer for the qcom-diag-router prebuilt tarball
.github/workflows/        # build-on-pr.yml, pkg-release.yml
```

This RPM packages the Artifactory-published prebuilt binary tarball for the
Qualcomm diagnostic router daemon. It depends on `libdiag`, packaged in
[`qualcomm-linux/pkg-rpm-libdiag`](https://github.com/qualcomm-linux/pkg-rpm-libdiag).
The upstream binary is distributed under Qualcomm's proprietary binary license
(`Qualcomm.nologin.binaries.license`).

---

## Getting started

### Update the version

On this branch, update `Version:` and `Source0:` in `diag-router.spec` when the
upstream archive changes. Recompute the SHA512 pointer in `sources` with:

```bash
sha512sum --tag diag-router-<version>_1.el10.aarch64.tar.gz > sources
```

Keep the filename in `sources` identical to the archive filename resolved from
`Source0`; source archives are fetched from Artifactory or the lookaside cache
and are not committed to Git.

### Open a PR

`build-on-pr` fetches the tarball (from the lookaside cache, or from the spec's
`Source` URL on a cache miss), verifies the checksum, and builds the RPM.
Download it from the run's **Artifacts**.

### Release

**Actions → Release → Run workflow**, selecting this branch. A reviewer
approves the `pkg-release-approval` gate, then the RPM publishes to
Artifactory.
