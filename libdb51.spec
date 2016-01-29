%define __soversion_major 5
%define __soversion %{__soversion_major}.1
%define main_version 5.1.29
%define realname libdb

Summary: The Berkeley DB database library for C
Name: libdb51
Version: %{main_version}
Release: 0.%{?dist}
Source0: http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
Source1: http://download.oracle.com/berkeley-db/db.1.85.tar.gz
# db-1.85 upstream patches
Patch10: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.1
Patch11: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.2
Patch12: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.3
Patch13: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.4
# other patches
Patch20: db-1.85-errno.patch
Patch22: db-4.6.21-1.85-compat.patch
Patch24: db-4.5.20-jni-include-dir.patch
URL: http://www.oracle.com/database/berkeley-db/
License: BSD
Group: System Environment/Libraries
BuildRequires: perl, libtool
BuildRequires: tcl-devel >= 8.5.2-3
#BuildRequires: gcc-java
#BuildRequires: java-1.6.0-openjdk-devel
BuildRequires: chrpath
BuildRequires: dos2unix
BuildRoot: %{_tmppath}/%{realname}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, Java, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package utils
Summary: Command line tools for managing Berkeley DB databases
Group: Applications/Databases
Requires: %{name} = %{version}-%{release}

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. DB supports C, C++, Java and Perl APIs.

%package devel
Summary: C development files for the Berkeley DB library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the header files,
libraries, and documentation for building programs which use the
Berkeley DB.

%package static
Summary: Berkeley DB static libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description static
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains static libraries
needed for applications that require static linking of
Berkeley DB.

%package cxx-devel
Summary: The Berkeley DB database library for C++
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description cxx-devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, Java, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package tcl-devel
Summary: Development files for using the Berkeley DB with tcl
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description tcl-devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in Tcl.

%package sql-devel
Summary: Development files for using the Berkeley DB with sql
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description sql-devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in SQL.

#%package java-devel
#Summary: Development files for using the Berkeley DB with Java
#Group: Development/Libraries
#Requires: %{name} = %{version}-%{release}
#Requires: %{name}-devel = %{version}-%{release}
#
#%description java-devel
#The Berkeley Database (Berkeley DB) is a programmatic toolkit that
#provides embedded database support for both traditional and
#client/server applications. This package contains the libraries
#for building programs which use the Berkeley DB in Java.

%prep
%setup -q -n db-%{version} -a 1

pushd db.1.85/PORT/linux
%patch10 -p0 -b .1.1
popd
pushd db.1.85
%patch11 -p0 -b .1.2
%patch12 -p0 -b .1.3
%patch13 -p0 -b .1.4
%patch20 -p1 -b .errno
popd

%patch22 -p1 -b .185compat
%patch24 -p1 -b .4.5.20.jni

cd dist
./s_config

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"; export CFLAGS

# Build the old db-185 libraries.
make -C db.1.85/PORT/%{_os} OORG="$CFLAGS"

