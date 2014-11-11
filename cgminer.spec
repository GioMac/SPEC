#
# spec file for package cgminer
#

Name:           cgminer
Version:        4.7.1
Release:        3.gmc
Summary:        A BitCoin miner
License:        GPL-3.0+
Group:          Productivity/Other
Url:            http://%{name}.org/
Source0:        %{name}-%{version}.tar.gz
Source1:        start_cgminer.in
Source2:        cgminer.service.in
Patch0:         cgminer-configure.patch
Patch1:         cgminer-makefile.patch
BuildRequires:  automake
BuildRequires:  libcurl-devel
BuildRequires:  jansson-devel >= 2.5
BuildRequires:  libtool
BuildRequires:  libudev-devel
BuildRequires:  libusb-devel
BuildRequires:  ncurses-devel
BuildRequires:  pkgconfig
BuildRequires:  zlib-devel
BuildRequires:  systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Packager:       George Machitidze <giomac@gmail.com>

%define plugdev_gid 46
%define plugdev_gname plugdev

%package -n %{name}-daemon
Summary:        Daemon for %{name}
Requires:       %{name} = %{version}
%{?systemd_requires}

%description
This is a multi-threaded multi-pool FPGA and ASIC miner for bitcoin.

%description -n %{name}-daemon
This package contains a systemd daemon for %{name}.

%prep
%setup -q
%patch0
%patch1
%{__sed} 's#^__SETTINGS__$#cgminer_bin=%{_bindir}/%{name}\ncgminer_conf=%{_sysconfdir}/%{name}.conf\ncgminer_log=%{_localstatedir}/log/%{name}/%{name}.log\ncgminer_run=%{_localstatedir}/run/%{name}.pid#g' %{S:1} > start_%{name}
%{__sed} 's#^__SETTINGS__$#ExecStart=%{_sbindir}/start_%{name} start\nExecStop=%{_sbindir}/start_%{name} stop#g' %{S:2} > %{name}.service

%build
NOCONFIGURE=yes ./autogen.sh
%configure --with-udevrulesdir=%{_usr}/lib/udev/rules.d --docdir=%{_defaultdocdir}/%{name} --with-system-libusb --disable-ants1 --disable-ants2 --enable-avalon --enable-avalon2 --disable-bab --enable-bflsc --enable-bitforce --enable-bitfury --disable-bitmine_A1 --enable-blockerupter --enable-cointerra --enable-drillbit --enable-hashfast --enable-hashratio --enable-icarus --enable-klondike --disable-knc --disable-minion --enable-modminer --disable-sp10 --disable-sp30
%{__make} %{?_smp_mflags}

%install
%{__make} install DESTDIR=%{buildroot}
%{__mkdir_p} %{buildroot}%{_sbindir}
%{__mkdir_p} %{buildroot}%{_sysconfdir}
%{__mkdir_p} %{buildroot}%{_usr}/lib/udev/rules.d
%{__mkdir_p} %{buildroot}%{_unitdir}
%{__mkdir_p} %{buildroot}%{_defaultdocdir}/%{name}/bitstreams
%{__install} -m 0644 -p -t %{buildroot}%{_usr}/lib/udev/rules.d 01-%{name}.rules
%{__install} -m 0644 -p -t %{buildroot}%{_defaultdocdir}/%{name} NEWS *README
%{__install} -m 0644 -p -t %{buildroot}%{_defaultdocdir}/%{name}/bitstreams bitstreams/COPYING_fpgaminer bitstreams/README
%{__rm} -fr %{buildroot}%{_bindir}/bitstreams
%{__install} -m 0755 -p -t %{buildroot}%{_sbindir} start_%{name}
%{__install} -m 0644 -p -t %{buildroot}%{_unitdir} %{name}.service
%{__cp} -a example.conf %{name}.conf
%{__install} -m 0644 -p -t %{buildroot}%{_sysconfdir} %{name}.conf

%pre
getent group %{plugdev_gname} > /dev/null || groupadd -g %{plugdev_gid} %{plugdev_gname}

%post -n %{name}-daemon
%systemd_post %{name}.service

%preun -n %{name}-daemon
%systemd_preun %{name}.service

%postun -n %{name}-daemon
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/*
%{_usr}/lib/udev/rules.d/
%{_defaultdocdir}/%{name}/

%files -n %{name}-daemon
%defattr(-,root,root,-)
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/%{name}.conf
%{_unitdir}/

%changelog
* Tue Nov 11 2014 George Machitidze <giomac@gmail.com> 4.7.1-3
- Fedora/RHEL7 fork
* Sun Nov  9 2014 marec@detebe.org
- bumped to version 4.7.1
* Sun Nov  9 2014 marec@detebe.org
- systemd service added
* Fri Oct 17 2014 marec@detebe.org
- bumped to version 4.7.0
* Sun Sep 21 2014 marec@detebe.org
- bumped to version 4.6.1
* Sun Sep  7 2014 marec@detebe.org
- bumped to version 4.6.0
* Fri Aug  1 2014 marec@detebe.org
- bumped to version 4.5.0
* Thu Jul 17 2014 marec@karumbe.box
- bumped to version 4.4.2
* Sat Jun 21 2014 marec@detebe.org
- bumped to version 4.4.1
* Mon Jun 16 2014 marec@detebe.org
- bumped to version 4.4.0
* Tue Jun 10 2014 marec@detebe.org
- bumped to version 4.3.5
* Sun May 25 2014 marec@detebe.org
- bumped to version 4.3.4
* Sun May  4 2014 marec@detebe.org
- bumped to version 4.3.3
* Fri May  2 2014 marec@detebe.org
- bumped to version 4.3.2
* Fri Apr 18 2014 marec@detebe.org
- bumped to version 4.3.0
* Thu Apr  3 2014 marec@detebe.org
- bumped to version 4.2.3
* Sat Mar 29 2014 marec@detebe.org
- bumped to version 4.2.2
* Mon Mar 24 2014 marec@detebe.org
- bumped to version 4.2.1
* Sat Mar 22 2014 marec@detebe.org
- initial package build
