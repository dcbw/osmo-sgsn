Name:           osmo-sgsn
Version:        1.13.0
Release:        1.dcbw%{?dist}
Summary:        Osmocom 3GPP Serving GPRS Support Node
License:        AGPL-3.0-or-later AND GPL-2.0-or-later

URL:            https://www.osmocom.org/projects/osmosgsn/wiki/OsmoSGSN

BuildRequires:  git gcc autoconf automake libtool doxygen systemd-devel
BuildRequires:  c-ares-devel
BuildRequires:  libasn1c-devel >= 0.9.38
BuildRequires:  libosmocore-devel >= 1.10.0
BuildRequires:  libosmo-netif-devel >= 1.6.0
BuildRequires:  libosmo-abis-devel >= 2.0.0
BuildRequires:  libosmo-sigtran-devel >= 2.1.0
BuildRequires:  osmo-ggsn-devel >= 1.13.0
BuildRequires:  osmo-hlr-devel >= 1.9.1
BuildRequires:  osmo-iuh-devel >= 1.7.0

Source0: %{name}-%{version}.tar.bz2

Requires: osmo-usergroup

%description
Osmocom implementation of the 3GPP Serving GPRS Support Node (SGSN).

%global _lto_cflags %{nil}

%prep
%autosetup -p1


%build
%global optflags %(echo %optflags | sed 's|-Wp,-D_GLIBCXX_ASSERTIONS||g')
echo "%{version}" >.tarball-version
autoreconf -fiv
%configure --enable-shared \
           --disable-static \
           --with-systemdsystemunitdir=%{_unitdir} \
           --enable-iu

# Fix unused direct shlib dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
# Remove libtool archives
find %{buildroot} -name '*.la' -exec rm -f {} \;


%check
make check

%preun
%systemd_preun osmo-gtphub.service
%systemd_preun %{name}.service

%postun
%systemd_postun osmo-gtphub.service
%systemd_postun %{name}.service

%post
%systemd_post osmo-gtphub.service
%systemd_post %{name}.service

%ldconfig_scriptlets

%files
%doc README.md
%doc %{_docdir}/%{name}
%license COPYING
%{_bindir}/*
%{_unitdir}/osmo-gtphub.service
%{_unitdir}/osmo-sgsn.service
%attr(0644,root,root) %config(missingok,noreplace) %{_sysconfdir}/osmocom/osmo-gtphub.cfg
%attr(0644,root,root) %config(missingok,noreplace) %{_sysconfdir}/osmocom/osmo-sgsn.cfg


%changelog
* Sun Jun  8 2025 Dan Williams <dan@ioncontrol.co> - 1.13.0
- Update to 1.13.0

* Sun Aug 26 2018 Cristian Balint <cristian.balint@gmail.com>
- git update release
