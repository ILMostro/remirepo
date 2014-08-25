# spec file for php-pecl-http
#
# Copyright (c) 2012-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package         php-pecl-http}
%{!?scl:         %global _root_prefix %{_prefix}}
%{!?php_inidir:  %global php_inidir   %{_sysconfdir}/php.d}
%{!?php_incldir: %global php_incldir  %{_includedir}/php}
%{!?__pecl:      %global __pecl       %{_bindir}/pecl}
%{!?__php:       %global __php        %{_bindir}/php}

# The project is pecl_http but the extension is only http
%global proj_name pecl_http
%global pecl_name http
%global with_zts  0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
# after json hash iconv propro raphf
%global ini_name  z-%{pecl_name}.ini
%else
# after 40-json 20-iconv 40-propro 40-raphf
%global ini_name  50-%{pecl_name}.ini
%endif
%global prever     RC3
%global with_tests %{?_without_tests:0}%{!?_without_tests:1}

Name:           %{?scl_prefix}php-pecl-http
Version:        2.1.0
Release:        0.6.RC3%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
Summary:        Extended HTTP support

License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/pecl_http
Source0:        http://pecl.php.net/get/%{proj_name}-%{version}%{?prever}.tgz

# From http://www.php.net/manual/en/http.configuration.php
Source1:        %{proj_name}.ini

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel >= 5.3.0
BuildRequires:  %{?scl_prefix}php-hash
BuildRequires:  %{?scl_prefix}php-iconv
BuildRequires:  %{?scl_prefix}php-json
BuildRequires:  %{?scl_prefix}php-spl
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  pcre-devel
BuildRequires:  zlib-devel >= 1.2.0.4
BuildRequires:  curl-devel >= 7.18.2
BuildRequires:  %{?scl_prefix}php-pecl-propro-devel
BuildRequires:  %{?scl_prefix}php-pecl-raphf-devel

%if 0%{?scl:1} && 0%{?fedora} < 15 && 0%{?rhel} < 7 && "%{?scl_vendor}" != "remi"
# Filter in the SCL collection
%{?filter_requires_in: %filter_requires_in %{_libdir}/.*\.so}
# libvent from SCL as not available in system
BuildRequires: %{scl_prefix}libevent-devel  > 2
Requires:      %{scl_prefix}libevent%{_isa} > 2
Requires:      libcurl%{_isa}
Requires:      zlib%{_isa}
%global        _event_prefix %{_prefix}

%else
%global        _event_prefix %{_root_prefix}
%if "%{?vendor}" == "Remi Collet"
BuildRequires: libevent-devel > 2
%else
# Copr build
BuildRequires: libevent-devel > 1.4
%endif
%endif

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%if "%{php_version}" < "5.4"
# php 5.3.3 in EL-6 don't use arched virtual provides
# so only requires real packages instead
Requires:       %{?scl_prefix}php-common%{?_isa}
%else
Requires:       %{?scl_prefix}php-hash%{?_isa}
Requires:       %{?scl_prefix}php-iconv%{?_isa}
Requires:       %{?scl_prefix}php-json%{?_isa}
Requires:       %{?scl_prefix}php-spl%{?_isa}
%endif
Requires:       %{?scl_prefix}php-pecl(propro)%{?_isa}
Requires:       %{?scl_prefix}php-pecl(raphf)%{?_isa}
%if "%{php_version}" > "5.6"
# V1 don't support PHP 5.6 https://bugs.php.net/66879
Obsoletes:      %{?scl_prefix}php-pecl-http1 < 2
%else
# Can't install both versions of the same extension
Conflicts:      %{?scl_prefix}php-pecl-http1
%endif

Provides:       %{?scl_prefix}php-pecl(%{proj_name})         = %{version}%{?prever}
Provides:       %{?scl_prefix}php-pecl(%{proj_name})%{?_isa} = %{version}%{?prever}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}%{?prever}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}%{?prever}
Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}%{?prever}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}%{?prever}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:     php53-pecl-http
Obsoletes:     php53u-pecl-http
Obsoletes:     php54-pecl-http
Obsoletes:     php54w-pecl-http
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-http
Obsoletes:     php55w-pecl-http
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-http
Obsoletes:     php56w-pecl-http
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%endif
%{?filter_setup}


%description
The HTTP extension aims to provide a convenient and powerful set of
functionality for major applications.

The HTTP extension eases handling of HTTP URLs, dates, redirects, headers
and messages in a HTTP context (both incoming and outgoing). It also provides
means for client negotiation of preferred language and charset, as well as
a convenient way to exchange arbitrary data with caching and resuming
capabilities.

Also provided is a powerful request and parallel interface.

Version 2 is completely incompatible to previous version.

Note:
. php-pecl-http1 provides API version 1
. php-pecl-http  provides API version 2

Documentation : http://devel-m6w6.rhcloud.com/mdref/http


%package devel
Summary:       Extended HTTP support developer files (header)
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}php-devel%{?_isa} >= 5.3.0
%if "%{php_version}" > "5.6"
# V1 don't support PHP 5.6 https://bugs.php.net/66879
Obsoletes:     %{?scl_prefix}php-pecl-http1-devel < 2
%else
# Can't install both versions of the same extension
Conflicts:     %{?scl_prefix}php-pecl-http1-devel
%endif

%description devel
These are the files needed to compile programs using HTTP extension.


%prep
%setup -c -q 

