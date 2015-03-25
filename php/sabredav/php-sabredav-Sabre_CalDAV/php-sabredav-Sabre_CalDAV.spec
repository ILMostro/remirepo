%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name   Sabre_CalDAV
%global channelname pear.sabredav.org
%global mainver     1.7.13
%global reldate     2014-07-28

Name:           php-sabredav-Sabre_CalDAV
Epoch:          1
Version:        1.7.9
Release:        2%{?dist}
Summary:        Provides RFC4791 (CalDAV) support to Sabre_DAV

Group:          Development/Libraries
License:        BSD
URL:            http://sabre.io
Source0:        https://github.com/fruux/sabre-dav/releases/download/%{mainver}/sabredav-%{mainver}.zip
Source1:        %{name}.xml

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(%{channelname})

Requires(post): %{__pear}
Requires(postun): %{__pear}

Requires:       php-pdo
Requires:       php-xml
Requires:       php-pear(PEAR)
Requires:       php-channel(%{channelname})
Requires:       php-pear(%{channelname}/Sabre)         >= 1.0.2
Requires:       php-pear(%{channelname}/Sabre_DAV)     >= 1.7.13
Requires:       php-pear(%{channelname}/Sabre_DAVACL)  >= 1.7.9
Requires:       php-pear(%{channelname}/Sabre_VObject) >= 2.1.3

Provides:       php-pear(%{pear_name}) = %{version}
Provides:       php-pear(%{channelname}/%{pear_name}) = %{version}

%description
CalDAV plugin for Sabre, adds support for CalDAV in Sabre_DAV.

%prep
%setup -q -n SabreDAV

sed -e 's/@VERSION@/%{version}/' \
    -e 's/@RELDATE@/%{reldate}/' \
    %{SOURCE1} >%{name}.xml
mv lib/Sabre Sabre

# Check version
extver=$(sed -n "/VERSION/{s/.* '//;s/'.*$//;p}" Sabre/CalDAV/Version.php)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

# Check files
touch error.lst
for fic in $(find Sabre/CalDAV -type f)
do
  grep $fic %{name}.xml || echo -$fic >> error.lst
done

for fic in $(grep '<file' %{name}.xml | sed -e 's/.*name="//' -e 's/".*//')
do
  [ -f $fic ] || echo +$fic >> error.lst
done

if [ -s error.lst ]; then
  : Error in %{name}.xml
  cat error.lst
  exit 1
fi


%build
# Empty build section, most likely nothing required.


%install
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Sabre/CalDAV


%changelog
* Tue Oct 28 2014 Adam Williamson <awilliam@redhat.com> - 1.7.9-2
- new release 1.7.9 (from SabreDAV 1.7.13, EOL)

* Thu Feb 20 2014 Remi Collet <RPMS@FamilleCollet.com> 1:1.7.9-1
- revert to 1.7

* Sat Oct  5 2013 Remi Collet <RPMS@FamilleCollet.com> 1.8.7-1
- update to 1.8.7

* Thu Sep 12 2013 Remi Collet <RPMS@FamilleCollet.com> 1.8.6-2
- fix roles

* Wed Jun 19 2013 Remi Collet <RPMS@FamilleCollet.com> 1.8.6-1
- update to 1.8.6

* Tue May  7 2013 Remi Collet <RPMS@FamilleCollet.com> 1.8.3-1
- update to 1.8.3
  use our own package.xml as upstream doesn't use pear anymore

* Mon Nov 12 2012 Remi Collet <RPMS@FamilleCollet.com> 1.6.4-3
- backport for remi repo

* Wed Oct 31 2012 Joseph Marrero <jmarrero@fedoraproject.org> 1.6.4-3
- Added required deps pointed out by phpci
* Tue Oct 23 2012 Joseph Marrero <jmarrero@fedoraproject.org> 1.6.4-2
- remove uncesary changes of directory
- change define to global
- fix documentation directory
- Fix description
* Thu Aug 30 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.6.4-1
- update
* Fri Apr 06 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.6.1-1
- initial package
