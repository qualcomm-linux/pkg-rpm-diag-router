# Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
Name:           diag-router
Version:        1.0.2
Release:        1%{?dist}
Summary:        Qualcomm diagnostic router daemon

License:        BSD-3-Clause
URL:            https://github.com/qualcomm-linux/pkg-diag-router
# Prebuilt binary tarball published to Artifactory (same artifact used by the
# Debian packaging in qualcomm-linux/pkg-diag-router, see its upstream.conf).
# %{name} and %{version} are NOT expanded here because the upstream tarball's
# own naming ("qcom-diag-router_<ver>_arm64") doesn't match this package's Name:.
Source0:        https://qartifactory-edge.qualcomm.com/artifactory/qsc_releases/software/chip/component/core-technologies.qclinux.0.0/260416.1/prebuilt_resolute/qcom-diag-router_1.0.2_arm64.tar.gz

# Prebuilt aarch64 ELF binary only; building on another arch would mislabel
# the RPM. Skip auto debuginfo extraction: there is no matching source tree
# for find-debuginfo to pair with this prebuilt binary.
ExclusiveArch:  aarch64
%global debug_package %{nil}

BuildRequires:  systemd-rpm-macros

Requires:       libdiag
Requires(pre):    systemd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
Daemon for routing Qualcomm diagnostic messages between the host and modem.

%prep
%setup -q -c -n %{name}-%{version}

%build
# Prebuilt binaries only; nothing to compile.

%install
rm -rf %{buildroot}
# Verified against the real tarball fetched from Source0: it ships a systemd
# unit and a sysusers.d entry (for the "diag" service user/group) alongside
# the binary, and no top-level LICENSE/README.md (Debian-style per-component
# doc/copyright file instead) — package all of what's actually there.
mkdir -p %{buildroot}
cp -a data/qcom-diag-router/arm64/usr %{buildroot}/
# %license/%doc below package copies of the same files by pulling straight
# from the source tree, so drop the originals to avoid "unpackaged file(s)".
rm -rf %{buildroot}%{_docdir}/qcom-diag-router

%pre
%sysusers_create_compat qcom-diag-router.conf

%post
%systemd_post qcom-diag-router.service

%preun
%systemd_preun qcom-diag-router.service

%postun
%systemd_postun_with_restart qcom-diag-router.service

%files
%license data/qcom-diag-router/arm64/usr/share/doc/qcom-diag-router/copyright
%doc data/qcom-diag-router/arm64/usr/share/doc/qcom-diag-router/changelog.gz
%{_bindir}/*
%{_unitdir}/qcom-diag-router.service
%{_sysusersdir}/qcom-diag-router.conf

%changelog
* Wed Aug 19 2026 Jairaj Solanki <jsolanki@qti.qualcomm.com> - 1.0.2-1
- Initial RPM packaging, ported from the Debian packaging in
  qualcomm-linux/pkg-diag-router (qcom/ubuntu/resolute branch).
