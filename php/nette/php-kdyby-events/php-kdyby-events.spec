# remirepo/fedora spec file for php-kdyby-events
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    8049e0fc7abb48178b4a2a9af230eceebe1a83bc
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     kdyby
%global gh_project   events
%global ns_vendor    Kdyby
%global ns_project   Events
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.4.0
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Events for Nette Framework

Group:          Development/Libraries
License:        BSD or GPLv2 or GPLv3
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
# pull a git snapshot to get test sutie
Source1:        makesrc.sh
# Autoloader
Source2:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(nette/di) >= 2.3
BuildRequires:  php-composer(nette/utils) >= 2.3
BuildRequires:  php-composer(doctrine/common) >= 2.5.0
BuildRequires:  php-composer(symfony/class-loader)
# From composer.json, "require-dev": {
#        "nette/nette": "~2.3@dev",
#        "nette/application": "~2.3@dev",
#        "nette/bootstrap": "~2.3@dev",
#        "nette/caching": "~2.3@dev",
#        "nette/component-model": "~2.2@dev",
#        "nette/database": "~2.3@dev",
#        "nette/deprecated": "~2.3@dev",
#        "nette/di": "~2.3@dev",
#        "nette/finder": "~2.3@dev",
#        "nette/forms": "~2.3@dev",
#        "nette/http": "~2.3@dev",
#        "nette/mail": "~2.3@dev",
#        "nette/neon": "~2.3@dev",
#        "nette/php-generator": "~2.3@dev",
#        "nette/reflection": "~2.3@dev",
#        "nette/robot-loader": "~2.3@dev",
#        "nette/safe-stream": "~2.3@dev",
#        "nette/security": "~2.3@dev",
#        "nette/tokenizer": "~2.2@dev",
#        "latte/latte": "~2.3@dev",
#        "tracy/tracy": "~2.3@dev",
#        "nette/utils": "~2.3@dev",
#        "symfony/event-dispatcher": "~2.5",
#        "nette/tester": "~1.4@rc",
#        "jakub-onderka/php-parallel-lint": "~0.7"
# The framework is enough as it requires everything
BuildRequires:  php-composer(nette/nette) >= 2.3
BuildRequires:  php-composer(nette/tester) >= 1.4
BuildRequires:  php-composer(symfony/event-dispatcher) >= 2.5
%endif

# from composer.json, "require": {
#        "nette/di": "~2.3@dev",
#        "nette/utils": "~2.3@dev"
Requires:       php-composer(nette/di) >= 2.3
Requires:       php-composer(nette/di) <  3
Requires:       php-composer(nette/utils) >= 2.3
Requires:       php-composer(nette/utils) <  3
# To avoid having to provide the compatibility layer
# version 2.5.0 for autoloader
Requires:       php-composer(doctrine/common) >= 2.5.0
# For autoloader
Requires:       php-composer(symfony/class-loader)
# from phpcompatinfo report for version 2.4.0
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
This extension is here to provide robust events system for Nette Framework.

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE2} src/%{ns_vendor}/%{ns_project}/autoload.php


%build
# Nothing


%install
rm -rf                  %{buildroot}
mkdir -p                %{buildroot}%{php_home}
cp -pr src/%{ns_vendor} %{buildroot}%{php_home}/%{ns_vendor}


%check
%if %{with_tests}
: Generate configuration
cat /etc/php.ini /etc/php.d/*ini >php.ini
export LANG=fr_FR.utf8

: Generate autoloader
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Tester/autoload.php';
require_once '%{php_home}/Nette/autoload.php';
require_once '%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';
EOF

php -r 'require "%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php";'

: Run test suite in sources tree
nette-tester --colors 0 -p php -c ./php.ini tests -s
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license license.md
%doc README.md
%doc composer.json
%{php_home}/%{ns_vendor}


%changelog
* Sun Nov  1 2015 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- initial package