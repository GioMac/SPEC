# Dogecoin RPM spec for Fedora
# Use the other spec file for Enterprise Linux

%define _hardened_build 1
%global selinux_variants mls strict targeted

Name:           dogecoin
Version:        1.10.0
Release:        0%{?dist}
Summary:        Peer-to-peer digital currency

Group:          Applications/System
License:        MIT
URL:            http://dogecoin.com/
Source0:        https://github.com/dogecoin/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source2:	dogecoin.sysconfig
Source3:        dogecoin.service
Source4:        dogecoin.te
Source5:        dogecoin.fc
Source6:        dogecoin.if

Patch4:         dogecoin-1.10.0-fhs-paths.patch

BuildRequires:  qt-devel >= 1:4.6
BuildRequires:  qrencode-devel
BuildRequires:  openssl-compat-bitcoin-devel
BuildRequires:  miniupnpc-devel
BuildRequires:  boost-devel >= 1.47.0
BuildRequires:  db4-devel
BuildRequires:  checkpolicy
BuildRequires:  selinux-policy-devel
BuildRequires:  /usr/share/selinux/devel/policyhelp
BuildRequires:  desktop-file-utils
BuildRequires:  libdb4-cxx-devel
Requires:       qt >= 4.6
Requires:       miniupnpc
Requires:       qrencode
Requires:       boost >= 1.47.0
Requires:       openssl-compat-bitcoin-libs >= 1.0.0j


%package server
Summary:        Peer-to-peer digital currency
BuildRequires:  systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires(pre):  shadow-utils
Requires(post):         /usr/sbin/semodule, /sbin/restorecon, /sbin/fixfiles
Requires(postun):       /usr/sbin/semodule, /sbin/restorecon, /sbin/fixfiles
Requires:       selinux-policy
Requires:       policycoreutils-python
Requires:       boost >= 1.47.0
Requires:       openssl-compat-bitcoin-libs >= 1.0.0j

%package cli
Summary:        Peer-to-peer digital currency

%package -n libbitcoinconsensus
Summary:        Peer-to-peer digital currency

%description
Dogecoin is an experimental new digital currency that enables instant
payments to anyone, anywhere in the world. Bitcoin uses peer-to-peer
technology to operate with no central authority: managing transactions
and issuing money are carried out collectively by the network.

Dogecoin is also the name of the open source software which enables the
use of this currency.

This package provides Dogecoin, a user-friendly wallet manager for
personal use.


%description server
Dogecoin is an experimental new digital currency that enables instant
payments to anyone, anywhere in the world. Dogecoin uses peer-to-peer
technology to operate with no central authority: managing transactions
and issuing money are carried out collectively by the network.

This package provides dogecoind, a wallet server and command line tool
for manipulating a remote dogecoind server.


%description cli
Dogecoin is an experimental new digital currency that enables instant
payments to anyone, anywhere in the world. Dogecoin uses peer-to-peer
technology to operate with no central authority: managing transactions
and issuing money are carried out collectively by the network.

This package provides dogecoind, a wallet server and command line tool
for manipulating a remote dogecoind server.


%description -n libbitcoinconsensus
Dogecoin is an experimental new digital currency that enables instant
payments to anyone, anywhere in the world. Dogecoin uses peer-to-peer
technology to operate with no central authority: managing transactions
and issuing money are carried out collectively by the network.

This package provides dogecoind, a wallet server and command line tool
for manipulating a remote dogecoind server.


%prep
%setup -q -n %{name}-%{version}
%patch4 -p1

# Prep SELinux policy
mkdir SELinux
cp -p %{SOURCE4} %{SOURCE5} %{SOURCE6} SELinux

%build
# Build dogecoin GUI
./autogen.sh
test -d /usr/lib64/qt4/bin && \
        QMAKE=/usr/lib64/qt4/bin/qmake || \
        QMAKE=/usr/lib/qt4/bin/qmake
