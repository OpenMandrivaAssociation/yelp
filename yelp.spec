%define req_gnome_doc_utils_version 0.19.1

Summary:	GNOME 2 help browser
Name:		yelp
Version:	2.30.2
Release:	%mkrel 6
# fwang: source0 was a merge of upstream webkit and gnome-2-30 branch
# git clone git://git.gnome.org/yelp
# cd yelp
# git checkout webkit
# git merge origin/gnome-2-30
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Source1:	yelp.png
# from Fedora: register docbook mime type for yelp
Patch2:		yelp-2.13.2-add-mime-handling.patch
# (fc) 2.4.2-4mdk strip newline from title 
Patch4:		yelp-2.6.0-title.patch
Patch5:		yelp-2.30.2-xz-support.patch
Patch6:		yelp-missing-slash.patch
Patch7:		yelp-add-mime-type-to-desktop.patch
URL:		http://live.gnome.org/Yelp
License:	GPLv2+
Group:		Graphical desktop/GNOME
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
Requires:	gnome-doc-utils >= %{req_gnome_doc_utils_version}
Requires:	man
BuildRequires:	gettext
BuildRequires:	webkitgtk-devel
BuildRequires:	gtk+2-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  libGConf2-devel
BuildRequires:	startup-notification-devel
BuildRequires:	libbzip2-devel
BuildRequires:	rarian-devel
BuildRequires:	liblzma-devel
BuildRequires:	intltool
BuildRequires:	gnome-doc-utils >= %{req_gnome_doc_utils_version}
BuildRequires:	libxslt-devel texinfo
BuildRequires:	desktop-file-utils
BuildRequires:  gnome-common
BuildRequires:  gettext-devel

%description
Help browser for GNOME 2 which supports docbook documents, info and man.

%prep
%setup -q
%patch2 -p1 -b .add-mime-handling~
#%patch4 -p1 -b .title~
%patch5 -p1 -b .xz~

# yelp-missing-slash.patch
%patch6 -p1 -b .misslash

# yelp-add-mime-type-to-desktop.patch
%patch7 -p1 -b .add-mime-type-to-desktop

#ensure schema is recreated correctly
rm -f data/yelp.schemas

%build
NOCONFIGURE=yes gnome-autogen.sh
%configure2_5x \
    --with-search=basic \
    --enable-debug

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

%preun
%preun_uninstall_gconf_schemas %name

%files -f %{name}.lang
%defattr(-,root,root)
%doc README TODO AUTHORS NEWS
%{_sysconfdir}/gconf/schemas/%name.schemas
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/yelp
%{_datadir}/pixmaps/*
%{_iconsdir}/hicolor/*/apps/*.png
