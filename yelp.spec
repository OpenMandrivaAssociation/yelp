%define lib_major	0
%define libname         %mklibname %name %{lib_major}
%define libnamedev      %mklibname -d %name 

%define url_ver	%(echo %{version}|cut -d. -f1,2)

Summary:	GNOME 3 help browser
Name:		yelp
Version:	3.4.1
Release:	%mkrel 1
Source0:	http://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
Source1:	yelp.png
URL:		http://live.gnome.org/Yelp
License:	GPLv2+
Group:		Graphical desktop/GNOME
BuildRequires:	pkgconfig(gio-2.0) >= 2.25.11
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 2.91.8
BuildRequires:	pkgconfig(gtk+-unix-print-3.0)
BuildRequires:	pkgconfig(libexslt) >= 0.8.1
BuildRequires:	pkgconfig(liblzma) >= 4.9
BuildRequires:	pkgconfig(libxml-2.0) >= 2.6.5
BuildRequires:	pkgconfig(libxslt) >= 1.1.4
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(webkitgtk-3.0) >= 1.3.2
BuildRequires:	pkgconfig(yelp-xsl) >= 3.1.2
BuildRequires:	pkgconfig(folks)
BuildRequires:	libbzip2-devel
BuildRequires:	sed
BuildRequires:	intltool
BuildRequires:	gnome-doc-utils >= 0.19.1
BuildRequires:	desktop-file-utils >= 0.19
BuildRequires:	gnome-common
BuildRequires:	gettext-devel
BuildRequires:	gtk-doc
BuildRequires:	itstool
Requires:	gnome-doc-utils >= 0.19.1
Requires:	yelp-xsl >= 3.1.2
Requires:	man

%description
Help browser for GNOME 3 which supports docbook documents, info and man.

%files -f %{name}.lang
%doc README TODO AUTHORS NEWS
%{_bindir}/*
%{_datadir}/applications/*
%dir %{_datadir}/gnome/help
%{_datadir}/%{name}
%{_datadir}/glib-2.0/schemas/org.gnome.yelp.gschema.xml
%{_datadir}/pixmaps/gnome-help.png
%{_datadir}/yelp-xsl/xslt/common/domains/yelp.xml

#--------------------------------------------------------------------

%package -n %{libname}
Summary:	Libraries for %name
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains libraries used by the yelp help browser.

%files -n %libname
%{_libdir}/lib%{name}.so.%{lib_major}*

#--------------------------------------------------------------------

%package -n %{libnamedev}
Summary:	Development files for %{name}
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{libnamedev}
This package contains header files and documentation for
the libraries in the yelp-libs package.

%files -n %{libnamedev}
%{_libdir}/lib%{name}.so
%{_includedir}/lib%{name}
%doc %{_datadir}/gtk-doc/html/lib%{name}

#--------------------------------------------------------------------

%prep
%setup -q

%build
%configure2_5x \
	--enable-debug \
	--disable-schemas-compile \
	--disable-rpath \
	--disable-static

%make

%install
rm -rf %{buildroot}
%makeinstall_std

# we don't want these
rm -rf %{buildroot}%{_libdir}/libyelp.a
rm -rf %{buildroot}%{_libdir}/libyelp.la

desktop-file-install \
  --remove-category="Application" \
  --add-only-show-in="GNOME" \
  --add-category="Documentation" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

install -Dpm644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/gnome-help.png

mkdir -p -m 755 %{buildroot}%{_datadir}/gnome/help

%find_lang %{name}