build() {
    test -d dist/$1 || mkdir dist/$1
    # Static link db_dump185 with old db-185 libraries.
    /bin/sh libtool --mode=compile	%{__cc} $RPM_OPT_FLAGS -Idb.1.85/PORT/%{_os}/include -D_REENTRANT -c util/db_dump185.c -o dist/$1/db_dump185.lo
    /bin/sh libtool --mode=link	%{__cc} -o dist/$1/db_dump185 dist/$1/db_dump185.lo db.1.85/PORT/%{_os}/libdb.a

    pushd dist
    popd
    pushd dist/$1
    ln -sf ../configure .
    # XXX --enable-diagnostic should be disabled for production (but is
    # useful).
    # XXX --enable-debug_{r,w}op should be disabled for production.
    %configure -C \
	--enable-compat185 --enable-dump185 \
	--enable-shared --enable-static \
	--enable-tcl --with-tcl=%{_libdir} \
	--enable-cxx --enable-sql \
	--disable-java \
	--enable-test \
	--with-tcl=%{_libdir}/tcl8.5 \
	--disable-rpath \
	# --enable-diagnostic \
	# --enable-debug --enable-debug_rop --enable-debug_wop \

    # Remove libtool predep_objects and postdep_objects wonkiness so that
    # building without -nostdlib doesn't include them twice.  Because we
    # already link with g++, weird stuff happens if you don't let the
    # compiler handle this.
    perl -pi -e 's/^predep_objects=".*$/predep_objects=""/' libtool
    perl -pi -e 's/^postdep_objects=".*$/postdep_objects=""/' libtool
    perl -pi -e 's/-shared -nostdlib/-shared/' libtool

    make %{?_smp_mflags}

    # XXX hack around libtool not creating ./libs/libdb_java-X.Y.lai
    LDBJ=./.libs/libdb_java-%{__soversion}.la
    if test -f ${LDBJ} -a ! -f ${LDBJ}i; then
	sed -e 's,^installed=no,installed=yes,' < ${LDBJ} > ${LDBJ}i
    fi

    popd
}

build dist-tls

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}

%makeinstall -C dist/dist-tls

# XXX Nuke non-versioned archives and symlinks
rm -f ${RPM_BUILD_ROOT}%{_libdir}/{libdb.a,libdb_cxx.a,libdb_tcl.a,libdb_sql.a}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb-%{__soversion_major}.so
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb_cxx-%{__soversion_major}.so
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb_tcl-%{__soversion_major}.so
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb_sql-%{__soversion_major}.so
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb_tcl.so
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb_sql.so
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb_cxx.so
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb.so

