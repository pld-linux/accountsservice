Summary:	D-Bus interface for user accounts management
Name:		accountsservice
Version:	0.6.4
Release:	0.1
License:	LGPL
Group:		Applications/System
Source0:	http://cgit.freedesktop.org/accountsservice/snapshot/%{name}-%{version}.tar.bz2
# Source0-md5:	274d9167bca65b3f3abfdd5702f6e4fc
URL:		http://cgit.freedesktop.org/accountsservice/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel
BuildRequires:	xmlto
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The AccountsService project provides:
- A set of D-Bus interfaces for querying and manipulating user account
  information.
- An implementation of these interfaces based on the usermod(8),
  useradd(8) and userdel(8) commands.

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
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	XMLTO_FLAGS="--skip-validation" \
	--enable-docbook-docs
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

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f accounts-service.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO doc/dbus/AccountsService.html
/etc/dbus-1/system.d/org.freedesktop.Accounts.conf
%attr(755,root,root) %{_libdir}/accounts-daemon
%{_libdir}/girepository-1.0/AccountsService-1.0.typelib
%attr(755,root,root) %ghost %{_libdir}/libaccountsservice.so.0
%attr(755,root,root) %{_libdir}/libaccountsservice.so.0.0.0
%{_datadir}/dbus-1/interfaces/org.freedesktop.Accounts.User.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Accounts.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.Accounts.service
%{_datadir}/polkit-1/actions/org.freedesktop.accounts.policy

%files devel
%defattr(644,root,root,755)
%{_datadir}/gir-1.0/AccountsService-1.0.gir
%{_pkgconfigdir}/accountsservice.pc
%attr(755,root,root) %{_libdir}/libaccountsservice.so
%{_includedir}/accountsservice-1.0

%files static
%defattr(644,root,root,755)
%{_libdir}/libaccountsservice.a
