Name:           kamarada-firstboot
Version:        15.3
Release:        0
Summary:        Kamarada Firstboot
License:        GPL-3.0
Url:            https://gitlab.com/kamarada/firstboot/
Source:         https://gitlab.com/kamarada/firstboot/-/archive/%{version}-dev/firstboot-%{version}-dev.tar.gz#/%{name}.tar.gz

# For directory ownership
BuildRequires:  gnome-session-core

Requires:       feh
Requires:       gnome-shell
Requires:       gnome-shell-extension-hide-activities-button
Requires:       openbox
Requires:       python3
Requires:       sed
Requires:       sudo
Requires:       systemd
Requires:       xsetroot
Requires:       wallpaper-branding-kamarada = %{version}

BuildArch:      noarch


%description
Try / Install welcome screen presented to the user when the Live system boots.


%prep
%setup -q -n %{name}


%build


%install
mkdir -p %{buildroot}%{_bindir}/
install -m0755 usr/bin/kamarada-firstboot %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/applications/
install -m0644 usr/share/applications/* %{buildroot}%{_datadir}/applications/

mkdir -p %{buildroot}%{_datadir}/gnome-session/sessions/
install -m0644 usr/share/gnome-session/sessions/kamarada-firstboot.session %{buildroot}%{_datadir}/gnome-session/sessions/

mkdir -p %{buildroot}%{_datadir}/kamarada-firstboot/png/
install -m0644 usr/share/kamarada-firstboot/kamarada-firstboot.{py,ui} %{buildroot}%{_datadir}/kamarada-firstboot/
install -m0644 usr/share/kamarada-firstboot/png/* %{buildroot}%{_datadir}/kamarada-firstboot/png/

mkdir -p %{buildroot}%{_datadir}/kamarada-firstboot/svg/
# TODO These SVGs were taken from Papirus, I could symlink them
install -m0644 usr/share/kamarada-firstboot/svg/{computer-laptop,media-flash-memory-stick,media-optical,ubiquity-kde}.svg %{buildroot}%{_datadir}/kamarada-firstboot/svg/

mkdir -p %{buildroot}%{_datadir}/locale/en_US/LC_MESSAGES/
install -m0644 usr/share/locale/en_US/LC_MESSAGES/kamarada-firstboot.mo %{buildroot}%{_datadir}/locale/en_US/LC_MESSAGES/

mkdir -p %{buildroot}%{_datadir}/locale/pt_BR/LC_MESSAGES/
install -m0644 usr/share/locale/pt_BR/LC_MESSAGES/kamarada-firstboot.mo %{buildroot}%{_datadir}/locale/pt_BR/LC_MESSAGES/

mkdir -p %{buildroot}%{_datadir}/xsessions/
install -m0644 usr/share/xsessions/com.linuxkamarada.Firstboot.desktop %{buildroot}%{_datadir}/xsessions/

%find_lang kamarada-firstboot


%files -f kamarada-firstboot.lang
%{_bindir}/kamarada-firstboot
%{_datadir}/applications/com.linuxkamarada.Firstboot.Script.desktop
%{_datadir}/applications/com.linuxkamarada.Firstboot.WindowManager.desktop
%{_datadir}/gnome-session/sessions/kamarada-firstboot.session
%{_datadir}/kamarada-firstboot/
%{_datadir}/xsessions/com.linuxkamarada.Firstboot.desktop


%changelog
