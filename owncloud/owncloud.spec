# remirepo spec file for owncloud from:
#
# Fedora spec file for owncloud
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
Name:           owncloud
Version:        8.2.3
Release:        4%{?dist}
Summary:        Private file sync and share server
Group:          Applications/Internet

License:        AGPLv3+ and MIT and BSD and CC-BY and CC-BY-SA and GPLv3 and Public Domain and (MPLv1.1 or GPLv2+ or LGPLv2+) and (MIT or GPL+) and (MIT or GPLv2) and ASL 2.0 and LGPLv3
URL:            http://owncloud.org

# Tarball with non-free sources stripped. To generate:
# ./owncloud-delete-nonfree.sh %%{name}-%%{version}.tar.bz2
Source0:        %{name}-%{version}-repack.tar.bz2
# orig source:  https://download.owncloud.org/community/%%{name}-%%{version}.tar.bz2
# sha256sum: https://download.owncloud.org/community/%%{name}-%%{version}.tar.bz2.sha256

# used to repack the source tarball
Source42:       %{name}-delete-nonfree.sh


Source1:        %{name}-httpd.conf
Source2:        %{name}-access-httpd.conf.avail
Source6:        %{name}-nginx.conf
# Config snippets
Source100:      %{name}-auth-any.inc
Source101:      %{name}-auth-local.inc
Source102:      %{name}-auth-none.inc
Source103:      %{name}-defaults.inc
# packaging notes and doc
Source3:        %{name}-README.fedora
Source4:        %{name}-mysql.txt
Source5:        %{name}-postgresql.txt
# config.php containing just settings we want to specify, OwnCloud's
# initial setup will fill out other settings appropriately
Source7:        %{name}-config.php

# Adjust mediaelement not to use its SWF and Silverlight plugins. This
# changes 'plugins:["flash,"silverlight","youtube","vimeo"]' to
# 'plugins:["youtube","vimeo"]'
Patch1:         %{name}-8.2.3-videoviewer_noplugins.patch
# Turn on include path usage for the Composer autoloader (so it'll find
# systemwide PSR-0 and PSR-4 compliant libraries)
# Upstream wouldn't likely take this, they probably only care about their
# bundled copies
Patch2:        %{name}-8.2.3-composer_include_path.patch
# Stop OC from trying to do stuff to .htaccess files. Just calm down, OC.
# Distributors are on the case.
Patch3:         %{name}-8.2.2-dont_update_htacess.patch

# Owncloud should use the system libraries with psr
Patch4:        %{name}-8.2.3-use_system_psr_libraries.patch

# Owncloud should use the system autoloaded react-promise and nitic-phpParser
Patch5:         %{name}-8.2.3-use_system_phpparser.patch

# Unbundle Google, Dropbox and AVS from app/files_external
Patch6:         %{name}-8.2.3-unbundle-files-external.patch

# unbundle php-Assetic to use the system autoloader
Patch7:         %{name}-8.2.3-use_system_assetic.patch

# Display the appropriate upgrade command for fedora/epel users bz#1321417
Patch8:         %{name}-8.2.3-correct-cli-upgrade-command.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

# expand pear macros on install
BuildRequires:  php-pear
# For sanity check
BuildRequires:  php-cli
BuildRequires:  php-composer(icewind/smb)     >= 1.0.4
BuildRequires:  php-composer(icewind/streams) >= 0.2

Requires:       %{name}-webserver = %{version}-%{release}
Requires:       %{name}-database = %{version}-%{release}

# Core PHP libs/extensions required by OC core
Requires:       php-curl
Requires:       php-dom
Requires:       php-exif
Requires:       php-fileinfo
Requires:       php-gd
Requires:       php-iconv
Requires:       php-json
Requires:       php-ldap
Requires:       php-mbstring
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-pdo
Requires:       php-session
Requires:       php-simplexml
Requires:       php-xmlwriter
Requires:       php-spl
Requires:       php-zip
%if 0%{?fedora} || 0%{?rhel} > 6
Requires:       php-filter
%endif

### External PHP libs required by OC core

# Ordering requires to match composer.json

# "sabre/dav" : "2.1.9"
# pulls in sabre event, http and vobject as deps
Requires:       php-composer(sabre/dav)  >= 2.1.9
Requires:       php-composer(sabre/dav)  < 2.2
Requires:       php-composer(sabre/vobject) >= 3.3.4
Requires:       php-composer(sabre/vobject) < 4.0.0
Requires:       php-composer(sabre/event) >= 2.0.0
Requires:       php-composer(sabre/event) < 3.0.0
Requires:       php-composer(sabre/http)  >= 3.0.0
Requires:       php-composer(sabre/http)  < 4.0.0