#$QMAKE BOOST_LIB_SUFFIX=-mt \
#        OPENSSL_INCLUDE_PATH=/opt/openssl-compat-bitcoin/include \
#        OPENSSL_LIB_PATH=/opt/openssl-compat-bitcoin/lib \
#        BDB_INCLUDE_PATH=/usr/include/libdb4 \
#        BDB_LIB_PATH=%{_libdir}/libdb4 \
#        USE_UPNP=1 \
#        USE_DBUS=1 \
#        USE_QRCODE=1 \
#        LIBS=-Wl,-rpath,/opt/openssl-compat-bitcoin/lib
%configure --enable-reduce-exports --enable-glibc-back-compat \
        PKG_CONFIG_PATH=/opt/openssl-compat-bitcoin/lib/pkgconfig \
	LIBS=-Wl,-rpath,/opt/openssl-compat-bitcoin/lib \
	CPPFLAGS="-I/usr/include/libdb-5.1 -I/opt/openssl-compat-bitcoin/include" \
	LDFLAGS="-L/opt/openssl-compat-bitcoin/lib"

make %{?_smp_mflags} CFLAGS="%{optflags}"
# Build dogecoind
#pushd src
#make -f makefile.unix \
#        %{?_smp_mflags} \
#        CFLAGS="%{optflags}" \
#        OPENSSL_INCLUDE_PATH=/opt/openssl-compat-bitcoin/include \
#        OPENSSL_LIB_PATH=/opt/openssl-compat-bitcoin/lib \
#        BDB_INCLUDE_PATH=/usr/include/libdb4 \
#        BDB_LIB_PATH=%{_libdir}/libdb4 \
#        LDFLAGS=-Wl,-rpath,/opt/openssl-compat-bitcoin/lib
#popd
# Build SELinux policy
pushd SELinux
for selinuxvariant in %{selinux_variants}
do
# FIXME: Create and debug SELinux policy
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
  mv dogecoin.pp dogecoin.pp.${selinuxvariant}
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
done
popd


# Bitcoin doesn't include a "make install" so we have to do it ourselves.
# This is just as well since everything is going into standard locations.
%install
rm -rf %{buildroot}
mkdir %{buildroot}
make install DESTDIR=%{buildroot}
cp contrib/debian/examples/dogecoin.conf dogecoin.conf.example
# Install dogecoin GUI
install -D -m755 -p src/qt/dogecoin-qt %{buildroot}%{_bindir}/dogecoin-qt
mkdir %{buildroot}%{_sbindir}
install -D -m755 -p src/dogecoind %{buildroot}%{_sbindir}/dogecoind
mkdir -p -m 755 %{buildroot}%{_datadir}/pixmaps
#install -D -m644 -p share/pixmaps/*.{png,xpm,ico} %{buildroot}%{_datadir}/pixmaps/
install -D -m644 -p share/pixmaps/bitcoin.ico %{buildroot}%{_datadir}/pixmaps/dogecoin.ico
install -D -m644 -p share/pixmaps/bitcoin64.png %{buildroot}%{_datadir}/pixmaps/dogecoin64.png
install -D -m644 -p share/pixmaps/bitcoin128.png %{buildroot}%{_datadir}/pixmaps/dogecoin128.png
install -D -m644 -p share/pixmaps/bitcoin256.png %{buildroot}%{_datadir}/pixmaps/dogecoin256.png
sed -i 's/bitcoin/dogecoin/g' contrib/debian/dogecoin-qt.desktop
install -D -m644 -p contrib/debian/dogecoin-qt.desktop %{buildroot}%{_datadir}/applications/dogecoin-qt.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/dogecoin-qt.desktop
install -D -m644 -p contrib/debian/dogecoin-qt.protocol %{buildroot}%{_datadir}/kde4/services/dogecoin-qt.protocol
install -D -m644 -p %{SOURCE3} %{buildroot}%{_unitdir}/dogecoin.service
install -d -m750 -p %{buildroot}%{_localstatedir}/lib/dogecoin
install -d -m750 -p %{buildroot}%{_sysconfdir}/dogecoin
install -D -m644 -p contrib/debian/examples/dogecoin.conf %{buildroot}%{_sysconfdir}/dogecoin/dogecoin.conf
install -D -m644 -p contrib/debian/manpages/dogecoind.1 %{buildroot}%{_mandir}/man1/dogecoind.1
install -D -m644 -p contrib/debian/manpages/dogecoin.conf.5 %{buildroot}%{_mandir}/man5/dogecoin.conf.5
install -D -m600 -p %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/dogecoin
gzip %{buildroot}%{_mandir}/man1/dogecoind.1
gzip %{buildroot}%{_mandir}/man5/dogecoin.conf.5
rm -f %{buildroot}%{_bindir}/dogecoind
# Install SELinux policy
for selinuxvariant in %{selinux_variants}
do
        install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
        install -p -m 644 SELinux/dogecoin.pp.${selinuxvariant} \
                %{buildroot}%{_datadir}/selinux/${selinuxvariant}/dogecoin.pp
