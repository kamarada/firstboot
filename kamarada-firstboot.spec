Name:           kamarada-firstboot
Version:        15.3
Release:        0
Summary:        Kamarada Firstboot
License:        GPL-3.0
Url:            https://gitlab.com/kamarada/firstboot/
Source:         https://gitlab.com/kamarada/firstboot/-/archive/%{version}-dev/firstboot-%{version}-dev.tar.gz#/%{name}.tar.gz

Requires:       calamares
Requires:       gnome-shell
# kdesu
Requires:       kde-cli-tools5
Requires:       libqt5-qtstyleplugins-platformtheme-gtk2
Requires:       live-langset-data
Requires:       openbox
Requires:       python3
Requires:       python3-gobject-Gdk
Requires:       sed
Requires:       sudo
Requires:       systemd

BuildArch:      noarch


%description
Try / Install welcome screen presented to the user when the Live system boots.


%prep
%setup -q -n %{name}


%build


%install
mkdir -p %{buildroot}%{_bindir}/
install -m0755 usr/bin/kamarada-firstboot %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_sbindir}/
install -m0755 usr/sbin/kamarada-setup %{buildroot}%{_sbindir}/

mkdir -p %{buildroot}%{_datadir}/kamarada-firstboot/png/
install -m0644 usr/share/kamarada-firstboot/kamarada-firstboot.{py,ui} %{buildroot}%{_datadir}/kamarada-firstboot/
install -m0644 usr/share/kamarada-firstboot/png/* %{buildroot}%{_datadir}/kamarada-firstboot/png/


%files
%{_bindir}/kamarada-firstboot
%{_sbindir}/kamarada-setup
%{_datadir}/kamarada-firstboot/


%changelog
