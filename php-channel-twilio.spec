%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global channelname twilio.github.io/pear

Name:           php-channel-twilio
Version:        0.1
Release:        0%{?dist}
Summary:        Adds the Twilio PEAR channel to PEAR
License:        Public Domain
URL:            http://twilio.github.io/pear/
Source0:        http://%{channelname}/channel.xml

BuildArch:  noarch
BuildRequires:  php-pear(PEAR)
Requires:   php-pear(PEAR)
Requires(post):     %{__pear}
Requires(postun):   %{__pear}
Provides:   php-channel(%{channelname})
Packager:   George Machitidze

%description
This package adds the Twilio Pear channel which allows PEAR packages
from this channel to be installed.

%prep
%setup -q -c -T

%build

%install
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{pear_xmldir}/%{name}.xml

%post
if [ $1 -eq  1 ] ; then
        %{__pear} channel-add %{pear_xmldir}/%{name}.xml > /dev/null || :
else
        %{__pear} channel-update %{pear_xmldir}/%{name}.xml > /dev/null ||:
fi

%postun
if [ $1 -eq 0 ] ; then
        %{__pear} channel-delete %{channelname} > /dev/null || :
fi

%files
%{pear_xmldir}/%{name}.xml

%changelog
* Fri Dec 26 2014 George Machitidze <giomac@gmail.com> - 0.1-0
- Initial build