done


%pre server
getent group dogecoin >/dev/null || groupadd -r dogecoin
getent passwd dogecoin >/dev/null ||
        useradd -r -g dogecoin -d /var/lib/dogecoin -s /sbin/nologin \
        -c "Dogecoin wallet server" dogecoin
exit 0


%post server
%systemd_post dogecoin.service
for selinuxvariant in %{selinux_variants}
do
        /usr/sbin/semodule -s ${selinuxvariant} -i \
                %{_datadir}/selinux/${selinuxvariant}/dogecoin.pp \
                &> /dev/null || :
done
# FIXME This is less than ideal, but until dwalsh gives me a better way...
/usr/sbin/semanage port -a -t dogecoin_port_t -p tcp 22555 # RPC
/usr/sbin/semanage port -a -t dogecoin_port_t -p tcp 22556 # P2P
/usr/sbin/semanage port -a -t dogecoin_port_t -p tcp 44555 # Test RPC
/usr/sbin/semanage port -a -t dogecoin_port_t -p tcp 44556 # Test P2P
/sbin/fixfiles -R dogecoin-server restore &> /dev/null || :
/sbin/restorecon -R %{_localstatedir}/lib/dogecoin || :
# this is a terrible way to get around some sort of bad state condition where
# systemctl keeps trying to wrap the old init script
systemctl is-enabled dogecoin.service || systemctl disable dogecoin.service


%preun server
%systemd_preun dogecoin.service


%postun server
%systemd_postun dogecoin.service
if [ $1 -eq 0 ] ; then
        # FIXME This is less than ideal, but until dwalsh gives me a better way...
        /usr/sbin/semanage port -d -p tcp 22555 # RPC
        /usr/sbin/semanage port -d -p tcp 22556 # P2P
        /usr/sbin/semanage port -d -p tcp 44555 # Test RPC
        /usr/sbin/semanage port -d -p tcp 44556 # Test P2P
        for selinuxvariant in %{selinux_variants}
        do
                /usr/sbin/semodule -s ${selinuxvariant} -r dogecoin \
                &> /dev/null || :
        done
        /sbin/fixfiles -R dogecoin-server restore &> /dev/null || :
        [ -d %{_localstatedir}/lib/dogecoin ] && \
                /sbin/restorecon -R %{_localstatedir}/lib/dogecoin \
                &> /dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc COPYING README.md dogecoin.conf.example
%{_bindir}/dogecoin-qt
%{_bindir}/test_dogecoin-qt
%{_datadir}/applications/dogecoin-qt.desktop
%{_datadir}/kde4/services/dogecoin-qt.protocol
%{_datadir}/pixmaps/*


%files server
%defattr(-,root,root,-)
%doc COPYING README.md
%dir %attr(750,dogecoin,dogecoin) %{_localstatedir}/lib/dogecoin
%dir %attr(750,dogecoin,dogecoin) %{_sysconfdir}/dogecoin
%doc SELinux/*
%{_sbindir}/dogecoind
%{_unitdir}/dogecoin.service
%config(noreplace) %{_sysconfdir}/dogecoin/dogecoin.conf
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/sysconfig/dogecoin
%{_mandir}/man1/dogecoind.1.gz
%{_mandir}/man5/dogecoin.conf.5.gz
%{_datadir}/selinux/*/dogecoin.pp

%files cli
%defattr(-,root,root,-)
%{_bindir}/dogecoin-cli
%{_bindir}/dogecoin-tx
%{_bindir}/test_dogecoin

