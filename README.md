<!--
Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
SPDX-License-Identifier: BSD-3-Clause
-->
# Package branch — CentOS 10 Stream (`c10s`)

**This is the branch you work on.** It holds the `diag-router` RPM's spec
file and `sources` pointer, plus the CI workflows that build and publish them.

Following the Fedora/CentOS **dist-git** convention, each distro stream gets its
own branch, and the packaging files live at the branch root:

| Branch | Stream | Contents |
|---|---|---|
| `main` | — | Template docs, onboarding guide, community files. Nothing is built here. |
| **`c10s`** | CentOS 10 Stream | **This branch.** `diag-router.spec` + `sources` + workflows. |

Full onboarding guide, configuration reference, and troubleshooting live on
[`main`](../../tree/main) — see its `README.md` and `docs/workflows.md`.

---

## Layout

```
diag-router.spec          # RPM spec for the Qualcomm diag router daemon
sources                   # dist-git checksum pointer for the qcom-diag-router prebuilt tarball
.github/workflows/        # build-on-pr.yml, pkg-release.yml
```

This RPM packages the same Artifactory-published prebuilt binary tarball as
the Debian packaging in
[`qualcomm-linux/pkg-diag-router`](https://github.com/qualcomm-linux/pkg-diag-router):
the daemon that routes Qualcomm diagnostic messages between the host and
modem. It depends on `libdiag`, packaged in
[`qualcomm-linux/pkg-rpm-libdiag`](https://github.com/qualcomm-linux/pkg-rpm-libdiag).

---

## Getting started

### Update the version

### Open a PR

`build-on-pr` fetches the tarball (from the lookaside cache, or from the spec's
`Source` URL on a cache miss), verifies the checksum, and builds the RPM.
Download it from the run's **Artifacts**.

### Release

**Actions → Release → Run workflow**, selecting this branch. A reviewer
approves the `pkg-release-approval` gate, then the RPM publishes to
Artifactory.