# "doctrine/dbal": "2.5.1"
Requires:       php-composer(doctrine/dbal) >= 2.5.1
Requires:       php-composer(doctrine/dbal) < 2.6

#"mcnetic/zipstreamer": "v0.7"
Requires:       php-composer(mcnetic/zipstreamer) >= 0.7

# "phpseclib/phpseclib": "~2.0@dev"
Requires:       php-composer(phpseclib/phpseclib) >= 2.0
Requires:       php-composer(phpseclib/phpseclib) < 3.0

#Requires:       php-composer(rackspace/php-opencloud) >= 1.9.2
# pulls in guzzle/http as a dep
Requires:       php-opencloud >= 1.9.2
Requires:       php-composer(guzzle/http) >= 3.8.0
Requires:       php-composer(guzzle/http) < 4.0.0

#"james-heinrich/getid3": "dev-master"
# fedora has 1.9.8 but current release 1.9.12
# bug filed for update: bz#1319676
Requires:       php-composer(james-heinrich/getid3)

# "jeremeamia/superclosure": "2.0.0"
Requires:       php-composer(jeremeamia/superclosure) >= 2.0

# "ircmaxell/random-lib": "~1.1"
# Also pulls in ircmaxell/security-lib which is a dep
Requires:       php-composer(ircmaxell/random-lib) >= 1.1
Requires:       php-composer(ircmaxell/random-lib) < 2.0
Requires:       php-composer(ircmaxell/security-lib) >= 1.0

# "bantu/ini-get-wrapper": "v1.0.1"
Requires:       php-composer(bantu/ini-get-wrapper) >= 1.0.1

# "natxet/CssMin": "dev-master"
# 3.0.4 is the current release and 3.0.3 in fedora
# ticket for update bz#1266491
Requires:       php-composer(natxet/CssMin) >= 3.0.2

# "punic/punic": "1.1.0"
Requires:       php-composer(punic/punic) >= 1.1.0

# "pear/archive_tar": "~1.4"
Requires:       php-composer(pear/archive_tar) >= 1.4
Requires:       php-composer(pear/archive_tar) < 2.0

# "patchwork/utf8": "~1.1"
Requires:       php-composer(patchwork/utf8) >= 1.1
Requires:       php-composer(patchwork/utf8) < 2.0

# "symfony/console": "2.6.4"
# pulls in symfony/event-dispatcher as a dep
# pulls in symfony/process as a dep
Requires:       php-composer(symfony/console) >= 2.6.4
Requires:       php-composer(symfony/event-dispatcher) >= 2.6.4
Requires:       php-composer(symfony/process) >= 2.6.4

# "symfony/routing": "2.6.4"
Requires:       php-composer(symfony/routing) >= 2.6.4

# "pimple/pimple": "~3.0"
Requires:       php-composer(pimple/pimple) >= 3.0
Requires:       php-composer(pimple/pimple) < 4.0

# "ircmaxell/password-compat": "1.0.*"
Requires:       php-composer(ircmaxell/password-compat) >= 1.0.0

# "nikic/php-parser": "~1.1"
Requires:       php-composer(nikic/php-parser) >= 1.0
Requires:       php-composer(nikic/php-parser) < 2.0

# "icewind/Streams": "0.2.0"
Requires:       php-composer(icewind/streams) >= 0.2

# "swiftmailer/swiftmailer": "@stable"
# Version 5.4.1 for autoloader in /usr/share/php
Requires:       php-composer(swiftmailer/swiftmailer) >= 5.4.1

# "guzzlehttp/guzzle": "~5.0"
# pulls in guzzlehttp/ringphp as a dep
# ringphp pulls in guzzlehttp/streams and react/promise
Requires:       php-composer(guzzlehttp/guzzle) >= 5.0
Requires:       php-composer(guzzlehttp/guzzle) < 6.0
Requires:       php-composer(guzzlehttp/ringphp) >= 1.1
Requires:       php-composer(guzzlehttp/ringphp) < 2.0
Requires:       php-composer(guzzlehttp/streams) >= 3.0
Requires:       php-composer(guzzlehttp/streams) < 4.0
Requires:       php-composer(react/promise) >= 2.2
Requires:       php-composer(react/promise) < 3.0

# "league/flysystem": "1.0.4"
Requires:       php-composer(league/flysystem) >= 1.0.4

