%define __os_install_post %{nil}

Name:     unifi
Summary:  Ubiquitu UniFi Controller
Version:  3.1.6b
Release:  0
Group:    Applications/System
License:  Proprietary
URL:      http://www.ubnt.com/
Source:   UniFi.unix.zip
Source1:  unifi.service
Requires: mongodb-server java
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
cp -a * $RPM_BUILD_ROOT/opt/%{name}/
install -D -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_unitdir}/%{name}.service

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%files
%defattr(-,root,root)
/opt/%{name}/*
%{_unitdir}/%{name}.service

%changelog
* Fri Jan 17 2014 George Machitidze <giomac@gmail.com>
- Initial build


