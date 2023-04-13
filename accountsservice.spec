#
# Conditional build:
%bcond_with	elogind		# elogind support (instead of systemd)
%bcond_without	systemd		# systemd support
%bcond_without	static_libs	# static library

%if %{with elogind}
%undefine	with_systemd
%endif
Summary:	D-Bus interface for user accounts management
Summary(pl.UTF-8):	Interfejs D-Bus do zarządzania kontami użytkowników
Name:		accountsservice
Version:	23.13.9
Release:	1
License:	GPL v3+
Group:		Applications/System
Source0:	https://www.freedesktop.org/software/accountsservice/%{name}-%{version}.tar.xz
# Source0-md5:	03dccfe1b306b7ca19743e86d118e64d
URL:		https://cgit.freedesktop.org/accountsservice/
BuildRequires:	dbus-devel >= 1.9.18
BuildRequires:	docbook-dtd412-xml
%{?with_elogind:BuildRequires:	elogind-devel >= 229.4}
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.63.5
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk-doc >= 1.15
BuildRequires:	libxcrypt-devel >= 4
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 0.50.0
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.102
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
%{?with_systemd:BuildRequires:	systemd-devel >= 1:209}
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	xmlto
BuildRequires:	xz
Requires(post,preun,postun):	systemd-units >= 1:186
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus >= 1.9.18
Requires:	polkit >= 0.102
Requires:	systemd-units >= 0.38
Suggests:	ConsoleKit
Obsoletes:	accountsservice-systemd < 0.6.15-5
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

%package libs
Summary:	Shared accountsservice library
Summary(pl.UTF-8):	Biblioteka współdzielona accountsservice
Group:		Libraries
Requires:	glib2 >= 1:2.63.5
Requires:	libxcrypt >= 4
Requires:	systemd-libs >= 1:186
Conflicts:	accountsservice < 0.6.39

%description libs
Shared accountsservice library.

%description libs -l pl.UTF-8
Biblioteka współdzielona accountsservice.

%package devel
Summary:	Development files for accountsservice
Summary(pl.UTF-8):	Pliki programistyczne biblioteki accountsservice
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.63.5

%description devel
Development files for accountsservice (headers, GObject API, D-Bus
interface description).

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki accountsservice (pliki nagłówkowe,
API GObject, opis interfejsu D-Bus).

%package static
Summary:	accountsservice static library
Summary(pl.UTF-8):	Statyczna biblioteka accountsservice
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
accountsservice static library.

%description static -l pl.UTF-8
Statyczna biblioteka accountsservice.

%package -n vala-accountsservice
Summary:	accountsservice API for Vala language
Summary(pl.UTF-8):	API accountsservice dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala

%description -n vala-accountsservice
accountsservice API for Vala language.

%description -n vala-accountsservice -l pl.UTF-8
API accountsservice dla języka Vala.

%package apidocs
Summary:	API documentation for accountsservice
Summary(pl.UTF-8):	Dokumentacja API accountsservice
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
API documentation for accountsservice.

%description apidocs -l pl.UTF-8
Dokumentacja API accountsservice.

%prep
%setup -q

# too hacky, works with bash or pdksh, but not with mksh; override version in hard way
%{__sed} -i -e '2a echo "%{version}" ; exit 0' generate-version.sh

%if %{with static_libs}
%{__sed} -i -e 's/shared_library/library/' src/libaccountsservice/meson.build
%endif

%build
%meson build \
	-Dadmin_group=wheel \
	-Ddocbook=true \
	%{?with_elogind:-Delogind=true} \
	-Dgtk_doc=true \
	-Dsystemdsystemunitdir=%{systemdunitdir}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/accountsservice/interfaces

%ninja_install -C build

%{__rm} $RPM_BUILD_ROOT%{_docdir}/accountsservice/spec/AccountsService.html

%find_lang accounts-service

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post accounts-daemon.service

%preun
%systemd_preun accounts-daemon.service

%postun
%systemd_reload

%triggerpostun -- accountsservice < 0.6.15-5
%systemd_trigger accounts-daemon.service

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f accounts-service.lang
%defattr(644,root,root,755)
%doc AUTHORS README.md TODO build/doc/dbus/AccountsService.html
%attr(755,root,root) %{_libexecdir}/accounts-daemon
%{systemdunitdir}/accounts-daemon.service
%dir %{_datadir}/accountsservice
%dir %{_datadir}/accountsservice/interfaces
%{_datadir}/accountsservice/user-templates
%{_datadir}/dbus-1/system.d/org.freedesktop.Accounts.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.Accounts.service
%{_datadir}/polkit-1/actions/org.freedesktop.accounts.policy
%dir /var/lib/AccountsService
%dir /var/lib/AccountsService/icons
%dir /var/lib/AccountsService/users

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaccountsservice.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libaccountsservice.so.0
%{_libdir}/girepository-1.0/AccountsService-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaccountsservice.so
%{_includedir}/accountsservice-1.0
%{_pkgconfigdir}/accountsservice.pc
%{_datadir}/dbus-1/interfaces/org.freedesktop.Accounts.User.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Accounts.xml
%{_datadir}/gir-1.0/AccountsService-1.0.gir

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libaccountsservice.a
%endif

%files -n vala-accountsservice
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/accountsservice.deps
%{_datadir}/vala/vapi/accountsservice.vapi

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libaccountsservice
