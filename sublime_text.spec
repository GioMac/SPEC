%define buildver 3047

Name:     sublime_text
Summary:  Sublime Text editor
Version:  3
Release:  %buildver.0
Group:    Development/Tools
License:  Proproetary
URL:      http://www.sublimetext.com/
%ifarch %ix86
Source0:  %{name}_%{version}_build_%{buildver}_x32.tar.bz2
%endif
%ifarch x86_64
Source0:  %{name}_%{version}_build_%{buildver}_x64.tar.bz2
%endif
Source1:  subl
Requires: libX11 libffi libxcb libXau glib2 python3
Packager: George Machitidze <giomac@gmail.com>

%description
Sublime Text is a sophisticated text editor for code, markup and prose.

%prep
%setup -n %{name}_%{version}

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/opt/%{name}/
mkdir -p $RPM_BUILD_ROOT/%_datadir/icons/hicolor/
mkdir -p $RPM_BUILD_ROOT/%_datadir/applications/

cp -a * $RPM_BUILD_ROOT/opt/%{name}/
mv $RPM_BUILD_ROOT/opt/%{name}/Icon/* $RPM_BUILD_ROOT/%_datadir/icons/hicolor/
mv $RPM_BUILD_ROOT/opt/%{name}/%{name}.desktop $RPM_BUILD_ROOT/%_datadir/applications/
install -D -p -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/%{_bindir}/subl

%clean
rm -rf $RPM_BUILD_ROOT

%files 
/opt/%{name}/*
%_bindir/*
%_datadir/*

%changelog
* Sat Nov 09 2013 George Machitidze <giomac@gmail.com> 3-3047.0
- Initial RPM

