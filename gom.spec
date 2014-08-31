#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	GObject Data Mapper library
Summary(pl.UTF-8):	Biblioteka GObject Data Mapper
Name:		gom
Version:	0.2.1
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gom/0.2/%{name}-%{version}.tar.xz
# Source0-md5:	97a9a260c4fe0ac57568122f53fab13d
URL:		http://www.gtk.org/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake
BuildRequires:	gdk-pixbuf2-devel >= 2.0
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.36
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
BuildRequires:	sqlite3-devel >= 3.7
Requires:	glib2 >= 1:2.36
Requires:	sqlite3 >= 3.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GOM (GObject Data Mapper) is an attempt to make a DataMapper for
GObject.

%description -l pl.UTF-8
GOM (GObject Data Mapper) to próba stworzenia DataMappera dla obieków
biblioteki GObject.

%package devel
Summary:	Header files for GOM library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GOM
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.36

%description devel
This is the package containing the header files for GOM.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe GOM.

%package static
Summary:	Static GOM library
Summary(pl.UTF-8):	Statyczna biblioteka GOM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GOM library.

%description static -l pl.UTF-8
Statyczna biblioteka GOM.

%package apidocs
Summary:	GOM library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki GOM
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
GOM library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GOM.

%prep
%setup -q

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libgom-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgom-1.0.so.0
%{_libdir}/girepository-1.0/Gom-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgom-1.0.so
%{_includedir}/gom-1.0
%{_pkgconfigdir}/gom-1.0.pc
%{_datadir}/gir-1.0/Gom-1.0.gir

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgom-1.0.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gom
