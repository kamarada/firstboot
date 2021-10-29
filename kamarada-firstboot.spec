Name:           kamarada-firstboot
Version:        15.3
Release:        0
Summary:        Kamarada Firstboot
License:        GPL-3.0
Url:            https://gitlab.com/kamarada/firstboot/
Source:         https://gitlab.com/kamarada/firstboot/-/archive/%{version}-dev/firstboot-%{version}-dev.tar.gz#/%{name}.tar.gz

# For directory ownership
BuildRequires:  gnome-session-core

Requires:       gnome-shell
Requires:       gnome-shell-extension-hide-activities-button

BuildArch:      noarch


%description
Try / Install welcome screen presented to the user when the Live system boots.


%prep
%setup -q -n %{name}


%build


%install
mkdir -p %{buildroot}%{_bindir}/
install -m0644 usr/bin/kamarada-firstboot %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/applications/
install -m0644 usr/share/applications/* %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}%{_datadir}/gnome-session/sessions/
install -m0644 usr/share/gnome-session/sessions/kamarada-firstboot.session %{buildroot}%{_datadir}/gnome-session/sessions/
mkdir -p %{buildroot}%{_datadir}/xsessions/
install -m0644 usr/share/xsessions/com.linuxkamarada.Firstboot.desktop %{buildroot}%{_datadir}/xsessions/


%files
%{_bindir}/kamarada-firstboot
%{_datadir}/applications/com.linuxkamarada.Firstboot.Script.desktop
%{_datadir}/applications/com.linuxkamarada.Firstboot.WindowManager.desktop
%{_datadir}/gnome-session/sessions/kamarada-firstboot.session
%{_datadir}/xsessions/com.linuxkamarada.Firstboot.desktop


%changelog
