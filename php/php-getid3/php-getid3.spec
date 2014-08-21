%global date 20140511

Name:      php-getid3
Version:   1.9.8
Release:   2%{?dist}
Epoch:     1
License:   LGPLv3+
Summary:   The PHP media file parser
Group:     Development/Libraries
URL:       http://getid3.sourceforge.net/
Source0:   http://downloads.sourceforge.net/getid3/getID3-%{version}-%{date}.zip

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# from composer.json
#        "php": ">=5.3.0"
Requires:  php(language) >= 5.3.0
# from phpcompatinfo for version 1.9.8
Requires:  php-ctype
Requires:  php-date
Requires:  php-exif
Requires:  php-gd
Requires:  php-iconv
Requires:  php-pcre
Requires:  php-xml
# Optional: dba, mysql, sqlite3, rar

Provides:  php-composer(james-heinrich/getid3) = %{version}


%description
getID3() is a PHP script that extracts useful information 
(such as ID3 tags, bitrate, playtime, etc.) from MP3s & 
other multimedia file formats (Ogg, WMA, WMV, ASF, WAV, AVI, 
AAC, VQF, FLAC, MusePack, Real, QuickTime, Monkey's Audio, MIDI and more).


%prep
%setup -q -c
for i in ./*.txt licenses/*.txt demos/*.php; do
      iconv -f iso-8859-1 -t utf-8 < "$i" > "${i}_"
      touch -r "$i" "${i}_"
      mv "${i}_" "$i"
done
sed -i 's/\r//' demos/index.php
sed -i 's/\r//' changelog.txt


%build


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/php
cp -a getid3 %{buildroot}%{_datadir}/php/


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc changelog.txt dependencies.txt readme.txt structure.txt demos
%doc composer.json
%{?_licensedir:%license licenses/*}
%{!?_licensedir:%doc licenses}
%{_datadir}/php/getid3


%changelog
* Thu Aug 21 2014 Remi Collet <remi@fedoraproject.org> - 1:1.9.8-2
- fix minimal PHP version
- add explicit dependencies for all php extensions
- fix license handling
- provides php-composer(james-heinrich/getid3)

* Wed Aug 20 2014 Adam Williamson <awilliam@redhat.com> - 1:1.9.8-1
- new release 1.9.8

* Sun Sep  8 2013 Remi Collet <RPMS@famillecollet.com> - 1:1.9.7-1
- backport 1.9.7 for remi repo

* Sun Sep 08 2013 Roma <roma@lcg.ufrj.br> - 1:1.9.7-1
- Updated to 1.9.7
- Changed license to LGPLv3+

* Sun Nov 25 2012 Remi Collet <RPMS@famillecollet.com> - 1:1.9.3-1
- backport 1.9.3 for remi repo

* Sun Oct 07 2012 Paulo Roma <roma@lcg.ufrj.br> - 1:1.9.3-1
- Downgraded to latest stable version.
- Got needed extensions by using:
  phpci print --recursive --report extension /usr/share/php/getid3/
- Added BR php-gd.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0b5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0b5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild


* Fri Jul 31 2009 Paulo Roma <roma@lcg.ufrj.br> 2.0.0b5-2
- Updated ampache patch.

* Thu Jun 04 2009 Paulo Roma <roma@lcg.ufrj.br> 2.0.0b5-1
- Updated to 2.0.0b5
- Patched with ampache fixes.

* Thu Jun 04 2009 Paulo Roma <roma@lcg.ufrj.br> 1.7.9-1
- Initial spec file.
