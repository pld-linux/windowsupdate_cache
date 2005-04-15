Summary:	WindowsUpdate Cache
Summary(pl):	Proxy-Cache dla Windows Update
Name:		windowsupdate_cache
Version:	20050414
Release:	0.2
Epoch:		0
License:	freeware
Vendor:		windowsupdate@glob.com.au
Group:		Applications
Source0:	http://glob.com.au/windowsupdate_cache/windowsupdate_cache.tar.gz
# Source0-md5:	f655b9c7704162cb41013de9cc335d27
Source1:	%{name}-apache_config
URL:		http://glob.com.au/windowsupdate_cache
Requires:	perl-TimeDate
Requires:	squid
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
These scripts are what I use to permanently cache downloads from
Microsoft (including Windows Update). Note that this does not "clone"
windowsupdate, rather it only stops you re-downloading files that have
already been fetched (ie. it's a cache not a clone).
Please read included README file for setup instructions.

%description -l pl
S± to skrypty u¿ywane przez autora do cache'owania plików z witryny
Microsoftu (w³±czaj±c Windows Update). Nale¿y zauwa¿yæ, ¿e to nie jest
"klon" serwisu windowsupdate, tylko prosty sposób na nie ¶ci±ganie
ponownie plików, które s± ju¿ w magazynie.
Proszê przeczytaæ za³±czony plik README z instrukcj± u¿ycia.

%package apachestorage
Summary:	WindowsUpdate Cache
Summary(pl):	Proxy-Cache dla Windows Update
Group:		Applications
Requires:	webserver = apache

%description apachestorage
This is apache-based storage for windowsupdate_cache.

%description apachestorage -l pl
To jest bazuj±cy na apache magazyn dla windowsupdate_cache.

%prep
%setup -q -n %{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}} \
	$RPM_BUILD_ROOT/var/cache/windowsupdate_cache/storage

install {check_store,redir.pl} $RPM_BUILD_ROOT%{_bindir}
install download $RPM_BUILD_ROOT/var/cache/windowsupdate_cache/storage/download
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin apachestorage -- apache1 >= 1.3.33-2
%{?debug:set -x; echo "triggerin apache1 %{name}-%{version}-%{release} 1:[$1]; 2:[$2]"}
if [ "$1" = "1" ] && [ "$2" = "1" ] && [ -d /etc/apache/conf.d ]; then
	ln -sf %{_sysconfdir}/%{name}.conf /etc/apache/conf.d/99_%{name}.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
else
	# restart apache if the config symlink is there
	if [ -L /etc/apache/conf.d/99_%{name}.conf ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%triggerun apachestorage -- apache1 >= 1.3.33-2
%{?debug:set -x; echo "triggerun apache1 %{name}-%{version}-%{release}: 1:[$1]; 2:[$2]"}
# remove link if eighter of the packages are gone
if [ "$1" = "0" ] || [ "$2" = "0" ]; then
	if [ -L /etc/apache/conf.d/99_%{name}.conf ]; then
		rm -f /etc/apache/conf.d/99_%{name}.conf
		if [ -f /var/lock/subsys/apache ]; then
			/etc/rc.d/init.d/apache restart 1>&2
		fi
	fi
fi

%triggerin apachestorage -- apache >= 2.0.0
%{?debug:set -x; echo "triggerin apache2 %{name}-%{version}-%{release}: 1:[$1]; 2:[$2]"}
if [ "$1" = "1" ] && [ "$2" = "1" ] && [ -d /etc/httpd/httpd.conf ]; then
	ln -sf %{_sysconfdir}/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
else
	# restart apache if the config symlink is there
	if [ -L /etc/httpd/httpd.conf/99_%{name}.conf ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%triggerun apachestorage -- apache >= 2.0.0
%{?debug:set -x; echo "triggerun apache2 %{name}-%{version}-%{release}: 1:[$1]; 2:[$2]"}
# remove link if eighter of the packages are gone
if [ "$1" = "0" ] || [ "$2" = "0" ]; then
	if [ -L /etc/httpd/httpd.conf/99_%{name}.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
		if [ -f /var/lock/subsys/httpd ]; then
			/etc/rc.d/init.d/httpd restart 1>&2
		fi
	fi
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*

%files apachestorage
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
/var/cache/windowsupdate_cache
