%define url_ver	%(echo %{version}|cut -d. -f1,2)
%define _disable_rebuild_configure 1

%define major	0
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname -d %{name}

%define __noautoreq 'devel\\(libyelpcommon(.*)'

Summary:	GNOME 3 help browser
Name:		yelp
Version:	3.32.2
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
Url:		http://live.gnome.org/Yelp
Source0:	http://ftp.gnome.org/pub/gnome/sources/yelp/%{url_ver}/%{name}-%{version}.tar.xz
Source1:	yelp.png

BuildRequires:	appstream-util
BuildRequires:	desktop-file-utils >= 0.19
BuildRequires:	gnome-common
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	sed
BuildRequires:	gettext-devel
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(gio-2.0) >= 2.25.11
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(gnome-doc-utils) >= 0.19.1
BuildRequires:	pkgconfig(gtk+-3.0) >= 2.91.8
BuildRequires:	pkgconfig(gtk+-unix-print-3.0)
BuildRequires:	pkgconfig(libexslt) >= 0.8.1
BuildRequires:	pkgconfig(liblzma) >= 4.9
BuildRequires:	pkgconfig(libxml-2.0) >= 2.6.5
BuildRequires:	pkgconfig(libxslt) >= 1.1.4
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(webkit2gtk-4.0) >= 1.3.2
BuildRequires:	pkgconfig(webkit2gtk-web-extension-4.0)
BuildRequires:	pkgconfig(yelp-xsl)
BuildRequires:	pkgconfig(gpg-error)
BuildRequires:	pkgconfig(libgcrypt)
Requires:	gnome-doc-utils >= 0.19.1
Requires:	yelp-xsl
Requires:	man
Requires:	docbook-dtds

%description
Help browser for GNOME 3 which supports docbook documents, info and man.

%package -n %{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries
Suggests:	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains libraries used by the yelp help browser.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains header files and documentation for
the libraries in the yelp-libs package.

%prep
%setup -q

%build
%configure \
	--disable-schemas-compile \
	--disable-static \
	--disable-rpath

%make_build

%install
%make_install

install -Dpm644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/gnome-help.png

mkdir -p -m 755 %{buildroot}%{_datadir}/gnome/help

%find_lang %{name}

%files -f %{name}.lang
%doc README TODO AUTHORS NEWS
%{_bindir}/*
%{_datadir}/applications/*
%dir %{_datadir}/gnome/help
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/apps/org.gnome.Yelp*.svg
%{_datadir}/glib-2.0/schemas/org.gnome.yelp.gschema.xml
%{_datadir}/pixmaps/gnome-help.png
%{_datadir}/yelp-xsl/xslt/common/domains/yelp.xml
%{_datadir}/metainfo/yelp.appdata.xml
%{_libdir}/yelp

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%{_libdir}/lib%{name}.so
%{_includedir}/lib%{name}
%doc %{_datadir}/gtk-doc/html/lib%{name}
