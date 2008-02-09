%define _requires_exceptions libnspr4\\|libplc4\\|libplds4\\|libnss\\|libsmime3\\|libsoftokn\\|libssl3\\|libgtkembedmoz\\|libxpcom

%define req_libgnome_version 2.0.2
%define req_libgtkhtml_version 2.1.2
%define req_gnome_doc_utils_version 0.3.1
%define firefox_version %(rpm -q mozilla-firefox --queryformat %{VERSION})


Summary:	GNOME 2 help browser
Name:		yelp
Version:	2.21.90
Release:	%mkrel 2
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Source1:	yelp.png
Patch: yelp-2.21.1-libbeagle-0.3.0.patch
# from Fedora: register docbook mime type for yelp
Patch2:		yelp-2.13.2-add-mime-handling.patch
# (fc) 2.4.2-4mdk strip newline from title 
Patch4:		yelp-2.6.0-title.patch
URL:		http://live.gnome.org/Yelp
License:	GPL
Group:		Graphical desktop/GNOME
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
Requires:	libgnome2 >= %{req_libgnome_version}
Requires:	gnome-doc-utils >= %{req_gnome_doc_utils_version}
Requires: 	%mklibname mozilla-firefox %firefox_version
Requires:	man
BuildRequires:	gettext
BuildRequires:	libglade2.0-devel
BuildRequires:	mozilla-firefox-devel
BuildRequires:	libgnome2-devel >= %{req_libgnome_version}
BuildRequires:	libgnomeprintui-devel
BuildRequires:	libgnomeui2-devel
BuildRequires:	startup-notification-devel
BuildRequires:	libbeagle-devel >= 0.3.0
BuildRequires:	libbzip2-devel
BuildRequires:	rarian-devel
BuildRequires:	lzma-devel
BuildRequires:	gnome-doc-utils >= %{req_gnome_doc_utils_version}
BuildRequires:	libxslt-devel perl-XML-Parser texinfo
BuildRequires:	desktop-file-utils
BuildRequires:  gnome-common

%description
Help browser for GNOME 2 which supports docbook documents, info and man.

%prep
%setup -q
%patch -p1 -b .libbeagle
%patch2 -p1 -b .add-mime-handling
%patch4 -p1 -b .title

# needed by patch7
autoreconf

%build
%configure2_5x \
    --enable-info \
    --with-search=beagle \
    --enable-debug \
    --with-gecko=firefox \
%if %mdkversion <= 200700
--with-mozilla=mozilla-firefox
%endif

%make

%install
rm -rf %{buildroot}

%makeinstall_std

desktop-file-install \
  --remove-category="Application" \
  --add-only-show-in="GNOME" \
  --add-category="Documentation" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

mkdir -p %{buildroot}%{_datadir}/pixmaps
cp %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/gnome-help.png

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
%post_install_gconf_schemas %name
%{update_menus}
%{update_desktop_database}
%update_icon_cache hicolor


%preun
%preun_uninstall_gconf_schemas %name
%postun
%{clean_menus}
%{clean_desktop_database}
%clean_icon_cache hicolor

%files -f %{name}.lang
%defattr(-,root,root)
%doc README TODO AUTHORS NEWS
%{_sysconfdir}/gconf/schemas/%name.schemas
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/yelp
%{_datadir}/pixmaps/*
%{_iconsdir}/hicolor/*/apps/*.png
