#
# Conditional build:
%bcond_without	python		# Python (3) binding
#
Summary:	GObject Data Mapper library
Summary(pl.UTF-8):	Biblioteka GObject Data Mapper
Name:		gom
Version:	0.4
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gom/0.4/%{name}-%{version}.tar.xz
# Source0-md5:	0cc4debe208cb4c91b013e5e57a99808
URL:		https://github.com/GNOME/gom
BuildRequires:	gdk-pixbuf2-devel >= 2.0
BuildRequires:	glib2-devel >= 1:2.36
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	intltool >= 0.40.0
BuildRequires:	meson >= 0.48
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python3-devel >= 1:3.4}
%{?with_python:BuildRequires:	python3-pygobject3-devel >= 3.16.0}
BuildRequires:	rpmbuild(macros) >= 1.714
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
Obsoletes:	gom-static

%description devel
This is the package containing the header files for GOM.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe GOM.

%package apidocs
Summary:	GOM library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki GOM
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
GOM library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GOM.

%package -n python3-gom
Summary:	Python 3 binding for GOM library
Summary(pl.UTF-8):	Wiązanie Pythona 3 do biblioteki GOM
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-pygobject3 >= 3.16.0

%description -n python3-gom
Python 3 binding for GOM library.

%description -n python3-gom -l pl.UTF-8
Wiązanie Pythona 3 do biblioteki GOM.

%prep
%setup -q

%build
CC="%{__cc}" \
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
LDFLAGS="%{rpmldflags}" \
%meson build \
	-Denable-gtk-doc=true
%meson_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install -C build

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO
%attr(755,root,root) %{_libdir}/libgom-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgom-1.0.so.0
%{_libdir}/girepository-1.0/Gom-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgom-1.0.so
%{_includedir}/gom-1.0
%{_pkgconfigdir}/gom-1.0.pc
%{_datadir}/gir-1.0/Gom-1.0.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gom

%if %{with python}
%files -n python3-gom
%defattr(644,root,root,755)
%{py3_sitedir}/gi/overrides/Gom.py
%{py3_sitedir}/gi/overrides/__pycache__/Gom.cpython-*.py[co]
%endif
