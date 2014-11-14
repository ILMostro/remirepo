# spec file for php-pecl-event
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package         php-pecl-event}
%{!?scl:         %global _root_prefix %{_prefix}}
%{!?php_inidir:  %global php_inidir   %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl       %{_bindir}/pecl}
%{!?__php:       %global __php        %{_bindir}/php}

%global with_tests  %{?_without_tests:0}%{!?_without_tests:1}
%global pecl_name   event
%global with_zts    0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
# After sockets.so
%global ini_name  z-%{pecl_name}.ini
%else
# After 20-sockets.so
%global ini_name  40-%{pecl_name}.ini
%endif

Summary:       Provides interface to libevent library
Name:          %{?scl_prefix}php-pecl-%{pecl_name}
Version:       1.11.1
Release:       1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/event
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{?scl_prefix}php-devel > 5.4
BuildRequires: %{?scl_prefix}php-pear

%if 0%{?scl:1} && 0%{?fedora} < 15 && 0%{?rhel} < 7 && "%{?scl_vendor}" != "remi"
# Filter in the SCL collection
%{?filter_requires_in: %filter_requires_in %{_libdir}/.*\.so}
# libvent from SCL as not available in system
BuildRequires: %{?scl_prefix}libevent-devel  >= 2.0.2
Requires:      %{?scl_prefix}libevent%{_isa} >= 2.0.2
%global        _event_prefix %{_prefix}
%else
BuildRequires: libevent-devel >= 2.0.2
%global        _event_prefix %{_root_prefix}
%endif

BuildRequires: openssl-devel
BuildRequires: pkgconfig

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
Requires:      %{?scl_prefix}php-sockets%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:      %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:      %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php53u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php54-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php54w-pecl-%{pecl_name} <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%endif
%{?filter_setup}


%description
This is an extension to efficiently schedule I/O, time and signal based
events using the best I/O notification mechanism available for specific
platform. This is a port of libevent to the PHP infrastructure.

Version 1.0.0 introduces:
* new OO API breaking backwards compatibility
* support of libevent 2+ including HTTP, DNS, OpenSSL and the event listener.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection}.


%prep
%setup -q -c 

# Don't install/register tests
sed -e 's/role="test"/role="src"/' -i package.xml

mv %{pecl_name}-%{version} NTS

cd NTS

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_EVENT_VERSION/{s/.* "//;s/".*$//;p}' php_event.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

# duplicate for ZTS build
%if %{with_zts}
cp -pr NTS ZTS
%endif

# Drop in the bit of configuration
cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension = %{pecl_name}.so
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-event-libevent-dir=%{_event_prefix} \
    --with-libdir=%{_lib} \
    --with-event-core \
    --with-event-extra \
    --with-event-openssl \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-event-libevent-dir=%{_event_prefix} \
    --with-libdir=%{_lib} \
    --with-event-core \
    --with-event-extra \
    --with-event-openssl \
    --with-event-pthreads \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

# use z-event.ini to ensure event.so load "after" sockets.so
: Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
: Install the ZTS stuff
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

: Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

: Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
if [ -f %{php_extdir}/sockets.so ]; then
  OPTS="-d extension=sockets.so"
fi

: Minimal load test for NTS extension
%{__php} --no-php-ini $OPTS  \
    --define extension=NTS/modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini $OPTS  \
    --define extension=ZTS/modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif

%if %{with_tests}
cd NTS
: Upstream test suite for NTS extension
SKIP_ONLINE_TESTS=1 \
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n $OPTS -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php

%if %{with_zts}
cd ../ZTS
: Upstream test suite for ZTS extension
SKIP_ONLINE_TESTS=1 \
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n $OPTS -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php
%endif
%endif


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Fri Nov 14 2014 Remi Collet <remi@fedoraproject.org> - 1.11.1-1
- Update to 1.11.1 (stable)
- no change, only our patch merged upstream

* Thu Nov 13 2014 Remi Collet <remi@fedoraproject.org> - 1.11.0-1
- Update to 1.11.0 (stable)
- don't provide test suite
- add patch for old openssl in EL-5
  https://bitbucket.org/osmanov/pecl-event/pull-request/10

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 1.10.3-2
- improve SCL build

* Mon Aug 11 2014 Remi Collet <remi@fedoraproject.org> - 1.10.3-1
- Update to 1.10.3 (no change)

* Fri Jun 20 2014 Remi Collet <remi@fedoraproject.org> - 1.10.2-1
- Update to 1.10.2 (stable)

* Sun May 11 2014 Remi Collet <remi@fedoraproject.org> - 1.10.1-1
- Update to 1.10.1 (stable, no change)

* Sat May 10 2014 Remi Collet <remi@fedoraproject.org> - 1.10.0-1
- Update to 1.10.0 (stable)

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 1.9.1-3
- add numerical prefix to extension configuration file

* Sun Mar 23 2014 Remi Collet <remi@fedoraproject.org> - 1.9.1-2
- allow SCL build, with libevent from SCL when needed

* Sun Mar 23 2014 Remi Collet <remi@fedoraproject.org> - 1.9.1-1
- Update to 1.9.1 (stable)

* Sun Mar 23 2014 Remi Collet <remi@fedoraproject.org> - 1.9.0-2
- add patch for php 5.6
  https://bitbucket.org/osmanov/pecl-event/pull-request/7

* Fri Jan 17 2014 Remi Collet <remi@fedoraproject.org> - 1.9.0-1
- Update to 1.9.0 (stable)
- add option to disable tests during build
- adapt for SCL

* Sat Jan 11 2014 Remi Collet <remi@fedoraproject.org> - 1.8.1-2
- install doc in pecl doc_dir
- install tests in pecl test_dir
- open https://bitbucket.org/osmanov/pecl-event/pull-request/6

* Mon Oct 07 2013 Remi Collet <remi@fedoraproject.org> - 1.8.1-1
- Update to 1.8.1 (stable)
- drop patch merged upstream
- patch for https://bitbucket.org/osmanov/pecl-event/pull-request/4

* Sun Oct 06 2013 Remi Collet <remi@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0
- patch for https://bitbucket.org/osmanov/pecl-event/pull-request/3

* Mon Sep 16 2013 Remi Collet <remi@fedoraproject.org> - 1.7.8-1
- Update to 1.7.8

* Sun Sep 08 2013 Remi Collet <remi@fedoraproject.org> - 1.7.6-1
- Update to 1.7.6

* Mon Aug 19 2013 Remi Collet <remi@fedoraproject.org> - 1.7.5-1
- Update to 1.7.5

* Sun Jul 28 2013 Remi Collet <remi@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2

* Wed Jul 24 2013 Remi Collet <remi@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1

* Thu Jul 18 2013 Remi Collet <remi@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Thu Jul 18 2013 Remi Collet <remi@fedoraproject.org> - 1.6.2-2
- missing requires php-sockets
- enable thread safety for ZTS extension

* Thu Jul 18 2013 Remi Collet <remi@fedoraproject.org> - 1.6.2-1
- Update to 1.6.2

* Sat Apr 20 2013 Remi Collet <remi@fedoraproject.org> - 1.6.1-1
- initial package, version 1.6.1
- upstream bugs:
  https://bugs.php.net/64678 missing License
  https://bugs.php.net/64679 buffer overflow
  https://bugs.php.net/64680 skip online test
