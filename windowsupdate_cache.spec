#
#
Summary:	WindowsUpdate Cache
Summary(pl):	Proxy-Cache dla Windows Update
Name:		windowsupdate_cache
Version:	20050414
Release:	0.1
Epoch:		0
License:	freeware
Vendor:		windowsupdate@glob.com.au
Group:		Applications
#Icon:		-
Source0:	http://glob.com.au/%{name}/windowsupdate_cache.tar.gz
# Source0-md5:	f655b9c7704162cb41013de9cc335d27
Source1:	%{name}-apache_config
#Patch0:		%{name}-what.patch
URL:		http://glob.com.au/windowsupdate_cache
#BuildRequires:	-
#PreReq:		-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires(postun):	-
Requires:	squid
#Requires:	apache
Requires:	Perl-TimeDate
#Provides:	-
#Obsoletes:	-
#Conflicts:	-
BuildArch:	noarch
#ExclusiveArch:  %{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
These scripts are what i use to permanently cache downloads from
microsoft (including windows update). note that this does not "clone"
windowsupdate, rather it only stops you re-downloading files that have
already been fetched (ie. it's a cache not a clone).
Please read included README file for setup instructions.

%description -l pl
S± to skrypty których u¿ywam aby keszowaæ pliki z witryny microsoft
(w³±czaj±c windows update). Zauwa¿ ¿e to nie jest "Klon" serwisu
windowsupdate, to tylko prosty sposób na nie¶ci±ganie ponownie
plików które s± ju¿ w magazynie.
Proszê, przeczytaj za³±czony plik README z instrukcj± u¿ycia.

%package apachestorage
Summary:	WindowsUpdate Cache
Summary(pl):	Proxy-Cache dla Windows Update
Group:		Applications
Requires:	apache

%description apachestorage
This is apache-based storage for windowsupdate_cache

%description apachestorage -l pl
To jest bazuj±cy na apache magazyn dla windowsupdate_cache

%prep
%setup -q -n %{name}
#%patch0 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT/var/cache/windowsupdate_cache/storage/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/

install {check_store,redir.pl} $RPM_BUILD_ROOT%{_bindir}
install download $RPM_BUILD_ROOT/var/cache/windowsupdate_cache/storage/download
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/99.%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README

%attr(755,root,root) %{_bindir}/*

# initscript and its config

%files apachestorage
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd/httpd.conf/99.%{name}.conf
/var/cache/windowsupdate_cache
