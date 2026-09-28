# Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
Name:           diag-router
Version:        1.0.3
Release:        1%{?dist}
Summary:        Qualcomm diagnostic router daemon

License:        BSD-3-Clause
URL:            https://github.com/qualcomm-linux/pkg-diag-router

Source0:        https://qartifactory-edge.qualcomm.com/artifactory/qsc_releases/software/chip/component/core-technologies.qclinux.0.0/260925.1/prebuilt_rpm/diag-router/%{name}-%{version}_1.el10.aarch64.tar.gz

# Prebuilt aarch64 ELF binary only; building on another arch would mislabel
# the RPM. The tarball ships its own prebuilt usr/lib/debug, usr/src/debug,
# and .build-id content, which %%install discards; debug_package stays
# disabled since there's no local build to pair a regenerated debuginfo with.
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
%setup -q

%build
# Prebuilt binaries only; nothing to compile.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a usr %{buildroot}/
rm -rf %{buildroot}%{_prefix}/lib/debug %{buildroot}%{_prefix}/src/debug %{buildroot}%{_prefix}/lib/.build-id

%pre
%sysusers_create_compat diag-router.conf

%post
%systemd_post diag-router.service

%preun
%systemd_preun diag-router.service

%postun
%systemd_postun_with_restart diag-router.service

%files
%license usr/share/licenses/%{name}/LICENSE
%doc usr/share/doc/%{name}/CHANGES usr/share/doc/%{name}/NOTICE usr/share/doc/%{name}/README.md
%{_bindir}/*
%{_unitdir}/diag-router.service
%{_sysusersdir}/diag-router.conf

%changelog
* Sat Sep 26 2026 Jairaj Solanki <jsolanki@qti.qualcomm.com> - 1.0.3-1
- Update to 1.0.3: upstream now publishes a "prebuilt_rpm" tarball laid out
  as an RPM payload (usr/bin, usr/lib/systemd/system, usr/share/doc/diag-router,
  usr/share/licenses/diag-router) instead of the Debian-style
  data/qcom-diag-router/arm64/usr tree; %%install/%%files updated to match,
  and the tarball's own prebuilt debuginfo/build-id tree is discarded since
  debug_package stays disabled.
* Wed Aug 19 2026 Jairaj Solanki <jsolanki@qti.qualcomm.com> - 1.0.2-1
- Initial RPM packaging, ported from the Debian packaging in
  qualcomm-linux/pkg-diag-router (qcom/ubuntu/resolute branch).