chmod +x ${RPM_BUILD_ROOT}%{_libdir}/*.so*


# Rename the utilities.
for bin in ${RPM_BUILD_ROOT}%{_bindir}/*db_* ; do
    t=`echo ${bin} | sed "s,db_,db51_,g"`
    mv ${bin} ${t}
done

mv ${RPM_BUILD_ROOT}%{_bindir}/dbsql ${RPM_BUILD_ROOT}%{_bindir}/dbsql51

# Leave relative symlinks in %%{_libdir}.
  touch $RPM_BUILD_ROOT/rootfile
  root=..
  while [ ! -e $RPM_BUILD_ROOT/%{_libdir}/${root}/rootfile ] ; do
    root=${root}/..
  done
  rm $RPM_BUILD_ROOT/rootfile

#  ln -sf ${root}/%{_lib}/libdb-%{__soversion}.so $RPM_BUILD_ROOT/%{_libdir}/

# Move the header files to a subdirectory, in case we're deploying on a
# system with multiple versions of DB installed.
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/%{realname}-%{__soversion}/
mv ${RPM_BUILD_ROOT}%{_includedir}/*.h ${RPM_BUILD_ROOT}%{_includedir}/%{realname}-%{__soversion}/

# Create symlinks to includes so that "use <db.h> and link with -ldb" works.
#for i in db.h db_cxx.h db_185.h; do
#	ln -s %{name}/$i ${RPM_BUILD_ROOT}%{_includedir}
#done

# Move java jar file to the correct place
#mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/java
#mv ${RPM_BUILD_ROOT}%{_libdir}/*.jar ${RPM_BUILD_ROOT}%{_datadir}/java

# Eliminate installed doco
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/docs

# XXX Avoid Permission denied. strip when building as non-root.
chmod u+w ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_bindir}/*

# remove unneeded .la files (#225675)
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

# remove C# devel files
rm -rf docs/csharp

# avoid fancy permissons
chmod 0755 ${RPM_BUILD_ROOT}%{_libdir}/*.so

# remove RPATHs
chrpath -d ${RPM_BUILD_ROOT}%{_libdir}/*.so ${RPM_BUILD_ROOT}%{_bindir}/*

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -p /sbin/ldconfig cxx-devel

%postun -p /sbin/ldconfig cxx-devel

%post -p /sbin/ldconfig sql-devel

%postun -p /sbin/ldconfig sql-devel

%post -p /sbin/ldconfig tcl-devel

%postun -p /sbin/ldconfig tcl-devel

#%post -p /sbin/ldconfig java-devel
#
#%postun -p /sbin/ldconfig java-devel

%files
%defattr(-,root,root,-)
%doc LICENSE README
%{_libdir}/libdb-%{__soversion}.so

%files cxx-devel
%defattr(-,root,root,-)
%doc examples/cxx
%{_libdir}/libdb_cxx-%{__soversion}.so

%files utils
%defattr(-,root,root,-)
%{_bindir}/db*_archive
%{_bindir}/db*_checkpoint
%{_bindir}/db*_deadlock
%{_bindir}/db*_dump*
%{_bindir}/db*_hotbackup
%{_bindir}/db*_load
%{_bindir}/db*_printlog
%{_bindir}/db*_recover
%{_bindir}/db*_replicate
%{_bindir}/db*_stat
%{_bindir}/db*_upgrade
%{_bindir}/db*_verify

%files devel
%defattr(-,root,root,-)
%doc	docs/*
%doc	examples/c
%{_libdir}/libdb-%{__soversion}.so
%dir %{_includedir}/%{realname}-%{__soversion}
%{_includedir}/%{realname}-%{__soversion}/db.h
%{_includedir}/%{realname}-%{__soversion}/db_185.h
%{_includedir}/%{realname}-%{__soversion}/db_cxx.h

%files static
%defattr(-,root,root,-)
%{_libdir}/libdb-%{__soversion}.a
%{_libdir}/libdb_cxx-%{__soversion}.a
%{_libdir}/libdb_tcl-%{__soversion}.a
%{_libdir}/libdb_sql-%{__soversion}.a
#%{_libdir}/libdb_java-%{__soversion}.a

%files tcl-devel
%defattr(-,root,root,-)
%{_libdir}/libdb_tcl-%{__soversion}.so

%files sql-devel
%defattr(-,root,root,-)
%doc examples/sql
%{_bindir}/dbsql51
%{_libdir}/libdb_sql-%{__soversion}.so
%{_includedir}/%{realname}-%{__soversion}/dbsql.h

#%files java-devel
#%defattr(-,root,root,-)
#%doc examples/java
#%{_libdir}/libdb_java*.so
#%{_datadir}/java/*.jar

%changelog
* Fri Jan 29 2016 George Machitidze <giomac@gmail.com> 5.1.29-0
- bump to version 5.1.29
- build for compatibility for RHEL/CentOS 7

* Tue Aug  9 2011 Jindrich Novy <jnovy@redhat.com> 5.1.25-3
- bump and rebuild because of multilib issues (#729250)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Jindrich Novy <jnovy@redhat.com> 5.1.25-1
- update to 5.1.25

* Wed Sep 29 2010 jkeating - 5.1.19-2
- Rebuilt for gcc bug 634757

* Fri Sep 10 2010 Jindrich Novy <jnovy@redhat.com> 5.1.19-1
- update to 5.1.19
- rename -devel-static to -static subpackage (#617800)
- build java on all arches

* Wed Jul  7 2010 Jindrich Novy <jnovy@redhat.com> 5.0.26-1
- update to 5.0.26
- drop BR: ed

* Thu Jun 17 2010 Jindrich Novy <jnovy@redhat.com> 5.0.21-2
- add Requires: libdb-cxx to libdb-devel

* Wed Apr 21 2010 Jindrich Novy <jnovy@redhat.com> 5.0.21-1
- initial build

* Thu Apr 15 2010 Jindrich Novy <jnovy@redhat.com> 5.0.21-0.2
- remove C# documentation
- disable/remove rpath
- fix description
- tighten dependencies
- run ldconfig for cxx and sql subpackages

* Fri Apr  9 2010 Jindrich Novy <jnovy@redhat.com> 5.0.21-0.1
- enable sql
- package 5.0.21