%files -n libbitcoinconsensus
%{_includedir}/bitcoinconsensus.h
%{_libdir}/libbitcoinconsensus.a
%{_libdir}/libbitcoinconsensus.la
%{_libdir}/libbitcoinconsensus.so
%{_libdir}/libbitcoinconsensus.so.0
%{_libdir}/libbitcoinconsensus.so.0.0.0
%{_libdir}/pkgconfig/libbitcoinconsensus.pc

%changelog
* Sat Jan 30 2016 George Machitidze <giomac@gmail.com> 1.10.0-0
- Update to 1.10.0
- Corrections for sysconfig
- Systemd update
- RHEL7/Centos 7 compatibility
- Compatibility with bitcoin RPMs

* Sat Mar  8 2014 Graham Forest <vitaminmoo@wza.us> 1.5.2-2
- Cleaned up old spec features
- Replaced tabs with spaces
- Updated source0 url to actually function with spectool
- Added some vertical whitespace
- Move to systemd
- Cherry-pick valid icons, rename to avoid conflicting with bitcoin RPM

* Thu Feb 20 2014 Graham Forest <vitaminmoo@wza.us> 1.5.2-1
- Version bump

* Sat Feb  8 2014 Graham Forest <vitaminmoo@wza.us> 1.5.1-1
- Version bump

* Sun Jan 26 2014 Graham Forest <vitaminmoo@wza.us> 1.4.1-1
- Port specfile to dogecoin
- Fix date error in changelog preventing rpmlint
- Remove references to toplevel src dir
- Backport in needed contrib/ files from dogecoin 1.5 alpha
- Port patches to dogecoin paths
- Update ports for RPC/P2P (with testnet) and IRC

* Wed Jan  8 2014 Michael Hampton <bitcoin@ringingliberty.com> 0.8.6-3
- Fix typo causing a nonexistent dependency to be pulled, fixes #9

* Thu Dec 12 2013 Michael Hampton <bitcoin@ringingliberty.com> 0.8.6-2
- Boost no longer requires -mt on Fedora 20+ so omit this option and patch

* Wed Oct 16 2013 Michael Hampton <bitcoin@ringingliberty.com> 0.8.5-2
- Remove bitcoind and bitcoin-qt launcher scripts no longer used upstream
- Ship upstream example config file

* Sat Oct 05 2013 Michael Hampton <bitcoin@ringingliberty.com> 0.8.5-1
- Update for Bitcoin 0.8.5.

* Wed Sep 04 2013 Michael Hampton <bitcoin@ringingliberty.com> 0.8.4-1
- Update for Bitcoin 0.8.4.
- Strip OS X resource forks from upstream tarball.
- Use default SELinux context for /etc/bitcoin directory itself;
  fixes SELinux denial against updatedb.

* Fri Jul 05 2013 Michael Hampton <bitcoin@ringingliberty.com> 0.8.3-1
- Update for Bitcoin 0.8.3.

* Sun Jun 02 2013 Michael Hampton <bitcoin@ringingliberty.com> 0.8.2-2
- Fixed bitcoin-server dependency for new openssl packages

* Sun Jun 02 2013 Michael Hampton <bitcoin@ringingliberty.com> 0.8.2-1
- Update for Bitcoin 0.8.2.

* Fri Mar 29 2013 Michael Hampton <bitcoin@ringingliberty.com> 0.8.1-3
- Added missing openssl and boost Requires for bitcoin-server

* Sun Mar 24 2013 Michael Hampton <bitcoin@ringingliberty.com> 0.8.1-2
- Added missing SELinux dependencies
- Updated for RHEL: Now build against a private copy of Boost

* Thu Mar 21 2013 Michael Hampton <bitcoin@ringingliberty.com> 0.8.1-1
- Update for Bitcoin 0.8.1.
- Removed Patch2 (qt 4.6 compatibility) as it has been accepted upstream

* Tue Jan 29 2013 Michael Hampton <bitcoin@ringingliberty.com> 0.7.2-3
- Mass rebuild for corrected package signing key

* Mon Dec 17 2012 Michael Hampton <bitcoin@ringingliberty.com> 0.7.2-1
- Update for Bitcoin 0.7.2.
- Update for separate OpenSSL package openssl-compat-bitcoin.

* Wed Aug 22 2012 Michael Hampton <bitcoin@ringingliberty.com> 0.6.3-1
- Initial package.