# "pear/pear-core-minimal": "v1.10.0alpha2"
# this includes pear/console_getopt and pear/PEAR 
# which is not listed in composer.json unlike archive_tar
Requires:       php-composer(pear/pear-core-minimal) > 1.10

# "interfasys/lognormalizer": "dev-master@dev"
Requires:       php-composer(interfasys/lognormalizer) >= 1.0

# "deepdiver1975/TarStreamer": "v0.1-beta3"
# Despite the difference in name this is correct
# https://github.com/owncloud/3rdparty/tree/master/deepdiver1975/tarstreamer
Requires:       php-composer(owncloud/tarstreamer) >= 0.1

# "patchwork/jsqueeze": "^2.0"
Requires:       php-composer(patchwork/jsqueeze) >= 2.0
Requires:       php-composer(patchwork/jsqueeze) < 3.0

# "kriswallsmith/assetic": "^1.3"
Requires:       php-composer(kriswallsmith/assetic) >= 1.3
Requires:       php-composer(kriswallsmith/assetic) < 2.0



### For dependencies of apps/files_external

## SMB/CIFS external storage stuff

#"icewind/smb": "1.0.4"
# note that streams is a dep but already required by core anyway
Requires:       php-composer(icewind/smb)     >= 1.0.4
# This makes smb external storage usable iin performance
# and doesn't break things like encryption due to timeouts
Requires:       php-pecl(smbclient) >= 0.8.0


# Requiring so that the shipped external smb storage works
# The net command is needed and enabling smb tests for smbclient command
%if 0%{?fedora} >= 20 || 0%{?rhel} >= 7
Requires:       samba-common-tools
Requires:       samba-client
%endif

## Note these next bits are not listed in composer but manually dropped in place

## Dropbox external storage
Requires:       php-pear(pear.dropbox-php.com/Dropbox)

## Google Drive external storage
Requires:       php-google-apiclient >= 1.0.3

## AWS S3 external storage
Requires:       php-aws-sdk >= 2.7.0


%if 0%{?rhel}
Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python
%endif

%description
ownCloud gives you universal access to your files through a web interface or
WebDAV. It also provides a platform to easily view & sync your contacts,
calendars and bookmarks across all your devices and enables basic editing right
on the web. ownCloud is extendable via a simple but powerful API for
applications and plugins.


%package httpd
Summary:    Httpd integration for ownCloud
Group:      Applications/Internet

Provides:   %{name}-webserver = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}

# PHP dependencies
Requires:       php

%description httpd
%{summary}.


%package nginx
Summary:    Nginx integration for ownCloud
Group:      Applications/Internet

Provides:   %{name}-webserver = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}

# PHP dependencies
Requires:   php-fpm nginx

%description nginx
%{summary}.


%package mysql
Summary:    MySQL database support for ownCloud
Group:      Applications/Internet

Provides:   %{name}-database = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}

Requires:   php-mysql

%description mysql
This package ensures the necessary dependencies are in place for ownCloud to
work with MySQL / MariaDB databases. It does not require a MySQL / MariaDB
server to be installed, as you may well wish to use a remote database
server.

If you want the database to be on the same system as ownCloud itself, you must
also install and enable a MySQL / MariaDB server package. See README.mysql for
more details.

%package postgresql
Summary:    PostgreSQL database support for ownCloud
Group:      Applications/Internet

Provides:   %{name}-database = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}

Requires:   php-pgsql

%description postgresql
This package ensures the necessary dependencies are in place for ownCloud to
work with a PostgreSQL database. It does not require the PostgreSQL server
package to be installed, as you may well wish to use a remote database
server.

If you want the database to be on the same system as ownCloud itself, you must
also install and enable the PostgreSQL server package. See README.postgresql
for more details.


%package sqlite
Summary:    SQLite 3 database support for ownCloud
Group:      Applications/Internet

Provides:   %{name}-database = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   php-sqlite3 php-pcre

%description sqlite
This package ensures the necessary dependencies are in place for ownCloud to
work with an SQLite 3 database stored on the local system.


%prep
%setup -q -n %{name}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

# prepare package doc
cp %{SOURCE3} README.fedora
cp %{SOURCE4} README.mysql
cp %{SOURCE5} README.postgresql


# Strip bundled libraries from global 3rdparty dir
find  3rdparty -mindepth 1 -maxdepth 1 -type d ! -name composer -exec rm -r "{}" \;

