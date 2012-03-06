%define major	0
%define libname	%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Summary:	GNOME 3 help browser
Name:		yelp
Version:	3.2.1
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		http://live.gnome.org/Yelp
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.xz
Source1:	yelp.png

BuildRequires:	gettext
BuildRequires:	gnome-doc-utils
BuildRequires:	gnome-common
BuildRequires:	intltool
BuildRequires:	sed
BuildRequires:	gettext-devel
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(folks)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libexslt)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(webkitgtk-3.0)
BuildRequires:	pkgconfig(yelp-xsl)

Requires:	gnome-doc-utils
Requires:	man
Requires:	yelp-xsl

%description
Help browser for GNOME 3 which supports docbook documents, info and man.

%package -n %{libname}
Summary:	Libraries for %name
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains libraries used by the yelp help browser.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package contains header files and documentation for
the libraries in the yelp-libs package.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--disable-static \
	--disable-rpath \
	--disable-schemas-compile \
    --with-search=basic \
    --enable-debug

%make LIBS='-lgthread-2.0'

%install
rm -rf %{buildroot}
%makeinstall_std

desktop-file-install \
	--remove-category="Application" \
	--add-only-show-in="GNOME" \
	--add-category="Documentation" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

mkdir -p %{buildroot}%{_datadir}/pixmaps
cp %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/gnome-help.png

%find_lang %{name}

%files -f %{name}.lang
%doc README TODO AUTHORS NEWS
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/glib-2.0/schemas/org.gnome.yelp.gschema.xml
%{_datadir}/yelp
%{_datadir}/pixmaps/*

%files -n %libname
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{develname}
%{_libdir}/lib%{name}.so
%{_includedir}/lib%{name}
%doc %{_datadir}/gtk-doc/html/lib%{name}

