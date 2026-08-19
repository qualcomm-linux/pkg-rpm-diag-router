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

> **Known gap:** the upstream tarball at `Source0` lives behind
> `qartifactory-edge.qualcomm.com`, which returned 401/403 on anonymous access
> while authoring this spec — the same access gap tracked for `qmi-framework`
> in [`pkg-rpm-time-services`](https://github.com/qualcomm-linux/pkg-rpm-time-services)'s
> README. The `sources` file holds a placeholder checksum until the tarball
> is fetchable and the real one can be computed.

---

## Getting started

### Update the version

Two edits, every time:

1. Bump `Version:` in [`diag-router.spec`](diag-router.spec) (and the
   `Source0:` URL if the upstream Artifactory path changed).
2. Recompute the checksum:
   ```bash
   sha512sum --tag qcom-diag-router_<newversion>_arm64.tar.gz > sources
   ```

Commit both, open a PR against this branch, merge, then run **Release**. The
first release fetches the new upstream tarball, verifies it, and caches it back
automatically.

### Open a PR

`build-on-pr` fetches the tarball (from the lookaside cache, or from the spec's
`Source` URL on a cache miss), verifies the checksum, and builds the RPM.
Download it from the run's **Artifacts**.

### Release

**Actions → Release → Run workflow**, selecting this branch. A reviewer
approves the `pkg-release-approval` gate, then the RPM publishes to
Artifactory.
