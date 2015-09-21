# Actually the date is the packaging date not the commit date
%global commit_date  20140319
%global commit_short f18c8f7
%global commit_long  f18c8f7204d6354220fd6754578b3daa43734e1b

Name:           wiringpi
Version:        2.3
Release:        0.%{commit_date}git%{commit_short}.rpfr18
Summary:        WiringPi is a Wiring library written in C and should be usable from C++.

License:        GPLv3
URL:            https://git.drogon.net/?p=wiringPi
#Source0:       https://git.drogon.net/?p=wiringPi;a=snapshot;h=%{commit_short};sf=tgz 
Source0:        wiringPi-%{commit_short}.tar.gz
Patch0:         wiringpi_make_fix.patch
ExclusiveArch:  armv6hl

%description
WiringPi is a Wiring library written in C and should be usable from C++.

%prep
%setup -qn wiringPi-%{commit_short}
%patch0 -p0

%build
./build

%install
rm -rf %{buildroot}

echo "[Install]"
install -m 0755 -d %{buildroot}%{_libdir}
install -m 0755 -d %{buildroot}%{_includedir}
install -m 0644 devLib/*.h %{buildroot}%{_includedir}
install -m 0755 devLib/libwiringPiDev.so.2.0 %{buildroot}%{_libdir}
install -m 0644 wiringPi/*.h %{buildroot}%{_includedir}
install -m 0755 wiringPi/libwiringPi.so.2.0 %{buildroot}%{_libdir}
echo "[GPIO Install]"
install -m 0755 -d %{buildroot}%{_bindir}
install -m 4755 gpio/gpio %{buildroot}%{_bindir}
install -m 0755 -d  %{buildroot}/usr/man/man1/
install -m 0644 gpio/gpio.1  %{buildroot}/usr/man/man1/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%_oldincludedir
%{_libdir}/*

%doc /usr/man/man1/*
%doc examples pins/pins.pdf

%changelog
* Wed Mar 18 2014 George Machitidze <giomac@gmail.com> - 2.3-0
- Build for 2.3

* Mon May 13 2013 Chris Tyler <chris@tylers.info> - 1-3.20130207git98bcd20.rpfr18
- Added scriptlets

* Fri Nov 16 2012 Andrew Greene <andrew.greene@senecacollege.ca> - 1-1
- Updated packaged version and release tags for rpfr18

* Wed Sep 17 2012 Andrew Greene <andrew.greene@senecacollege.ca> - 1.0-4
- Package updated to include new files gerthboard.h, piNes.h and wiringSerial.h

* Thu Jul 12 2012 Andrew Greene <andrew.greene@senecacollege.ca> - 1.0-3
- changed the rpm name of from raspberrypi-wiringpi to wiringpi

* Thu Jul 12 2012 Andrew Greene <andrew.greene@senecacollege.ca> - 1.0-2
- fixed the missing file lcd.h with the correct path for the examples make

* Wed Jul 11 2012 Andrew Greene <agreene@learn.senecac.on.ca> - 1.0-1
- basic install instructions copied some files to /usr/bin and /usr/lib
- added a quick hack to fix the examples make error lcd.h file not in the right location