# we need to symlink some annoying files back here, though...direct file
# autoloading sucks. "files" sections of "autoload" statements in
# composer.json files cause composer to basically hardcode the path to a
# given file and require that exact path *every time the autoloader is
# invoked*: I can't see an elegant way around that. "classmap" does much
# the same. If we unbundle *all* of the 'files' or 'classmap' bundled
# deps in such a way that they're laid out exactly the same as upstream
# relative to /usr/share/php, then instead of doing this we could patch
# $vendorDir in the composer loader files to be /usr/share/php.
mkdir -p 3rdparty/natxet/CssMin/src
mkdir -p 3rdparty/james-heinrich/getid3/getid3
mkdir -p 3rdparty/swiftmailer/swiftmailer/lib
mkdir -p 3rdparty/ircmaxell/password-compat/lib
mkdir -p 3rdparty/react/promise/src

# individual core apps now bundle libs as well - yay
rm -rf apps/files_external/3rdparty/{icewind,Dropbox,google-api-php-client,aws-sdk-php,composer*}

# create autoloader, from composer.json, "require": {
#                "icewind/smb": "1.0.4",
#                "icewind/streams": "0.2"
cat << 'EOF' | tee apps/files_external/3rdparty/autoload.php
<?php
require_once '%{_datadir}/php/Icewind/Streams/autoload.php';
require_once '%{_datadir}/php/Icewind/SMB/autoload.php';
EOF

# clean up content
for f in {l10n.pl,init.sh,setup_owncloud.sh,image-optimization.sh,install_dependencies.sh}; do
    find . -name "$f" -exec rm {} \;
done
find . -size 0 -type f -exec rm {} \;

# Drop pre-compiled binary lumps: Flash and Silverlight
# This means that Flash/Silverlight video/audio fallbacks in the
# 'media' and 'videoviewer' apps are not available.
# To re-introduce these they would have to be built from the
# source as part of this package build, they cannot be shipped
# pre-compiled. - AdamW, 2013/08
# https://fedoraproject.org/wiki/Packaging:Guidelines#No_inclusion_of_pre-built_binaries_or_libraries
rm apps/files_videoviewer/js/flashmediaelement.swf
rm apps/files_videoviewer/js/silverlightmediaelement.xap

# let's not ship upstream's 'updater' app, which has zero chance of working and
# a big chance of blowing things up
rm -r apps/updater


%check
nb=$(ls %{buildroot}%{_datadir}/%{name}/apps/files_external/3rdparty | wc -l)
if [ $nb -gt 1  ]; then
  false apps/files_external/3rdparty must only have autoload.php
fi

if grep -r 3rdparty %{buildroot}%{_datadir}/%{name}/apps/files_external \
   | grep -v 3rdparty/autoload.php; then
   false Patch needs to be adapted
fi

php %{buildroot}%{_datadir}/%{name}/apps/files_external/3rdparty/autoload.php



%build
# Nothing to build


%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_datadir}/%{name}

# create owncloud datadir
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/data
# create writable app dir for appstore
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/apps
# create owncloud sysconfdir
mkdir -p %{buildroot}%{_sysconfdir}/%{name}

# install content
for d in $(find . -mindepth 1 -maxdepth 1 -type d | grep -v config); do
    cp -a "$d" %{buildroot}%{_datadir}/%{name}
done

for f in {*.php,*.xml,*.html,occ,robots.txt}; do
    install -pm 644 "$f" %{buildroot}%{_datadir}/%{name} 
done

# symlink config dir
ln -sf %{_sysconfdir}/%{name} %{buildroot}%{_datadir}/%{name}/config

# Owncloud looks for ca-bundle.crt in config dir
ln -sf %{_sysconfdir}/pki/tls/certs/ca-bundle.crt %{buildroot}%{_sysconfdir}/%{name}/ca-bundle.crt

# set default config
install -pm 644 %{SOURCE7}    %{buildroot}%{_sysconfdir}/%{name}/config.php

# httpd config
install -Dpm 644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
install -Dpm 644 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}-access.conf.avail
install -Dpm 644 %{SOURCE100} %{SOURCE101} %{SOURCE102} %{SOURCE103} \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/

# nginx config
install -Dpm 644 %{SOURCE6} \
    %{buildroot}%{_sysconfdir}/nginx/conf.d/%{name}.conf

# symlink 3rdparty libs - if possible
# global
ln -s %{_datadir}/php/natxet/CssMin/src/CssMin.php %{buildroot}%{_datadir}/%{name}/3rdparty/natxet/CssMin/src/
ln -s %{_datadir}/php/getid3/getid3.php %{buildroot}%{_datadir}/%{name}/3rdparty/james-heinrich/getid3/getid3/
ln -s %{_datadir}/php/Swift/swift_required.php %{buildroot}%{_datadir}/%{name}/3rdparty/swiftmailer/swiftmailer/lib/swift_required.php
ln -s %{_datadir}/php/password_compat/password.php %{buildroot}%{_datadir}/%{name}/3rdparty/ircmaxell/password-compat/lib/password.php
ln -s %{_datadir}/php/React/Promise/functions_include.php  %{buildroot}%{_datadir}/%{name}/3rdparty/react/promise/src/functions_include.php


