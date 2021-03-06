# remirepo/Fedora spec file for php-zendframework-zend-mail
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    3311e163de28dc3b41dfba642939132a16336143
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-mail
%global php_home     %{_datadir}/php
%global library      Mail
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.6.1
Release:        1%{?dist}
Summary:        Zend Framework %{library} component

Group:          Development/Libraries
License:        BSD
URL:            http://framework.zend.com/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-ctype
BuildRequires:  php-date
BuildRequires:  php-iconv
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-crypt)            >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-mime)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
BuildRequires:  php-composer(%{gh_owner}/zend-validator)        >= 2.6
# From composer, "require-dev": {
#        "zendframework/zend-config": "^2.6",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0"
BuildRequires:  php-composer(%{gh_owner}/zend-config)           >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.7.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "zendframework/zend-crypt": "^2.6",
#        "zendframework/zend-loader": "^2.5",
#        "zendframework/zend-mime": "^2.5",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0",
#        "zendframework/zend-validator": "^2.6"
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-crypt)            >= 2.6
Requires:       php-composer(%{gh_owner}/zend-crypt)            <  3
Requires:       php-composer(%{gh_owner}/zend-loader)           >= 2.5
Requires:       php-composer(%{gh_owner}/zend-loader)           <  3
Requires:       php-composer(%{gh_owner}/zend-mime)             >= 2.5
Requires:       php-composer(%{gh_owner}/zend-mime)             <  3
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
Requires:       php-composer(%{gh_owner}/zend-validator)        >= 2.6
Requires:       php-composer(%{gh_owner}/zend-validator)        <  3
# From composer, "suggest": {
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3 when using SMTP to deliver messages"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
%endif
%endif
# From phpcompatinfo report for version 2.6.1
Requires:       php-ctype
Requires:       php-date
Requires:       php-iconv
Requires:       php-pcre
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Mail provides generalized functionality to compose and send both text
and MIME-compliant multipart email messages. Mail can be sent with Zend\Mail
via the Mail\Transport\Sendmail, Mail\Transport\Smtp or the
Mail\Transport\File transport. Of course, you can also implement your own
transport by implementing the Mail\Transport\TransportInterface.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/Zend/
cp -pr src %{buildroot}%{php_home}/Zend/%{library}


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\Loader\AutoloaderFactory::factory(array(
    'Zend\Loader\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest\\%{library}' => dirname(__DIR__).'/test/',
           'Zend\\%{library}'     => '%{buildroot}%{php_home}/Zend/%{library}'
))));
require_once '%{php_home}/Zend/autoload.php';
EOF

%{_bindir}/phpunit --include-path=%{buildroot}%{php_home}

if which php70; then
   php70 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home}
fi
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc CONTRIBUTING.md README.md
%doc composer.json
%{php_home}/Zend/%{library}


%changelog
* Thu Feb 25 2016 Remi Collet <remi@fedoraproject.org> - 2.6.1-1
- update to 2.6.1

* Fri Feb 19 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0
- raise dependency on zend-crypt >= 2.6
- raise dependency on zend-stdlib >= 2.7
- raise dependency on zend-validator >= 2.6

* Fri Sep 11 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- update to 2.5.2
- raise minimum PHP version to 5.5

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
