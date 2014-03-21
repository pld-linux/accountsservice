Summary:	D-Bus interface for user accounts management
Summary(pl.UTF-8):	Interfejs D-Bus do zarządzania kontami użytkowników
Name:		accountsservice
Version:	0.6.37
Release:	1
License:	GPL v3
Group:		Applications/System
Source0:	http://cgit.freedesktop.org/accountsservice/snapshot/%{name}-%{version}.tar.xz
# Source0-md5:	d4842f2a054459746947f85476144077
URL:		http://cgit.freedesktop.org/accountsservice/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.38.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk-doc >= 1.15
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.102
BuildRequires:	rpmbuild(macros) >= 1.641
BuildRequires:	systemd-devel >= 186
BuildRequires:	tar >= 1:1.22
BuildRequires:	xmlto
BuildRequires:	xz
Requires(post,preun,postun):	systemd-units >= 38
Requires:	polkit >= 0.102
Requires:	systemd-units >= 0.38
Suggests:	ConsoleKit
Obsoletes:	accountsservice-systemd
Obsoletes:	vala-accountsservice
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The AccountsService project provides:
- A set of D-Bus interfaces for querying and manipulating user account
  information.
- An implementation of these interfaces based on the usermod(8),
  useradd(8) and userdel(8) commands.

%description -l pl.UTF-8
Projekt AccountsService dostarcza:
- Zbiór interfejsów D-Bus do odpytywania i manipulowania informacjami
  o kontach użytkowników.
- Implementacje tych interfejsów oparte o komendy usermod(8),
  useradd(8) i userdel(8).

%package devel
Summary:	accountsservice includes, and more
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki accountsservice
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
accountsservice includes, and more

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki accountsservice.

%package static
Summary:	accountsservice static library
Summary(pl.UTF-8):	Statyczna biblioteka accountsservice
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
accountsservice static library.

%description static -l pl.UTF-8
Statyczna biblioteka accountsservice.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__gtkdocize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	XMLTO_FLAGS="--skip-validation" \
	--disable-silent-rules \
	--with-systemdsystemunitdir=%{systemdunitdir} \
	--enable-docbook-docs \
	--enable-admin-group=wheel
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libaccountsservice.la
%{__rm} $RPM_BUILD_ROOT%{_docdir}/accountsservice/spec/AccountsService.html

%find_lang accounts-service

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%systemd_post accounts-daemon.service

%preun
%systemd_preun accounts-daemon.service

%postun
/sbin/ldconfig
%systemd_reload

%triggerpostun -- accountsservice < 0.6.15-5
%systemd_trigger accounts-daemon.service

%files -f accounts-service.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO doc/dbus/AccountsService.html
%attr(755,root,root) %{_libexecdir}/accounts-daemon
%attr(755,root,root) %{_libdir}/libaccountsservice.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libaccountsservice.so.0
%{_libdir}/girepository-1.0/AccountsService-1.0.typelib
/etc/dbus-1/system.d/org.freedesktop.Accounts.conf
%{systemdunitdir}/accounts-daemon.service
%{_datadir}/dbus-1/system-services/org.freedesktop.Accounts.service
%{_datadir}/polkit-1/actions/org.freedesktop.accounts.policy
%dir /var/lib/AccountsService
%dir /var/lib/AccountsService/icons
%dir /var/lib/AccountsService/users

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaccountsservice.so
%{_includedir}/accountsservice-1.0
%{_pkgconfigdir}/accountsservice.pc
%{_datadir}/dbus-1/interfaces/org.freedesktop.Accounts.User.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Accounts.xml
%{_datadir}/gir-1.0/AccountsService-1.0.gir

%files static
%defattr(644,root,root,755)
%{_libdir}/libaccountsservice.a
