%define __os_install_post %{nil}

Name:     unifi
Summary:  Ubiquitu UniFi Controller
Version:  5.11.47
Release:  0%{dist}
Group:    Applications/System
License:  Proprietary
URL:      http://www.ubnt.com/
Source:   https://www.ubnt.com/downloads/unifi/%{version}/UniFi.unix.zip
Source1:  unifi.service
Requires: rh-mongodb34-mongodb-server java
Packager: George Machitidze <giomac@gmail.com>
AutoReq:  0
AutoReqProv: no
Requires(post): systemd-units
Requires(preun): systemd-units

%description
UniFi Controller for Linux

%prep
%setup -q -n UniFi

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/opt/%{name}/
rm -f readme.txt
rm -f bin/mongod
ln -sf /opt/rh/rh-mongodb34/root/usr/bin/mongod bin/mongod
cp -a * $RPM_BUILD_ROOT/opt/%{name}/
install -D -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_unitdir}/%{name}.service

%clean
rm -rf $RPM_BUILD_ROOT

%post
rm -rf /opt/%{name}/work
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%files
%defattr(-,root,root)
/opt/%{name}/*
%{_unitdir}/%{name}.service

%changelog
* Fri Oct 04 2019 George Machitidze <giomac@gmail.com> - 5.11.47
- Switch to SCL mongodb34
* Sun Jun 28 2015 George Machitidze <giomac@gmail.com>
- Fix for ROOT problem
* Sat Dec 17 2014 George Machitidze <giomac@gmail.com>
- Workaround for webapps ROOT issue https://github.com/GioMac/SPEC/issues/1
* Fri Jan 17 2014 George Machitidze <giomac@gmail.com>
- Initial build
