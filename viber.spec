Name:          viber
Summary:       Viber Messenger
Version:       3.1.2.3
Release:       0%{dist}
Group:         Applications/Internet
License:       Proprietary
URL:           https://github.com/Emdek/otter
Source0:        %{name}.deb
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
Packager:      George Machitidze <giomac@gmail.com>
Requires:      qt5-qtbase >= 5.2.0 qt5-qtbase-gui >= 5.2.0 qt5-qtdeclarative >= 5.2.0 qt5-qtscript >= 5.2.0 qt5-qtwebkit >= 5.2.0
BuildRequires: binutils tar
ExclusiveArch: x86_64
AutoReqProv:   no

%description
  Free Text & Calls.
  More than 200 million Viber users text, call, and send photo and video messages worldwide - for free.

  Your phone number is your ID. Viber syncs with your mobile contact list, automatically detecting which of your contacts have Viber.

  Viber Desktop and the latest versions of the Viber mobile app were designed for individuals using Viber on multiple devices,
  so you can always use the app that's right for you, whether at home, in school, at the office, or on the go.

  Viber is completely free with no advertising. We value your privacy.

  Follow us for updates and news:
  Facebook - http://facebook.com/viber.
  Twitter - http://twitter.com/viber.

  Main features:
  - Text with your friends, privately or in groups
  - Make free calls with HD sound quality
  - Seamlessly transfer calls between Viber Desktop and the Viber app with one click or tap
  - Send stickers and emoticons
  - Messages are shown on all devices

%prep
%setup -cT
cp %{SOURCE0} .
ar x %{name}.deb

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
tar -xvvf data.tar.gz -C $RPM_BUILD_ROOT
chmod a+s $RPM_BUILD_ROOT/usr/share/viber/Viber
chmod a+s $RPM_BUILD_ROOT/usr/share/viber/Viber.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/*

%changelog
* Wed May 28 2014 George Machitidze <giomac@gmail.com> - 3.1.2.3
- Initial RPM build

