%global pluginname   pdf
#global svnrelease   315

Name:           glpi-pdf
Version:        0.84.1
%if 0%{?svnrelease}
Release:        0.1.svn%{svnrelease}%{?dist}
%else
Release:        1%{?dist}
%endif
Summary:        GLPI Plugin to print PDF of equipment
Summary(fr):    Extension GLPI pour créer des PDF des matériels

Group:          Applications/Internet
License:        GPLv2+
URL:            https://forge.indepnet.net/projects/pdf

%if 0%{?svnrelease}
# svn export -r 315 https://forge.indepnet.net/svn/pdf/trunk pdf
# tar czf glpi-pdf-0.83-315.tar.gz pdf
Source0:        glpi-pdf-0.83-%{svnrelease}.tar.gz
%else
Source0:        https://forge.indepnet.net/attachments/download/1730/glpi-pdf-0.84.1.tar.gz
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext

Requires:       glpi >= 0.84
Requires:       glpi <  0.85


%description
This GLPI plugin enables you to print, in pdf format, the information 
sheet of an equipment or a software of the inventory. 


%description -l fr
Cette extension GLPI vous permet de créer un PDF contenant toutes les
informations sur un équipement ou un logiciel de l'inventaire.


%prep
%setup -q -c

# Fix version
sed -e "/'version'/s/'0.84'/'0.84.1'/" -i %{pluginname}/setup.php

# dos2unix to avoid rpmlint warnings
mv %{pluginname}/docs docs
for doc in docs/* ; do
    sed -i -e 's/\r//' $doc
done


%build
# Regenerate the locales
for po in %{pluginname}/locales/*.po
do
   msgfmt $po -o $(dirname $po)/$(basename $po .po).mo
done


%install
rm -rf %{buildroot} 

mkdir -p %{buildroot}/%{_datadir}/glpi/plugins
cp -ar %{pluginname} %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}

for i in %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}/locales/*
do
  lang=$(basename $i)
  echo "%lang(${lang:0:2}) %{_datadir}/glpi/plugins/%{pluginname}/locales/${lang}"
done | tee %{name}.lang


%clean
rm -rf %{buildroot} 


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc docs/* %{pluginname}/LICENSE
%dir %{_datadir}/glpi/plugins/%{pluginname}
%dir %{_datadir}/glpi/plugins/%{pluginname}/locales
%{_datadir}/glpi/plugins/%{pluginname}/*.php
%{_datadir}/glpi/plugins/%{pluginname}/fonts
%{_datadir}/glpi/plugins/%{pluginname}/front
%{_datadir}/glpi/plugins/%{pluginname}/inc
%{_datadir}/glpi/plugins/%{pluginname}/pics
# Keep here as required from interface
%{_datadir}/glpi/plugins/%{pluginname}/LICENSE


%changelog
* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 0.84.1-1
- version 0.84.1
  https://forge.indepnet.net/projects/pdf/versions/1019

* Wed Feb 12 2014 Remi Collet <remi@fedoraproject.org> - 0.84-1
- version 0.84 for GLPI 0.84
  https://forge.indepnet.net/projects/pdf/versions/941

* Thu Apr 19 2012 Remi Collet <Fedora@FamilleCollet.com> - 0.83-2
- add patch for 0.83.1 (Problem tab on various object)

* Fri Apr 06 2012 Remi Collet <Fedora@FamilleCollet.com> - 0.83-1
- version 0.83
  https://forge.indepnet.net/projects/pdf/versions/615

* Sun Feb 26 2012 Remi Collet <Fedora@FamilleCollet.com> - 0.83-0.1.svn315
- update to 0.83 for glpi 0.83 RC (svn snapshot)

* Tue Sep 20 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.80.3-1
- version 0.80.3
  https://forge.indepnet.net/projects/pdf/versions/617

* Tue Jul 19 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.80-1
- update to 0.80 (version have change from 0.8.0)

* Tue Jun 28 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.8.0-0.1.svn259
- update to 0.8.0 for glpi 0.80 RC (svn snapshot)

* Sat Jun 11 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.7.2-1
- version 0.7.2
  https://forge.indepnet.net/projects/pdf/versions/550

* Sat Jan 22 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.7.1-1
- version 0.7.1

* Tue Oct 12 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.7.0-1
- version 0.7.0 and GLPI 0.78 released

* Sat Sep 18 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.7.0-0.1.svn194
- new snapshot

* Tue Aug 10 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.7.0-0.1.svn190
- new snapshot

* Thu Jul 08 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.7.0-0.1.svn189
- new snapshot

* Tue Jun 15 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.7.0-0.1.svn188
- update to 0.7.0 for glpi 0.78 RC (svn snapshot)

* Fri May 21 2010 Remi Collet <Fedora@FamilleCollet.com> - 0.6.1-2
- spec cleanup

* Tue Aug 18 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.6.1-1
- update to 0.6.1 finale for glpi 0.72

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jul 12 2008 Remi Collet <Fedora@FamilleCollet.com> - 0.5-1
- update to 0.5 finale for glpi 0.71

* Thu Dec 27 2007 Remi Collet <Fedora@FamilleCollet.com> - 0.4-1
- update to 0.4 finale
- Initial RPM for Fedora review

* Sun Nov 11 2007 Remi Collet <RPMS@FamilleCollet.com> - 0.4-0.20071111
- update from SVN

* Sun Sep 23 2007 Remi Collet <RPMS@FamilleCollet.com> - 0.3-0.20070922
- new SVN snapshot

* Mon Aug 13 2007 Remi Collet <RPMS@FamilleCollet.com> - 0.2-0.20070813
- Initial RPM