%if 0%{?rhel} < 7
%post
semanage fcontext -a -t httpd_sys_rw_content_t '%{_sysconfdir}/%{name}/config.php' 2>/dev/null || :
semanage fcontext -a -t httpd_sys_rw_content_t '%{_sysconfdir}/%{name}' 2>/dev/null || :
semanage fcontext -a -t httpd_sys_rw_content_t '%{_localstatedir}/lib/%{name}(/.*)?' 2>/dev/null || :
restorecon -R %{_sysconfdir}/%{name} || :
restorecon -R %{_localstatedir}/lib/%{name} || :

%postun
if [ $1 -eq 0 ] ; then
semanage fcontext -d -t httpd_sys_rw_content_t '%{_sysconfdir}/%{name}/config.php' 2>/dev/null || :
semanage fcontext -d -t httpd_sys_rw_content_t '%{_sysconfdir}/%{name}' 2>/dev/null || :
semanage fcontext -d -t httpd_sys_rw_content_t '%{_localstatedir}/lib/%{name}(/.*)?' 2>/dev/null || :
fi
%endif


%post httpd
%if 0%{?fedora} || 0%{?rhel} > 6
/usr/bin/systemctl reload httpd.service > /dev/null 2>&1 || :
%else
/sbin/service httpd reload > /dev/null 2>&1 || :
%endif

%postun httpd
if [ $1 -eq 0 ]; then
%if 0%{?fedora} || 0%{?rhel} > 6
  /usr/bin/systemctl reload httpd.service > /dev/null 2>&1 || :
%else
  /sbin/service httpd reload > /dev/null 2>&1 || :
%endif
fi

%post nginx
%if 0%{?fedora} || 0%{?rhel} > 6
  /usr/bin/systemctl reload nginx.service > /dev/null 2>&1 || :
  /usr/bin/systemctl reload php-fpm.service > /dev/null 2>&1 || :
%else
  /sbin/service nginx reload > /dev/null 2>&1 || :
  /sbin/service php-fpm reload > /dev/null 2>&1 || :
%endif

%postun nginx
if [ $1 -eq 0 ]; then
%if 0%{?fedora} || 0%{?rhel} > 6
  /usr/bin/systemctl reload nginx.service > /dev/null 2>&1 || :
  /usr/bin/systemctl reload php-fpm.service > /dev/null 2>&1 || :
%else
  /sbin/service nginx reload > /dev/null 2>&1 || :
  /sbin/service php-fpm reload > /dev/null 2>&1 || :
%endif
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING-AGPL README.fedora config/config.sample.php

%dir %attr(-,apache,apache) %{_sysconfdir}/%{name}
# contains sensitive data (dbpassword, passwordsalt)
%config(noreplace) %attr(0600,apache,apache) %{_sysconfdir}/%{name}/config.php
# need the symlink in confdir but it's not config
%{_sysconfdir}/%{name}/ca-bundle.crt

%{_datadir}/%{name}
%dir %attr(0755,apache,apache) %{_localstatedir}/lib/%{name}
# user data must not be world readable
%dir %attr(0750,apache,apache) %{_localstatedir}/lib/%{name}/data
%attr(-,apache,apache) %{_localstatedir}/lib/%{name}/apps


