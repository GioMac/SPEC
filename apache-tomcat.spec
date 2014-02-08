%define appprefix	/opt
%define appbuildroot	%{buildroot}%{appprefix}/%{name}
%define	appdir		%{appprefix}/%{name}

Name:		apache-tomcat
Version:	7.0.50
Release:	0%{?dist}
Summary:	Apache Servlet/JSP Engine
Group:		Networking/Daemons
License:	ASL 2.0
URL:		http://tomcat.apache.org
Source0:	%{name}-%{version}.tar.gz
Source1:	apache-tomcat-setenv.sh
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	redhat-release = 6
BuildArch:	x86_64

#Requires SUN JDK
Requires:	jdk >= 1.7.0

#Requres tomcat6 package for creation and compatibility with standard tomcat user
Requires:	tomcat6

Packager:	George Machitidze <giomac@gmail.com>

%description
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License version 2.0. Tomcat is intended
to be a collaboration of the best-of-breed developers from around the world.

%prep
%setup -q

%install
rm -rf %{buildroot}
mkdir -p %{appbuildroot}
cp -a * %{appbuildroot}/
install -m 0755 %{SOURCE1} %{appbuildroot}/bin/setenv.sh
cd %{appbuildroot}
rm -f LICENSE NOTICE RELEASE-NOTES RUNNING.txt
cd bin
rm -f *.bat
chmod o-rwx -R %{appbuildroot}

%clean
rm -rf %{buildroot}

%files
%doc LICENSE NOTICE RELEASE-NOTES RUNNING.txt
%defattr(-,tomcat,tomcat,-)
%attr(0750,tomcat,tomcat) %dir %{appdir}/bin
%config(noreplace) %{appdir}/bin/*.sh
%config(noreplace) %{appdir}/bin/*.xml
%{appdir}/bin/*.jar
%{appdir}/bin/*.tar.gz
%config(noreplace) %{appdir}/conf/
%{appdir}/lib/
%{appdir}/logs/
%{appdir}/temp/
%{appdir}/webapps/
%{appdir}/work/

%changelog
* Sat Feb 08 2014 George Machitidze <giomac@gmail.com> 7.0.50-0
- initial release
