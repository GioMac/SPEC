Name:           keepassx
Version:        2.0alpha4
Release:        0%{?dist}
Summary:        Cross-platform password manager
Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://keepassx.sourceforge.net
Source0:        http://download.sf.net/keepassx/keepassx-2.0-alpha4.tar.gz
BuildRequires:  qt4-devel > 4.1, libXtst-devel, ImageMagick, desktop-file-utils, libgcrypt-devel
Requires:       hicolor-icon-theme

%description
KeePassX is an application for people with extremly high demands on secure
personal data management.
KeePassX saves many different information e.g. user names, passwords, urls,
attachemts and comments in one single database. For a better management
user-defined titles and icons can be specified for each single entry.
Furthermore the entries are sorted in groups, which are customizable as well.
The integrated search function allows to search in a single group or the
complete database.
KeePassX offers a little utility for secure password generation. The password
generator is very customizable, fast and easy to use. Especially someone who
generates passwords frequently will appreciate this feature.
The complete database is always encrypted either with AES (alias Rijndael) or
Twofish encryption algorithm using a 256 bit key. Therefore the saved
information can be considered as quite safe. KeePassX uses a database format
that is compatible with KeePass Password Safe for MS Windows.

%prep
%setup -q -n keepassx-2.0-alpha4

%build
export CFLAGS=$RPM_OPT_FLAGS
export CXXFLAGS=$RPM_OPT_FLAGS
cmake -DCMAKE_INSTALL_PREFIX=/usr
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Associate KDB files
cat > x-keepass.desktop << EOF
[Desktop Entry]
Comment=
Hidden=false
Icon=keepassx.png
MimeType=application/x-keepass
Patterns=*.kdb;*.KDB
Type=MimeType
EOF
install -D -m 644 -p x-keepass.desktop  $RPM_BUILD_ROOT%{_datadir}/mimelnk/application/x-keepass.desktop
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/keepassx
mv $RPM_BUILD_ROOT/usr/lib/keepassx/libkeepassx-autotype-x11.so $RPM_BUILD_ROOT/%{_libdir}/keepassx/
rm -rf $RPM_BUILD_ROOT/usr/local

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%{_bindir}/keepassx
%{_libdir}/keepassx
%{_datadir}/keepassx
%{_datadir}/icons/hicolor/*/*/keepassx*
%{_datadir}/mimelnk/application/x-keepass.desktop

%changelog