%files httpd
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_sysconfdir}/httpd/conf.d/%{name}-access.conf.avail
%{_sysconfdir}/httpd/conf.d/*.inc

%files nginx
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nginx/conf.d/%{name}.conf

%files mysql
%defattr(-,root,root,-)
%doc README.mysql

%files postgresql
%defattr(-,root,root,-)
%doc README.postgresql

%files sqlite
%defattr(-,root,root,-)


%changelog
* Fri Apr 01 2016 James Hogarth <james.hogarth@gmail.com> - 8.2.3-4
- Update to new dependency versions now packaged
- Add fedora autoloader based external_files 
- Add patch to fix bz#1321417

* Thu Mar 24 2016 James Hogarth <james.hogarth@gmail.com> - 8.2.3-3
- Add typical appstore issue to readme
- Clean up spec to make it easier to follow the requires from unbundling

* Wed Mar 23 2016 Remi Collet <remi@fedoraproject.org> - 8.2.3-2
- use php-swift-Swift 5.4 in /usr/share/php
- fix patch to not update .htaccess
- drop samba dependency on old EL

* Tue Mar 22 2016 James Hogarth <james.hogarth@gmail.com> - 8.2.3-2
- Add smbclient dependency so that shipped external storage works as expected
- Add some data to the Fedora readme

* Mon Mar 14 2016 James Hogarth <james.hogarth@gmail.com> - 8.2.3-1
- new release 8.2.3

* Mon Mar 14 2016 Remi Collet <remi@fedoraproject.org> - 8.1.6-1
- Update to 8.1.6
- fix autoloader to ensure sabre/vobject 3.4 is used

* Sat Feb 20 2016 James Hogarth <james.hogarth@gmail.com> - 8.1.5-1
- Update to 8.1.5

* Mon Jan 11 2016 Adam Williamson <awilliam@redhat.com> - 8.0.10-1
- new release 8.0.10 (multiple security fixes)

* Wed Nov 04 2015 Adam Williamson <awilliam@redhat.com> - 8.0.9-1
- new release 8.0.9 (with security fixes)

* Fri Sep 18 2015 Adam Williamson <awilliam@redhat.com> - 8.0.8-1
- new release 8.0.8

* Wed Sep 02 2015 Adam Williamson <awilliam@redhat.com> - 8.0.7-1
- new release 8.0.7

* Fri Jul 10 2015 Adam Williamson <awilliam@redhat.com> - 8.0.5-1
- new release 8.0.5 (should fix app enabling, RHBZ #1240776)
- patch to use Google lib autoloader

* Sun Jul  5 2015 Remi Collet <remi@remirepo.net> - 8.0.4-3
- backport for remirepo

* Sat Jul 04 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 8.0.4-3
- Fix Symfony max version (2.6 changed to 3.0)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Adam Williamson <awilliam@redhat.com> - 8.0.4-1
- new release 8.0.4

* Mon May 04 2015 Adam Williamson <awilliam@redhat.com> - 8.0.3-2
- disable the htaccess fiddling stuff harder

* Fri May 01 2015 Adam Williamson <awilliam@redhat.com> - 8.0.3-1
- new release 8.0.3

* Sat Apr 25 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org>
- Fix nginx conf to serve static apps-appstore

* Fri Apr 24 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org>
- Use php handler from php-fpm nginx conf

* Sun Mar 15 2015 Adam Williamson <awilliam@redhat.com> - 8.0.2-1
- new release 8.0.2

* Fri Mar 06 2015 Adam Williamson <awilliam@redhat.com> - 8.0.1-0.2.rc1
- backport some significant app store fixes from upstream stable8

* Fri Mar 06 2015 Adam Williamson <awilliam@redhat.com> - 8.0.1-0.1.rc1
- update to 8.0.1rc1

* Mon Feb 23 2015 Adam Williamson <awilliam@redhat.com> - 8.0.0-6
- extend the htaccess patch to cover updater as well as initial setup
- rebase apache config stuff again, private dir denials only on 8.x branch

* Mon Feb 23 2015 Adam Williamson <awilliam@redhat.com> - 8.0.0-5
- simplify dropbox autoloader patch (just drop it entirely a la AWS)

* Mon Feb 23 2015 Adam Williamson <awilliam@redhat.com> - 8.0.0-4
- unbundle php-natxet-cssmin, add getid3 to the list of symlink hacks

* Mon Feb 23 2015 Adam Williamson <awilliam@redhat.com> - 8.0.0-3
- merge second version of Apache/Nginx config changes into 8.x build
- backport upstream PR #14119 to fix OC for DBAL 2.5.1

* Sun Feb 22 2015 Adam Williamson <awilliam@redhat.com> - 7.0.4-3
- revise and strengthen Apache configuration layout, fix external apps
- fix external apps for Nginx

* Sun Feb 22 2015 Adam Williamson <awilliam@redhat.com> - 8.0.0-2
- Initial version of Apache/Nginx config changes later re-done in 7.0.4-3

* Sat Feb 21 2015 Adam Williamson <awilliam@redhat.com> - 8.0.0-1
- new release 8.0.0
- rediff patches, adjust for new bundled libs, etc etc

* Sat Dec 20 2014 Adam Williamson <awilliam@redhat.com> - 7.0.4-2
- backport upstream support for google PHP lib 1.x and unbundle it

* Tue Dec 09 2014 Adam Williamson <awilliam@redhat.com> - 7.0.4-1
- new release 7.0.4

* Tue Nov 25 2014 Adam Williamson <awilliam@redhat.com> - 7.0.3-3
- fix dropbox autoload patch (thanks Tomas Dolezal) #1168082

* Tue Nov 11 2014 Adam Williamson <awilliam@redhat.com> - 7.0.3-2
- drop unnecessary bits from 3rdparty_includes.patch
- split Dropbox loading changes into a separate patch (submitted upstream)

* Mon Nov 10 2014 Adam Williamson <awilliam@redhat.com> - 7.0.3-1
- new release 7.0.3

* Wed Oct 29 2014 Adam Williamson <awilliam@redhat.com> - 7.0.2-4
- db sub-packages should not depend on db server packages
- improve README
- improve db sub-package descriptions
- don't check for new versions or working .htaccess files

* Tue Oct 28 2014 Adam Williamson <awilliam@redhat.com> - 7.0.2-3
- drop unnecessary deps: php-gmp (#1152438) and Net_Curl(#999720)
- re-arrange deps in spec to be the way I like 'em

* Tue Sep 09 2014 Adam Williamson <awilliam@redhat.com> - 7.0.2-2
- 10927.patch: backport fix for an upgrade bug (upstream #10762)

* Thu Aug 28 2014 Adam Williamson <awilliam@redhat.com> - 7.0.2-1
- update to 7.0.2
- update patch for using Composer autoloader with 3rdparty deps

* Wed Aug 20 2014 Adam Williamson <awilliam@redhat.com> - 7.0.1-2
- make php directives in httpd config conditional on mod_php (FPM compat)

* Wed Aug 20 2014 Adam Williamson <awilliam@redhat.com> - 7.0.1-1
- update to 7.0.1
- drop contact_type.patch (merged upstream)

* Tue Jul 29 2014 Adam Williamson <awilliam@redhat.com> - 7.0.0-6
- do not ship upstream's 'updater' app (it'll only lead to tears)
- don't patch and ship OC's sample config, write a stub instead

* Tue Jul 29 2014 Adam Williamson <awilliam@redhat.com> - 7.0.0-5
- fix up sabre paths right this time

* Tue Jul 29 2014 Adam Williamson <awilliam@redhat.com> - 7.0.0-4
- more autoloader tweaking
- use composer not OC autoloader for legacy 3rdparty includes (core#9643)
- specify explicit paths to Sabre deps

* Sun Jul 27 2014 Adam Williamson <awilliam@redhat.com> - 7.0.0-3
- update apache config for OC 7 changes
- drop unneeded isoft/mssql-bundle from 3rdparty

* Sun Jul 27 2014 Adam Williamson <awilliam@redhat.com> - 7.0.0-2
- opcache_invalidate.patch: avoid triggering a crash in the PHP opcache
- contact_type.patch: fix selection of current field type in contact view

* Thu Jul 24 2014 Adam Williamson <awilliam@redhat.com> - 7.0.0-1
- 7.0.0
- rediff 3rdparty_includes.patch
- update 3rdparty strip commands and dependencies for upstream changes
- update dependencies

* Mon Jun 30 2014 Gregor Tätzner <brummbq@fedoraproject.org> - 6.0.4-1
- 6.0.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 01 2014 Gregor Tätzner <brummbq@fedoraproject.org> - 6.0.3-1
- 6.0.3
- update symfony routing patch

* Tue Mar 04 2014 Gregor Tätzner <brummbq@fedoraproject.org> - 6.0.2-1
- 6.0.2

* Mon Feb 24 2014 Adam Williamson <awilliam@redhat.com> - 6.0.1-3
- set a minimum ver on the DBAL req for safety (using with 2.3 is dangerous)

* Mon Jan 27 2014 Adam Williamson <awilliam@redhat.com> - 6.0.1-2
- unbundle phpseclib (packaged now)

* Thu Jan 23 2014 Gregor Tätzner <brummbq@fedoraproject.org> - 6.0.1-1
- 6.0.1

* Tue Jan 14 2014 Gregor Tätzner <brummbq@fedoraproject.org>  - 6.0.0a-9
- fix routing with symfony 2.3

* Fri Jan 10 2014 Adam Williamson <awilliam@redhat.com> - 6.0.0a-8
- make a warning OC keeps triggering into a debug message

* Thu Jan  9 2014 Adam Williamson <awilliam@redhat.com> - 6.0.0a-7
- re-enable irods, patch loading of it, add dependency on it

* Fri Jan  3 2014 Adam Williamson <awilliam@redhat.com> - 6.0.0a-6
- disable irods a bit harder

* Fri Jan  3 2014 Adam Williamson <awilliam@redhat.com> - 6.0.0a-5
- drop non-existent OC_User_IMAP from config file

* Fri Jan  3 2014 Adam Williamson <awilliam@redhat.com> - 6.0.0a-4
- apps_3rdparty_includes: fix more 3rdparty loading stuff
- disable_irods: disable storage app's irods (it's broken)

* Mon Dec 30 2013 Adam Williamson <awilliam@redhat.com> - 6.0.0a-3
- tar-include, blowfish-include, dropbox-include: fix more paths

* Mon Dec 30 2013 Adam Williamson <awilliam@redhat.com> - 6.0.0a-2
- dropbox-include.patch: fix loading of system copy of php-Dropbox

* Sun Dec 22 2013 Adam Williamson <awilliam@redhat.com> - 6.0.0a-1
- 6.0.0a

* Sun Dec 22 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 6.0.0-1
- 6.0.0

* Fri Dec 20 2013 Adam Williamson <awilliam@redhat.com> - 5.0.14a-2
- Correct location of php-symfony-routing: #1045301

* Fri Dec 20 2013 Adam Williamson <awilliam@redhat.com> - 5.0.14a-1
- 5.0.14a

* Sat Nov 16 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 5.0.13-1
- 5.0.13

* Tue Oct 08 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 5.0.12-1
- 5.0.12

* Tue Sep 24 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 5.0.11-2
- keep MDB2/pgsql driver, genuine version causes upgrade problems (RBZ#962082)

* Sat Sep 07 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 5.0.11-1
- 5.0.11

* Wed Sep 04 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 5.0.10-4
- unbundle sabredav again

* Fri Aug 23 2013 Adam Williamson <awilliam@redhat.com> - 5.0.10-3
- patch mediaelement not to try and use its plugins

* Fri Aug 23 2013 Adam Williamson <awilliam@redhat.com> - 5.0.10-2
- drop binary Flash and Silverlight blobs: #1000257
- don't ship source of jplayer in the binary package

* Sun Aug 18 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 5.0.10-1
- 5.0.10

* Thu Aug 15 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.5.13-2
- RBZ #962082 keep 3rdparty pqsql mdb2 driver

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 5.0.9-2
- buildreq: php-pear (RBZ #987279)

* Tue Jul 16 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 5.0.9-1
- major upgrade to 5.0.9
- symlink 3rdparty libs and drop most of the patches
- new deps: php-ZendFramework symfony

* Sat Jun 08 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.5.12-1
- 4.5.12

* Thu May 16 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.5.11-2
- RBZ #963701: require mdb2-mysql not mysqli

* Thu May 16 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.5.11-1
- 4.5.11

* Tue Apr 23 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.5.10-1
- 4.5.10

* Sat Apr 13 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.5.9-1
- 4.5.9
- disable remote access by default

* Fri Mar 15 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.5.8-1
- 4.5.8
- unbundle dropbox-php
- log to syslog
- include nginx config

* Mon Feb 25 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.5.7-2
- added script for re-creating stripped tarball
- new httpd.conf for httpd 2.4

* Sun Feb 24 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.5.7-1
- 4.5.7

* Sun Jan 13 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.8-7
- fixed selinux file context on rhel

* Sat Dec 08 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.8-6
- unbundled phpass and php-when
- added database setup instructions

* Thu Nov 08 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.8-5
- moved included sqlite3 driver to owncloud-sqlite
- unbundled php-cloudfiles
- reworked runtime requirements

* Sun Nov 04 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.8-4
- repacked source tarball (deleted jslint code)

* Sat Nov 03 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.8-3
- added missing licenses
- obliterated jslint code from aceeditor

* Fri Nov 02 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.8-2
- updated license field
- added README.fedora

* Thu Oct 18 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.8-1
- owncloud-4.0.8

* Fri Oct 12 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.7-5
- unbundle php-getid3
- remove conf dir access check

* Tue Oct 02 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.7-4
- require rsyslog
- switched log type back to 'owncloud'

* Sun Sep 23 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.7-3
- unbundled Archive/Tar.php, Guess.php, phpmailer
- created virtual packages for supported databases
- added logrotate script

* Thu Sep 20 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.7-2
- moved httpd files and sciptlets into own subpackage
- redirected log output to /var/log/owncloud.log
- deleted unecessary files

* Wed Sep 19 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 4.0.7-1
- updated to version 4.0.7

* Fri Apr 06 2012 Felix Kaechele <heffer@fedoraproject.org> - 3.0.1-1
- initial package

