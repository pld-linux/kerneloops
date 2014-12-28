#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Tool to automatically collect and submit kernel crash signatures
Name:		kerneloops
Version:	0.12
Release:	2
License:	GPL v2
Group:		Base/Kernel
Source0:	http://www.kerneloops.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	97e611e5b09831cb6ee31c31bf2bc286
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.kerneloops.org
BuildRequires:	curl-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-tools
BuildRequires:	gtk+2-devel
BuildRequires:	libnotify-devel
BuildRequires:	rpmbuild(macros) >= 1.268
%if %{with tests}
%ifnarch %{ix86} %{x8664} ppc ppc64
BuildRequires:	valgrind
%endif
%endif
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the tools to collect kernel crash signatures,
and to submit them to the kerneloops.org website where the kernel
crash signatures get collected and grouped for presentation to the
Linux kernel developers.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -DDBUS_API_SUBJECT_TO_CHANGE"

%{?with_tests:%{__make} tests}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc Changelog
%attr(755,root,root) %{_sbindir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/kerneloops.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
/etc/dbus-1/system.d/kerneloops.dbus
%{_sysconfdir}/xdg/autostart/kerneloops-applet.desktop
%{_datadir}/kerneloops
%attr(755,root,root) %{_bindir}/kerneloops-applet
%{_mandir}/man8/kerneloops.8*