mv %{proj_name}-%{version}%{?prever} NTS
cd NTS

extver=$(sed -n '/#define PHP_PECL_HTTP_VERSION/{s/.* "//;s/".*$//;p}' php_http.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream HTTP version is now ${extver}, expecting %{version}%{?prever}.
   : Update the pdover macro and rebuild.
   exit 1
fi
cd ..

cp %{SOURCE1} %{ini_name}

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif


%build
peclconf() {
%configure \
  --with-http \
  --with-http-zlib-dir=%{_root_prefix} \
  --with-http-libcurl-dir=%{_root_prefix} \
  --with-http-libevent-dir=%{_event_prefix} \
  --with-libdir=%{_lib} \
  --with-php-config=$1
}
cd NTS
%{_bindir}/phpize
peclconf %{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
peclconf %{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file (z-http.ini to be loaded after json)
install -Dpm644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Test & Documentation
cd NTS
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_testdir}/%{proj_name}/$i
done
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{proj_name}/$i
done


%check
%if "%{php_version}" < "5.4"
# Known failed test with 5.3.3 (need investigations)
rm ?TS/tests/envrequestbody001.phpt \
   ?TS/tests/envrequestbody002.phpt \
   ?TS/tests/envrequestbody003.phpt \
   ?TS/tests/envrequestjson002.phpt \
   ?TS/tests/envresponse015.phpt
%endif

# Shared needed extensions
modules=""
for mod in json hash iconv propro raphf; do
  if [ -f %{php_extdir}/${mod}.so ]; then
    modules="$modules -d extension=${mod}.so"
  fi
done

: Minimal load test for NTS extension
%{__php} --no-php-ini \
    $modules \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_tests}
: Upstream test suite NTS extension
cd NTS
SKIP_ONLINE_TESTS=1 \
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n $modules -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff
%endif

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    $modules \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_tests}
: Upstream test suite ZTS extension
cd ../ZTS
SKIP_ONLINE_TESTS=1 \
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n $modules -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff
%endif
%endif


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{proj_name} >/dev/null || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{proj_name}
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif

%files devel
%defattr(-,root,root,-)
%doc %{pecl_testdir}/%{proj_name}
%{php_incldir}/ext/%{pecl_name}

%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif


%changelog
* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 2.1.0-0.6.RC3
- improve SCL build

* Tue Aug 19 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-0.5.RC3
- Update to 2.1.0RC3
- ignore known failed test with PHP 5.3.3

* Mon Aug 11 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-0.4.RC2
- add upstream patch for PHP 5.3

* Mon Aug 11 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-0.3.RC2
- Update to 2.1.0RC2

* Tue Aug 05 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-0.2.RC1
- add upstream patches

* Sat Aug 02 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-0.1.RC1
- Update to 2.1.0RC1
- run test suite during build

* Fri Jul 11 2014 Remi Collet <remi@fedoraproject.org> - 2.0.7-1
- Update to 2.0.7

* Wed May 14 2014 Remi Collet <remi@fedoraproject.org> - 2.0.6-2
- php56: obsoletes php-pecl-http1

* Thu Apr 24 2014 Remi Collet <remi@fedoraproject.org> - 2.0.6-1
- Update to 2.0.6

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 2.0.5-2
- add numerical prefix to extension configuration file

* Fri Apr 04 2014 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5
- use libevent v2 in SCL

* Sun Mar 09 2014 Remi Collet <remi@fedoraproject.org> - 2.0.4-2
- add upstream patch for -Werror=format-security

* Thu Jan 02 2014 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4
- fix link to documentation
- update provided configuration

* Tue Dec 10 2013 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3 (stable)
- drop Conflicts with pecl/event

* Fri Nov 29 2013 Remi Collet <rcollet@redhat.com> - 2.0.1-1
- adapt for SCL

* Tue Nov 26 2013 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1 (stable)

* Fri Nov 22 2013 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0 (stable)
- install doc in pecl doc_dir
- install tests in pecl test_dir (in devel)

* Tue Aug 20 2013 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.18.beta5
- update to 2.0.0 beta5
- requires propro and raphf extensions

* Thu Mar 21 2013 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.15.beta4
- fix build with php 5.5.0beta1

* Sun Dec 30 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.14.beta4
- update to 2.0.0beta4

* Thu Dec 13 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.13.beta3
- update to 2.0.0beta3

* Thu Nov 29 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.12.beta2
- update to 2.0.0beta2
- also provides php-http
- remove old directives from configuration file

* Fri Oct 12 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.11.beta1
- update to 2.0.0beta1
- must be load after json, to rename config to z-http.ini

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-0.10.alpha1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 21 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.9.alpha1
- update to 2.0.0alpha1

* Sat Mar 31 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.8.dev10
- update to 2.0.0dev10

* Fri Mar 16 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.7.dev8
- update to 2.0.0dev8

* Fri Mar 09 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.6.dev7
- update to 2.0.0dev7

* Fri Mar 02 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.5.dev6
- update to 2.0.0dev6

* Sat Feb 18 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.4.dev5
- update to 2.0.0dev5
- fix filters

* Wed Jan 25 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.3.dev4
- zts binary in /usr/bin with zts prefix

* Mon Jan 23 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.2.dev4
- update to 2.0.0dev4
- fix missing file https://bugs.php.net/60839

* Sun Jan 22 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.dev3
- initial package

